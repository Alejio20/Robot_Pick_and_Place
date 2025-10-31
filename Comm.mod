MODULE Comm
	
	CONST robtarget pStart:=[[5.06,-0.11,-6.92],[0.0138188,-0.365894,0.93054,-0.00505574],[0,-1,-4,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget pRec:=[[310.63,-70.33,-6.03],[0.0127568,-0.365704,0.930631,-0.00497656],[-1,-1,-5,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget pTri:=[[300.44,-184.15,-7.79],[0.0126439,-0.36571,0.93063,-0.00496706],[-1,-1,-5,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget pStar:=[[250.48,-123.27,-9.13],[0.0128506,-0.365721,0.930622,-0.00502466],[-1,-1,-5,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget pHex:=[[191.06,-174.56,-8.20],[0.0129353,-0.365779,0.930598,-0.00506177],[-1,-1,-5,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
	CONST robtarget pCir:=[[181.73,-64.08,-7.25],[0.0130283,-0.365816,0.930583,-0.00502633],[0,-1,-5,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    
    
    
    PROC Robotserver()
    VAR string receivedStringCoords;   !//Received string
    VAR string sendString;       !//Reply string
    VAR pos pickpos;
    VAR bool ok;
        !Inital Position camera pos
        !MoveL p20, v1000, z50, tool0\WObj:=wobj_pickplace;
        !Create Server in controller
        
        ServerCreateAndConnect;
        !Handshake
        sendString:="request coords";
        TPWrite "Sending to camerasystem:"+sendString;
       
        SendMessage(sendString);
        receivedStringCoords:=ReciveMessage();
        TPWrite "Camera Answer:"+receivedStringCoords;	
        ok:=StrToval(receivedStringCoords,pickpos);
        WaitTime 1;
        sendString:="thanks";
        SendMessage(sendString);
        ServerCloseAndDisconnect;
        
        WaitTime 10;
    ENDPROC
    
    
PROC RobotClient()
    VAR string receivedStringCoords;   !//Received string
    VAR string sendString;       !//Reply string
    VAR pos pickpos;
    VAR bool ok;
    VAR bool okX;
    VAR bool okY;
    VAR bool okShape;
    VAR num posX;
    VAR num posY;
    VAR num shape;
    VAR num length;
    VAR num findPosY;
    
    VAR num counter := 0;
    VAR bool keepListening := TRUE;
    VAR pos targets{30};
    VAR num shapes{30};
    VAR num allShape;
    VAR num allColor;
    VAR num shapeIndex;
    VAR num colorIndex;
    VAR robtarget dropLocations{5} := [pRec, pTri, pHex, pStar, pCir];

     

    ClientCreateAndConnect ;
    
    TPReadFK allShape, "Do you want to pick all objects", stEmpty, stEmpty, stEmpty, "YES", "NO";
    IF allShape = 4 THEN
        shapeIndex := 6;
    ELSE 
        TPReadFK shapeIndex, "Select Shape", "Rectangle", "Triangle", "Hexagonal", "Star", "Circle";
    ENDIF
    
    TPReadFK allColor, "Do you want to pick all colors", stEmpty, stEmpty, stEmpty, "YES", "NO";
    IF allColor = 4 THEN
        colorIndex := 6;
    ELSE 
        TPReadFK colorIndex, "Select Color", "Red", "Blue", "Green", "White", "Black";
    ENDIF
    
    ! Enconde selected index of shape and color and send to client
    sendString:= "shape: " + NumToStr(shapeIndex, 0) + ", color: " + NumToStr(colorIndex, 0);
    SendMessage(sendString);
    
    WHILE keepListening DO
        !//VreceivedStringäntar på order/Svar from PC Funktion returns a string
        receivedStringCoords:=ReciveMessage();
        
        ! Check message from server. If the message is "DONE", exit loop
        IF receivedStringCoords = "DONE" THEN
            keepListening := FALSE;
        ELSE
            counter := counter + 1;
            length := StrLen(receivedStringCoords);
            findPosY := StrFind(receivedStringCoords, 1, "y");
            
            okShape := StrToVal(StrPart(receivedStringCoords, 11, 1), shape);
            okX := StrToVal(StrPart(receivedStringCoords, 19, (findPosY - 22)), posX);
            okY := StrToVal(StrPart(receivedStringCoords, findPosY+4, (length - (findPosY + 4))), posY);
            targets{counter} := [posX, posY, 0];
            shapes{counter} := shape;

            
            TPWrite "shape: " \Num:=shape;
            TPWrite "x: " \Num:=posX;	
            TPWrite "y: " \Num:=posY;
        ENDIF
        
        
    ENDWHILE
    
    
    ! Pick the object from the array of targets
    FOR i FROM 1 TO counter DO
        ! access the index of the current shape anfd save
        shape := shapes{i};
        
        WaitTime 2;
        ! Move to object position to pick
        MoveJ Offs(pStart, targets{i}.x,  targets{i}.y, 100), v500, fine, suction\WObj:=arucowobj;
        ! Move down to pick object
        MoveL Offs(pStart, targets{i}.x,  targets{i}.y, 0), v100, fine, suction\WObj:=arucowobj;
        WaitTime 2;
        ! Pick object
        Set doValve2;
        WaitTime 2;
        ! Move up
        MoveL Offs(pStart, targets{i}.x,  targets{i}.y, 100), v100, fine, suction\WObj:=arucowobj;
        ! Move to drop zone
        MoveJ Offs(dropLocations{shape}, 0,  0, 50), v100, fine, suction\WObj:=arucowobj;
        ! Come down
        MoveL dropLocations{shape}, v50, fine, suction\WObj:=arucowobj;
        WaitTime 2;
        Reset doValve2;
        !Go up
        MoveL Offs(dropLocations{shape}, 0,  0, 50), v100, fine, suction\WObj:=arucowobj;
    ENDFOR
    
    MoveJ pStart, v100, fine, suction\WObj:=arucowobj;
ENDPROC    
    
ENDMODULE