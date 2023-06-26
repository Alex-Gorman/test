import socket
import time
import random
import numpy as np
import sys
import json
import shutil

terminal_width = shutil.get_terminal_size().columns
line = '*' * terminal_width

def main():
    # Create TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's address and port
    server_address = ('localhost', 30000)

    # Try connecting the server
    try:
        client_socket.connect(server_address)
    except ConnectionError as e:
        print("Unable to connect to the server:", str(e))
        sys.exit()

    # Client connected to the server
    print("Connected to server...")

    # list of numpy arrays
    array_list = []
    lengths = [3, 3, 3]

    # add the numpy arrays to the list
    for length in lengths:
        random_array = np.random.randint(1, 11, size=length)
        
        # Convert NumPy array to list since to can't convert NumPy array to JSON
        array_list.append(random_array.tolist())

    # set the print options to remove the delimiter space
    np.set_printoptions(formatter={'int': lambda x: f'{x}'})

    num_of_iterations = 0
    
    try:
        # Infinite loop
        while True:
            # Sleep for a random amount of time
            time.sleep(random.randint(1, 10))

            # Convert the list of NumPy arrays to a JSON string
            array_list_json = json.dumps(array_list)

            # Send the JSON string to the server
            client_socket.sendall(array_list_json.encode())

            # Receive the response from the server
            try:
                print("\n"+line+"\n") 
                data = client_socket.recv(1024)
                if not data:
                    print("Connection error with Server detected. Exciting program. ")
                    sys.exit()
                
                # print the sent data to server
                print("Iteration: "+str(num_of_iterations))
                print(str(array_list)+"\n")

                # Split the received data into individual JSON objects
                received_data = data.decode()
                json_objects = received_data.split("\n")

                for json_obj in json_objects:
                    if json_obj:
                        # Print the response from the server
                        print(f'Iteration: {num_of_iterations}. Average received from Server. \n{json_obj}')
                        num_of_iterations += 1

                        # Get the 3x3 array list from the server
                        array_list = json.loads(json_obj)
                        
                        # Randomly multiply each element in the array list by 0.1 to 1
                        for i in range(len(array_list)):
                            for j in range(len(array_list[i])):
                                multiplier = random.uniform(0.1, 1)
                                array_list[i][j] *= multiplier
                                array_list[i][j] = round(array_list[i][j], 1)


            except ConnectionError:
                print("Connection error with Server detected. Exciting program. ")
                sys.exit()
    

    # If you get a keyboard interrupt then exit the program
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exciting Program.")
        sys.exit()


if __name__ == '__main__':
    main()