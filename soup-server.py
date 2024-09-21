#!/usr/bin/env python3

import socket
import sys

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

grocery_aisles = {
    "1": "produce",
    "2": "dry goods",
    "3": "stocks and more",
    "4": "spice supply"
}

produce_aisle = {
    "1": "green onion",
    "2": "red onion",
    "3": "yellow onion",
    "4": "white onion",
    "5": "carrot",
    "6": "tomato",
    "7": "celery stick",
    "8": "potato",
    "9": "sweet potato",
    "10": "corn cob"
}

dry_goods_aisle = {
    "1": "can of pinto beans",
    "2": "can of black beans",
    "3": "can of kidney beans",
    "4": "tube of tomato paste",
    "5": "tub of miso paste",
    "6": "tub of doenjang paste",
    "7": "tub of honey",
    "8": "bottle of apple cider vinegar",
    "9": "bottle of olive oil",
    "10": "pack of noodles"
}

stocks_and_more_aisle = {
    "1": "container of vegetable stock",
    "2": "container of beef stock",
    "3": "container of chicken stock"
}

spice_supply_aisle = {
    "1": "red pepper flake shaker",
    "2": "salt shaker",
    "3": "pepper shaker",
    "4": "garlic powder shaker",
    "5": "cayenne pepper shaker",
    "6": "pack of oregano",
    "7": "pack of thyme",
    "8": "pack of rosemary",
}

inventory = {}

def run_soup_server():
    try:
        HOST = "127.0.0.1"
        PORT = 65432
    except socket.gaierror:
        print('Could not get hostname...Ending server.')
        sys.exit()
    print("server starting - listening for connections at IP", HOST, "and port", PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected established with {addr}\n")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"Received client message:\n'{message}' [{len(data)} bytes]\n")
                take_in_request(conn, message)


def take_in_request(sock, message):
    if "browse" in message:
        init_browse(sock)
    elif "buy" in message:
        init_buy(sock)
    elif "return" in message:
        init_return_item(sock)
    else:
        #NTS: better typo catcher. this just prints and stops!
        print("Sorry, we do not offer that function. Please input 'browse', 'buy', or 'return'")


def init_browse(sock):
    # send message of offerings
    shop_desc = "Sally's Soup Supplies contains four aisles: \n1. produce \n2. dry goods \n3. stocks and more \n4. spice supply\nWhat aisle would you like to browse?"
    print("sending message\n'" + shop_desc + "'\nto client\n")
    sock.sendall(shop_desc.encode('utf-8'))
    
    # receive response and trigger browse
    response = sock.recv(1024).decode('utf-8')
    print(f"received reply:\n'{response}'\nfrom client [{len(response)} bytes]\n")
    
    # validate aisle input
    if response in grocery_aisles:  
        # pass the aisle name to browse
        browse(grocery_aisles[response], sock) 
    else:
        invalid_aisle = "Invalid aisle selection. Please try again. "
        print("sending message\n'" + invalid_aisle + "' to client")  # Add this line
        sock.sendall(invalid_aisle.encode('utf-8'))
        init_browse(sock)


def browse(aisle_name, sock):
    # send info about aisle
    aisle_display = "You are in the " + aisle_name + " aisle."
    
    # 
    if "produce" in aisle_name:
        aisle_display += "\nOn the shelves you see:"
        
        # iterate through aisle supply
        for produce in produce_aisle.values():
            aisle_display += f"\n- {produce}" 
        aisle_display += "\nWould you like to purchase something? (yes/no)"
        
        print("sending message\n'" + aisle_display + "'\nto client\n")
        sock.sendall((aisle_display).encode('utf-8'))
        
        check = sock.recv(1024).decode('utf-8')
        print(f"received reply:\n'{check}'\nfrom client [{len(check)} bytes]\n") 
        
        if "yes" in check:
            purchase_query = "What would you like to purchase?"
            print("sending message\n'" + purchase_query + "'\nto client\n")
            sock.sendall((purchase_query).encode('utf-8'))
        
            # receive response
            product = sock.recv(1024).decode('utf-8')
            print(f"received reply:\n'{product}'\nfrom client [{len(product)} bytes]\n")
        
        elif "no" in check:
            anything_else = "\n\nAll good? (yes/no)"
            
            # send purchase confirmation
            print("sending message\n'" + anything_else + "' to server")
            sock.sendall(anything_else.encode('utf-8'))
            
            more_to_do = sock.recv(1024).decode('utf-8')
            print(f"received reply\n'{more_to_do}'\nfrom client [{len(more_to_do)} bytes]\n")  
            
            if "yes" in more_to_do:
                quit_message = "Operation complete"
                print("sending message\n'" + quit_message + "' to server")
                sock.sendall(quit_message.encode('utf-8'))
            
            else:
                print("\nWelcome to Sally's Soup Supplies. What would you like to do? Input 'browse' to browse the aisles, 'buy' to make a purchase, or 'return' to return an item:\n")
        else:
            error_message = "Please enter (yes/no)"
            print("sending message\n'" + error_message + "' to server")
            sock.sendall(error_message.encode('utf-8'))
            browse(aisle_name, sock)    
    
    elif "dry" in aisle_name:
        aisle_display += "\nOn the shelves you see:"
        
        # iterate through aisle supply
        for dry_good in dry_goods_aisle.values():
            aisle_display += f"\n- {dry_good}" 
        aisle_display += "\nWould you like to purchase something? (yes/no)"
        
        print("sending message\n'" + aisle_display + "'\nto client\n")
        sock.sendall((aisle_display).encode('utf-8'))
        
        check = sock.recv(1024).decode('utf-8')
        print(f"received reply:\n'{check}'\nfrom client [{len(check)} bytes]\n") 
        
        if "yes" in check:
            purchase_query = "What would you like to purchase?"
            print("sending message\n'" + purchase_query + "'\nto client\n")
            sock.sendall((purchase_query).encode('utf-8'))
        
            # receive response and trigger buy
            product = sock.recv(1024).decode('utf-8')
            print(f"received reply:\n'{product}'\nfrom client [{len(product)} bytes]\n")
        
        elif "no" in check:
            anything_else = "\n\nAll good? (yes/no)"
            
            # send purchase confirmation
            print("sending message\n'" + anything_else + "' to server")
            sock.sendall(anything_else.encode('utf-8'))
            
            more_to_do = sock.recv(1024).decode('utf-8')
            print(f"received reply\n'{more_to_do}'\nfrom client [{len(more_to_do)} bytes]\n")  
            
            if "yes" in more_to_do:
                quit_message = "Operation complete"
                print("sending message\n'" + quit_message + "' to server")
                sock.sendall(quit_message.encode('utf-8'))
            else:
                print("\nWelcome to Sally's Soup Supplies. What would you like to do? Input 'browse' to browse the aisles, 'buy' to make a purchase, or 'return' to return an item:\n")
        else:
            error_message = "Please enter (yes/no)"
            print("sending message\n'" + error_message + "' to server")
            sock.sendall(error_message.encode('utf-8'))
            browse(aisle_name, sock)    
            
    elif "stock" in aisle_name:
        aisle_display += "\nOn the shelves you see:"
        
        # iterate through aisle supply
        for stock in stocks_and_more_aisle.values():
            aisle_display += f"\n- {stock}" 
        aisle_display += "\nWould you like to purchase something? (yes/no)"
        
        print("sending message\n'" + aisle_display + "'\nto client\n")
        sock.sendall((aisle_display).encode('utf-8'))
        
        check = sock.recv(1024).decode('utf-8')
        print(f"received reply:\n'{check}'\nfrom client [{len(check)} bytes]\n") 
        
        if "yes" in check:
            purchase_query = "What would you like to purchase?"
            print("sending message\n'" + purchase_query + "'\nto client\n")
            sock.sendall((purchase_query).encode('utf-8'))
        
            # receive response and trigger buy
            product = sock.recv(1024).decode('utf-8')
            print(f"received reply:\n'{product}'\nfrom client [{len(product)} bytes]\n")
        
        elif "no" in check:
            anything_else = "\n\nAll good? (yes/no)"
            
            # send purchase confirmation
            print("sending message\n'" + anything_else + "' to server")
            sock.sendall(anything_else.encode('utf-8'))
            
            more_to_do = sock.recv(1024).decode('utf-8')
            print(f"received reply\n'{more_to_do}'\nfrom client [{len(more_to_do)} bytes]\n")  
            
            if "yes" in more_to_do:
                quit_message = "Operation complete"
                print("sending message\n'" + quit_message + "' to server")
                sock.sendall(quit_message.encode('utf-8'))  
            
            else:
                print("\nWelcome to Sally's Soup Supplies. What would you like to do? Input 'browse' to browse the aisles, 'buy' to make a purchase, or 'return' to return an item. It is suggested to browse first. \n")
        else:
            error_message = "Please enter (yes/no)"
            print("sending message\n'" + error_message + "' to server")
            sock.sendall(error_message.encode('utf-8'))
            browse(aisle_name, sock)    
            
    elif "spice" in aisle_name:
        aisle_display += "\nOn the shelves you see:"
        
        # iterate through aisle supply
        for spice in spice_supply_aisle.values():
            aisle_display += f"\n- {spice}" 
        aisle_display += "\nWould you like to purchase something? (yes/no)"
        
        print("sending message\n'" + aisle_display + "'\nto client\n")
        sock.sendall((aisle_display).encode('utf-8'))
        
        check = sock.recv(1024).decode('utf-8')
        print(f"received reply:\n'{check}'\nfrom client [{len(check)} bytes]\n") 
        
        if "yes" in check:
            purchase_query = "What would you like to purchase?"
            print("sending message\n'" + purchase_query + "'\nto client\n")
            sock.sendall((purchase_query).encode('utf-8'))
        
            # receive response and trigger buy
            product = sock.recv(1024).decode('utf-8')
            print(f"received reply:\n'{product}'\nfrom client [{len(product)} bytes]\n")
        
        elif "no" in check:
            anything_else = "\n\nAll good? (yes/no)"
            
            # send purchase confirmation
            print("sending message\n'" + anything_else + "' to server")
            sock.sendall(anything_else.encode('utf-8'))
            
            more_to_do = sock.recv(1024).decode('utf-8')
            print(f"received reply\n'{more_to_do}'\nfrom client [{len(more_to_do)} bytes]\n")  
            
            if "yes" in more_to_do:
                quit_message = "Operation complete"
                print("sending message\n'" + quit_message + "' to server")
                sock.sendall(quit_message.encode('utf-8'))
            
            else:
                print("\nWelcome to Sally's Soup Supplies. What would you like to do? Input 'browse' to browse the aisles, 'buy' to make a purchase, or 'return' to return an item:\n")
        else: 
            error_message = "Please enter (yes/no)" + browse(sock)
            print("sending message\n'" + error_message + "' to server")
            sock.sendall(error_message.encode('utf-8'))
            
    else:
        error_message = "Please enter a valid aisle number (1 - 4)" + browse(sock)
        print("sending message\n'" + error_message + "' to server")
        sock.sendall(error_message.encode('utf-8'))    

    # check product in aisle 
    if product in aisle_display:  
        quantity_query = "What quantity of " + product +  " would you like to buy?"
        print("sending message\n'" + quantity_query + "'\nto client\n")
        sock.sendall((quantity_query).encode('utf-8'))
        
        quantity = sock.recv(1024).decode('utf-8')
        print(f"received reply:\n'{quantity}'\nfrom client [{len(quantity)} bytes]\n")
        
        # make sure quantity is in int form
        quantity = int(quantity)
        
        # pass the item to purchase
        buy(product, quantity, sock)
    else:
        error_message = 'Invalid product selection. Please try again.'
        print("sending message\n'" + error_message + "'\nto server")
        sock.sendall(error_message.encode('utf-8'))


def init_buy(sock):
    # take input
    purchase_prompt = "What aisle would you like to purchase from? (please use the browse() function to see aisle contents)"
    sock.sendall(purchase_prompt.encode('utf-8'))
    # NTS: thinking here, split the string to find item # and ID   
    
    # NTS: add case to insure response is an int!
    purchase_response = sock.recv(1024).decode('utf-8')
    print(f"received reply:\n'{purchase_response}'\nfrom client [{len(purchase_response)} bytes]\n")

    # process response!
    if purchase_response == "1" or purchase_response == "2" or purchase_response == "3" or purchase_response == "4":
        aisle_location = int(purchase_response)
        confirm_location = ("Purchasing from aisle " + purchase_response + ". What would you like to buy from this aisle? " )
        sock.sendall(confirm_location.encode('utf-8'))
        
        product = sock.recv(1024).decode('utf-8')
        print(f"received reply:\n'{product}'\nfrom client [{len(product)} bytes]\n")
        
        # check if product is in aisle of designated aisle_location #
        # i.e., produce = 1, dry goods = 2, stocks = 3, spices = 4
        if (aisle_location == 1 and product in produce_aisle.values()) or \
           (aisle_location == 2 and product in dry_goods_aisle.values()) or \
           (aisle_location == 3 and product in stocks_and_more_aisle.values()) or \
           (aisle_location == 4 and product in spice_supply_aisle.values()):  
            quantity_query = "What quantity of " + product +  " would you like to buy?"
            print("sending message\n'" + quantity_query + "'\nto client\n")
            sock.sendall((quantity_query).encode('utf-8'))
            
            quantity = sock.recv(1024).decode('utf-8')
            print(f"received reply:\n'{quantity}'\nfrom client [{len(quantity)} bytes]\n")
            
            # make sure quantity is in int form
            quantity = int(quantity)
            
            # pass the item to purchase
            buy(product, quantity, sock)
            
        else: 
            # NTS: break
            error_code = "We do not have " + product + " in aisle " + str(aisle_location) + "."
            print("sending message\n'" + error_code + "'\nto client\n")
            sock.sendall((error_code).encode('utf-8'))
    
    else:
        invalid_location = (purchase_response + " is not a valid input. Please enter a value between 1 and 4:\n")
        sock.sendall(invalid_location.encode('utf-8'))    
        init_buy(sock)    
  
def buy(product, quantity, sock):    
    # declare inventory
    global inventory
    
    # if quantity is 1
    # singular form
    if quantity == 1:
        confirmation = "You are purchasing " + str(quantity) + " " + product + "."
        confirmation += " Correct? (yes/no)"
    
    # if quantity > 1
    # plural form
    # NTS: change the product names to be grammatically correct!
    elif quantity > 1:
        confirmation = "You are purchasing " + str(quantity) + " " + product + "s."
        confirmation += " Correct? (yes/no)"
        
    else:
        confirmation = "You cannot purchase " + str(quantity) + " " + product + "s."
        confirmation += " Please choose a quantity >= 1"  
        # NTS: finish (break)     
    
    # add functionality for item quantity and whatnot
    print("sending message\n'" + confirmation + "'\nto server\n")
    sock.sendall(confirmation.encode('utf-8'))
    
    # receive confirmation response
    response = sock.recv(1024).decode('utf-8')
    print(f"received reply\n'{response}'\nfrom client [{len(response)} bytes]\n")
    
    # check confirmation
    if "yes" in response:  
    # confirm purchase
        if quantity == 1:
            purchase_confirmation_and_inventory_update = "You have purchased " + str(quantity) + " " + product + "."
            inventory[product] = str(quantity)
        
        elif quantity > 1:
            purchase_confirmation_and_inventory_update = "You have purchased " + str(quantity) + " " + product + "s."
            inventory[product + "s"] = str(quantity)
        
        # add inventory update
        purchase_confirmation_and_inventory_update += "\n\nInventory:\n" + str(inventory)
        purchase_confirmation_and_inventory_update += "\n\nAll good? (yes/no)"
        
        # send purchase confirmation
        print("sending message\n'" + purchase_confirmation_and_inventory_update + "' to server")
        sock.sendall(purchase_confirmation_and_inventory_update.encode('utf-8'))
        
        more_to_do = sock.recv(1024).decode('utf-8')
        print(f"received reply\n'{more_to_do}'\nfrom client [{len(more_to_do)} bytes]\n")  
        
        if "yes" in more_to_do:
            quit_message = "Operation complete"
            print("sending message\n'" + quit_message + "' to server")
            sock.sendall(quit_message.encode('utf-8'))
             
    else:
        abort = "Aborting purchase\nOperation complete"
        print("sending message\n'" + abort + "' to server")
        sock.sendall(abort.encode('utf-8'))


def init_return_item(sock):
    global inventory
    
    # print inventory
    return_item_query = "Inventory:\n" + str(inventory) +"\n\n"
    
    return_item_query += "What would you like to return? Please enter the item name:"
    print("sending message\n'" + return_item_query + "' to server")
    sock.sendall(return_item_query.encode('utf-8'))
    
    # receive confirmation response
    response = sock.recv(1024).decode('utf-8')
    print(f"received reply\n'{response}'\nfrom client [{len(response)} bytes]\n")    
    
    # check if return item in inventory
    if response in inventory:
        # check quantity in inventory
        quantity = inventory[response] 
        
        # ask how many of the item to return
        quantity_to_return = "How many " + response + "s would you like to return? You have " + quantity + " " + response + "s"
        print("sending message\n'" + quantity_to_return + "' to server")
        sock.sendall(quantity_to_return.encode('utf-8'))     
        
        # receive confirmation response
        return_quantity = sock.recv(1024).decode('utf-8')
        print(f"received reply\n'{return_quantity}'\nfrom client [{len(return_quantity)} bytes]\n")    
        
        # check if sufficient quantity to be returned
        if int(return_quantity) <= int(quantity):
            # check to make sure quantity is restored to a string!
            quantity = return_quantity 
            
            # send info to return_item()
            return_item(response, quantity, sock)
        else:
            # NTS: send error message you cannot return that many items
            return_quantity_error = "You do not have " + quantity + " " + response + init_return_item(sock)
            print("sending message\n'" + return_quantity_error + "' to server")
            sock.sendall(return_quantity_error.encode('utf-8'))      
            
    else:
        error_message = f"{response} is not in your inventory."
        print("sending message\n'" + error_message + "' to server")
        sock.sendall(error_message.encode('utf-8'))    
    
def return_item(product, quantity, sock):
    confirmation = f"You are returning {quantity} {product}(s). Correct? "
    print("sending message\n'" + confirmation + "' to server")
    sock.sendall(confirmation.encode('utf-8'))
    
    # wait for confirmation response
    confirm_response = sock.recv(1024).decode('utf-8')
    if "yes" in confirm_response:
        # decrement inventory quantity
        # convert to int, then back to string
        inventory[product] = str(int(inventory[product]) - int(quantity))
        success_message = f"You have successfully returned {quantity} {product}(s)."
        success_message += "\n\nInventory:\n" + str(inventory)
        success_message += "\n\nAll good? (yes/no)"
        print("sending message\n'" + success_message + "' to server")
        sock.sendall(success_message.encode('utf-8'))
        
        more_to_do = sock.recv(1024).decode('utf-8')
        print(f"received reply\n'{more_to_do}'\nfrom client [{len(more_to_do)} bytes]\n")  
        
        if "yes" in more_to_do:
            quit_message = "Operation complete"
            print("sending message\n'" + quit_message + "' to server")
            sock.sendall(quit_message.encode('utf-8'))
    else:
        sock.sendall("Return canceled.".encode('utf-8'))

if __name__ == "__main__":
    run_soup_server()
    print("server is done!")