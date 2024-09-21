#!/usr/bin/env python3

import socket
import sys

HOST = "127.0.0.1"  # This is the loopback address
PORT = 65432        # The port used by the server

def run_soup_client():
    print("")
    try:
        HOST = "127.0.0.1"
        PORT = 65432
    except socket.gaierror:
        print('Invalid hostname, exiting...')
        sys.exit()
    print("client starting - connecting to server at IP", HOST, "and port", PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"connection established")
        while True:
            # loop until the user asks to leave
            if not check_out(s):
                break


def check_out(sock):
    print("\nWelcome to Sally's Soup Supplies. What would you like to do? Input 'browse' to browse the aisles, 'buy' to make a purchase, or 'return' to return an item:\n")
    while True:  # Loop to keep asking for input until 'leave' is entered
        msg = input()
        if msg == 'leave':
            print("client quitting at operator request")
            return False
        
        print(f"\nsending request '{msg}' to server")
        sock.sendall(msg.encode('utf-8'))
        print("request sent, waiting for reply\n")
        
        reply = sock.recv(1024).decode()
        if not reply:
            return False
        else:
            print(f"received reply:\n'{reply}'\nfrom server")
        
        if "What aisle would you like to browse?" in reply:
            aisle_selection = input("\nPlease enter the aisle number you would like to browse:\n")
            sock.sendall(aisle_selection.encode('utf-8'))
            
            # wait for response
            aisle_response = sock.recv(1024).decode('utf-8')
            print(f"\nreceived reply:\n'{aisle_response}'\nfrom server")
        
        if "You are purchasing" in reply:
            confirmation = input()
            sock.sendall(confirmation.encode('utf-8'))
            
            # wait for response
            confirmation_response = sock.recv(1024).decode('utf-8')
            print(f"\nreceived reply:\n'{confirmation_response}'\nfrom server") 

        if "What would you like to return" in reply:
            return_query = input()
            sock.sendall(return_query.encode('utf-8'))
            
            # wait for response
            return_query_response = sock.recv(1024).decode('utf-8')
            print(f"\nreceived reply:\n'{return_query_response}'\nfrom server")    

        if "What quantity" in reply:
            quantity = input()
            sock.sendall(quantity.encode('utf-8'))
            
            # wait for response
            quantity_response = sock.recv(1024).decode('utf-8')
            print(f"\nreceived reply:\n'{quantity_response}'\nfrom server")    
            
        if "What aisle" in reply:
            aisle_num = input()
            sock.sendall(aisle_num.encode('utf-8'))
            
            # wait for response
            aisle_num_response = sock.recv(1024).decode('utf-8')
            print(f"\nreceived reply:\n'{aisle_num_response}'\nfrom server")    

        
        if "You are returning" in reply:
            return_confirmation = input()
            sock.sendall(return_confirmation.encode('utf-8'))
            
            # wait for response
            return_confirmation_response = sock.recv(1024).decode('utf-8')
            print(f"\nreceived reply:\n'{return_confirmation_response}'\nfrom server")           
        
        if "How many" in reply:
            return_quantity_query = input()
            sock.sendall(return_quantity_query.encode('utf-8'))
            
            # wait for response
            return_quantity_query_response = sock.recv(1024).decode('utf-8')
            print(f"\nreceived reply:\n'{return_quantity_query_response}'\nfrom server")           
               
        # follow-up question after each operation
        if "Operation complete" in reply:
            follow_up = input("\nIs there anything else you would like to do? (yes/no) ")
            if follow_up.lower() != 'yes':
                print("client quitting at operator request")
                return False
            else:
                print("\nWelcome to Sally's Soup Supplies. What would you like to do? Input 'browse' to browse the aisles, 'buy' to make a purchase, or 'return' to return an item:\n")
                continue

if __name__ == "__main__":
    run_soup_client()
