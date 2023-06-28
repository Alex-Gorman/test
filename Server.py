import socket
import select
import json
import sys
import numpy as np
import shutil

terminal_width = shutil.get_terminal_size().columns
line = '*' * terminal_width

def create_3x3_array():
    array_3x3 = []
    for _ in range(3):
        row = []
        for _ in range(3):
            row.append(0)
        array_3x3.append(row)
    return array_3x3

def main():
    print("Server Started.")
    num_clients = 0
    num_of_iterations = 0

    # Get the number of clients
    if len(sys.argv) > 3 or len(sys.argv) < 3:
        print("Usage: python3 Server.py numberOfClients numberOfIterations")
        sys.exit()
    else:
        num_clients = int(sys.argv[1])
        num_of_iterations = int(sys.argv[2])

    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 30000)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(num_clients)

    # List of sockets for select.select()
    sockets_list = [server_socket]

    print("Server listening for incoming connections...")

    # keep track of connected clients
    connected_clients = []

    # accept all the clients before trying to receive messages from them
    try:
        while len(connected_clients) < num_clients:
            readable_sockets, _, _ = select.select(sockets_list, [], [])

            for sock in readable_sockets:
                if sock == server_socket:
                    client_socket, client_address = server_socket.accept()
                    sockets_list.append(client_socket)
                    connected_clients.append(client_socket)
                    print(f'New client connected: {client_address}')
    
    except KeyboardInterrupt:
        print("Keyboard interruption detected. Exciting the program. ")
        sys.exit()

    
    print("All clients connected. Listening for messages...")

    # create the initial 3x3 array
    array_3x3 = create_3x3_array()

    print("\n"+line+"\n")
    print("Total number of iterations to do: "+str(num_of_iterations))
    print("Total number of clients: "+str(num_clients))
    print("\n"+line+"\n")

    # counters for clients and iterations
    client_count = 0
    iterations_count = 0


    try: 
        while True:
            readable_sockets, _, _ = select.select(sockets_list, [], [])

            # Iterate over the sockets that are ready to be read
            for sock in readable_sockets:
                # If a new connection is received, accept it and add it to the list of sockets
                if sock == server_socket:
                    client_socket, client_address = server_socket.accept()
                    sockets_list.append(client_socket)
                    print(f'New client connected: {client_address}')

                # Otherwise, receive data from the connected client    
                else:
                    data = sock.recv(1024)

                    # If no data is received, remove the socket from the list of sockets
                    if not data:
                        sockets_list.remove(sock)
                        print(f'Client disconnected: {sock.getpeername()}')
                        print("One client has disconnected. Exciting the program. ")
                        sys.exit()
                    
                    else:
                        print("3x3 Array received from client: "+str(client_count)+". Iteration: "+str(iterations_count))
                        client_count += 1
                        receive_data = data.decode()
                        array_list = json.loads(receive_data)

                        # Print each array from the list
                        print(array_list)
                        # for array in array_list:
                        #     print(array)
                        
                        for i in range(len(array_list)):
                            for j in range(len(array_list[i])):
                                array_3x3[i][j] += array_list[i][j]
                        
                        print(" ")

                        if (client_count < num_clients):
                            continue
                        else:

                            for i in range(len(array_3x3)):
                                for j in range(len(array_3x3)):
                                    array_3x3[i][j] /= num_clients
                                    array_3x3[i][j] = round(array_3x3[i][j], 1)
                            
                            print("Avg 3x3 array, iteration: "+str(iterations_count))
                            print(array_3x3)
                            print("\n"+line+"\n")

                            client_count = 0
                            iterations_count += 1

                            # Convert the list of arrays to a JSON string
                            array_json = json.dumps(array_3x3)
                            array_list_json = f"{array_json}\n"


                            # Send the JSON string of 3x3 array to each client
                            for clientSocket in connected_clients:
                                clientSocket.sendall(array_list_json.encode())

                            # refresh the 3x3 array
                            array_3x3 = create_3x3_array()
                            
                            # check if done correct num of iterations
                            if iterations_count == num_of_iterations:
                                print("Iterations number met. Exciting system")
                                sys.exit()

    
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exciting the Program.")
        sys.exit()
            


if __name__ == '__main__':
    main()
