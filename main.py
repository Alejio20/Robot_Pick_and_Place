# in this lab you create a server on the python side
import json
import socket
from time import sleep

from camera import locateRequestedObjectsCoordinate
from helper import extract_shape_and_color, process_coordinates_with_offset

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set socket listening port. To find the robot adress use cmd and type ipconfig in the terminal, there you see the ip of the robot.
# you may have to open the port in the firewall as well. Note that the ip adress is 127.0.0.1 if you run via Robotstudio
server_socket.bind(("192.168.125.205", 5000))
# Set up the server
# listen to incomming client connection
server_socket.listen()
print("Looking for client")
# accept and store incomming socket connection
(client_socket, client_ip) = server_socket.accept()
print(f"Robot at address {client_ip } connected.")
print("If you would like to end the program, enter 'quit'.")

while True:
    # Wait for answer and print in terminal
    if client_socket.recv:
        client_message = client_socket.recv(4094)
        client_message = client_message.decode("latin-1")
        print(client_message)

        # extract shape and color based onn the message from client
        shape, color = extract_shape_and_color(client_message)

        objects_coordinate = locateRequestedObjectsCoordinate(shape, color)

        # converts coordinates to millimeter from centimeter and handle offset due to distortion
        objects_coordinate = process_coordinates_with_offset(objects_coordinate)

        for coordinate in objects_coordinate:
            shape, x_coordinate, y_coordinate = coordinate
            data = json.dumps({"shape": shape, "x": x_coordinate, "y": y_coordinate})
            # send objects coordinate to the client
            client_socket.send(data.encode("UTF-8"))
            print(data)
            sleep(0.5)

        # inform client that server is done sending data
        message = "DONE"
        client_socket.send(message.encode("UTF-8"))
