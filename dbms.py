import mysql.connector
import random
from tabulate import tabulate

import time
from time import sleep
import os
import sys
import subprocess

import tkinter as tk
import mysql.connector as mysql

## TODO
## - Run Transactions Query
## - Edit My Profile
## - Fix Payments in Passenger

mydb = mysql.connect(
  host="localhost",
  user="root",
  password="",
  database="cc2"
)

cursor = mydb.cursor()

fare_dict = {
    ('A', 'B'): 200,
    ('A', 'C'): 400,
    ('A', 'D'): 600,
    ('B', 'A'): 200,
    ('B', 'C'): 200,
    ('B', 'D'): 400,
    ('C', 'A'): 400,
    ('C', 'B'): 200,
    ('C', 'D'): 200,
    ('D', 'A'): 600,
    ('D', 'B'): 400,
    ('D', 'C'): 200
}

def insert_admin():
    admin_ID = 'A' + str(random.randint(42, 100))
    cursor.execute("SELECT admin_ID FROM admin WHERE admin_ID=%s", (admin_ID,))
    result = cursor.fetchone()
    while result is not None:
        admin_ID = 'A' + str(random.randint(42, 100))
        cursor.execute("SELECT admin_ID FROM admin WHERE admin_ID=%s", (admin_ID,))
        result = cursor.fetchone()
    
    print('Your Username is the Admin_ID: ', admin_ID)
    
    password = input("Enter your password: ")
    
    cursor.execute("INSERT INTO login (username, passwor, user_type) VALUES (%s, %s, 'admin')", (admin_ID, password))
    cursor.execute("INSERT INTO admin (admin_ID, username) VALUES (%s, %s)", (admin_ID, admin_ID))

def insert_driver():
    f_name = input("Enter your first name: ")
    l_name = input("Enter your last name: ")
    ph_number = input("Enter your phone number: ")
    number_plate = input("Enter your number plate: ")
    taxi_type = input("Enter your taxi type: ")
    password = input("Enter your password: ")
    
    taxi_ID = 'T' + str(random.randint(42, 100))
    query = "SELECT * FROM taxi WHERE taxi_ID = %s"
    values = (taxi_ID,)
    cursor.execute(query, values)
    while cursor.fetchone() is not None:
        taxi_ID = 'T' + str(random.randint(42, 100))
        values = (taxi_ID,)
        cursor.execute(query, values)
    
    driver_ID = 'D' + str(random.randint(42, 100))
    cursor.execute("SELECT driver_ID FROM driver WHERE driver_ID=%s", (driver_ID,))
    result = cursor.fetchone()
    while result is not None:
        driver_ID = 'D' + str(random.randint(42, 100))
        cursor.execute("SELECT driver_ID FROM driver WHERE driver_ID=%s", (driver_ID,))
        result = cursor.fetchone()
    
    print('Your Username is the Driver_ID: ', driver_ID)
    
    rating  = random.randint(1, 5)
    
    
    cursor.execute("INSERT INTO login (username, passwor, user_type) VALUES (%s, %s, 'driver')", (driver_ID, password))
    
    cursor.execute("INSERT INTO taxi (taxi_ID, number_plate, taxi_type) VALUES (%s, %s, %s)", (taxi_ID, number_plate, taxi_type))
    
    cursor.execute("INSERT INTO driver (driver_ID, username, f_name, l_name, ph_num, rating, taxi_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)", (driver_ID, driver_ID, f_name, l_name, ph_number, rating, taxi_ID))

def insert_passenger():
    f_name = input("Enter your first name: ")
    l_name = input("Enter your last name: ")
    ph_number = input("Enter your phone number: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    
    username = 'P' + str(random.randint(42, 100))
    cursor.execute("SELECT username FROM login WHERE username=%s", (username,))
    result = cursor.fetchone()
    while result is not None:
        username = 'P' + str(random.randint(42, 100))
        cursor.execute("SELECT username FROM login WHERE username=%s", (username,))
        result = cursor.fetchone()
        
    rating  = random.randint(1, 5)

    print('Your Username is: ', username)
    
    cursor.execute("INSERT INTO login (username, passwor, user_type) VALUES (%s, %s, 'passenger')", (username, password))
    cursor.execute("INSERT INTO passenger (username, f_name, l_name, ph_num, email, rating, request_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, f_name, l_name, ph_number, email, rating, None))

##############################
######Admin Functions#########
##############################
def view_drivers():
    cursor.execute("SELECT * FROM driver")
    results = cursor.fetchall()
    print(tabulate(results, headers=['driver_ID','f_name','l_name','phone_number','rating','taxi_ID'], tablefmt='rounded_outline'))

def view_admins():
    cursor.execute("SELECT * FROM admin")
    results = cursor.fetchall()
    print(tabulate(results, headers=['admin_ID','username'], tablefmt='rounded_outline'))

def view_passengers():
    cursor.execute("SELECT * FROM passenger")
    results = cursor.fetchall()
    print(tabulate(results, headers=['username','f_name','l_name','email','phone_number', 'rating', 'request_ID'], tablefmt='rounded_outline'))

def view_rides():
    cursor.execute("SELECT * FROM ride")
    results = cursor.fetchall()
    print(tabulate(results, headers=['ride_ID','request_ID','driver_ID','pickup_time','drop_time'], tablefmt='rounded_outline'))

def view_ride_requests():
    cursor.execute("SELECT * FROM ride_request")
    results = cursor.fetchall()
    print(tabulate(results, headers=['request_ID','passenger_username','pickup_loc','drop_loc','fare','taxi_type','status'], tablefmt='rounded_outline'))

def view_payments():
    cursor.execute("SELECT * FROM payment")
    results = cursor.fetchall()
    print(tabulate(results, headers=['payment_ID','ride_ID','payment_method'], tablefmt='rounded_outline'))

def custom_query():
    def execute_query():
        query = query_text.get('1.0', tk.END)
        # Execute the query and get the results
        cursor = mydb.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        results_text.delete('1.0', tk.END)
        results_text.insert(tk.END, tabulate(results, tablefmt='rounded_outline'))

    root = tk.Tk()
    root.title('Custom Query')
    query_label = tk.Label(root, text='Enter SQL Query:')
    query_label.pack()
    query_text = tk.Text(root, height=10, width=100, wrap='none')
    query_text.pack()

    # Create a button to execute the query
    execute_button = tk.Button(root, text='Execute Query', command=execute_query)
    execute_button.pack()

    # Create a text widget to display the results
    results_text = tk.Text(root, height=15, width=100, wrap = 'none')
    results_text.pack()
       
    root.mainloop()
    
def fetch_request_ID_from_ride_ID(ride_ID):
    cursor.execute("SELECT request_ID FROM ride WHERE ride_ID=%s", (ride_ID,))
    results = cursor.fetchall()
    if results:
        request_ID = results[0][0]
        return request_ID
    
def run_transactions():
    ride_ID = input("Enter the Ride ID to delete:")
    request_ID  = fetch_request_ID_from_ride_ID(ride_ID)
    
    cursor.execute("start transaction; delete from payment where ride_id='%s'; DELETE FROM Ride WHERE ride_id = '%s';UPDATE Ride_request SET status = 'Rejected' WHERE request_id = %s;COMMIT; ", (ride_ID, ride_ID, request_ID,))
    mydb.commit()
    print("Ride Deleted Successfully")
    
    return 0 

def q1(): #Find all rides
        cursor.execute("select ride.ride_ID, ride_request.request_ID, ride_request.fare, ride_request.taxi_type from ride join ride_request on ride.   request_ID=ride_request.request_ID;")
        results = cursor.fetchall()
        print(tabulate(results,headers=['Ride ID', 'Request ID', 'Fare', 'Taxi Type' ], tablefmt='rounded_outline'))

def q2(): #Find all rides sorted by fare
        cursor.execute("select ride_ID, driver_ID, ride_request.fare, ride_request.pickup_loc, ride_request.drop_loc from ride join ride_request on ride.request_ID=ride_request.request_ID order by fare asc;")
        results = cursor.fetchall()
        print(tabulate(results, headers=['Ride ID', 'Driver ID','Fare','PickUp', 'Drop'], tablefmt='rounded_outline'))
        
def q3(): #Find all usernames
        cursor.execute("select username from passenger union select username from driver union select username from admin order by username;")
        results = cursor.fetchall()
        print(tabulate(results, headers=['Usernames'], tablefmt='rounded_outline'))
        
def q4(): #Find passengers with the same rating as drivers
        cursor.execute("select passenger.f_name, passenger.request_ID, driver.driver_id, driver.f_name from passenger join driver on passenger.rating= driver.rating;")
        results = cursor.fetchall()
        print(tabulate(results, tablefmt='rounded_outline'))
    
def q5(): #Find passenger and their requests 
        cursor.execute("select passenger.f_name, passenger.ph_num, passenger.request_ID, ride_request.taxi_type, ride_request.pickup_loc, ride_request.drop_loc, ride_request.fare from passenger join ride_request on passenger.request_ID=ride_request.request_ID order by fare desc;")
        results = cursor.fetchall()
        print(tabulate(results, headers=['Passenger Name', 'Passenger Phone Number', 'Request ID', 'Taxi Type', 'Pickup Loc', 'Drop Loc', 'Fare'], tablefmt='rounded_outline'))
    
def q6(): #Find whether the ride is accepted or rejected

        cursor.execute("select passenger.f_name, passenger.request_ID, ride_request.status from passenger join ride_request on passenger.request_ID=ride_request.request_ID order by fare desc;")
        results = cursor.fetchall()
        print(tabulate(results, headers=['Passenger Name', 'Request ID', 'Status'], tablefmt='rounded_outline'))
        
def q7(): #Find passengers with the same pickup and drop location
        cursor.execute("select passenger.f_name, passenger.request_ID, ride_request.pickup_loc, ride_request.drop_loc from passenger join ride_request on passenger.request_ID=ride_request.request_ID where pickup_loc='A' and drop_loc='D';")
        results = cursor.fetchall()
        print(tabulate(results, headers=['Passenger Name', 'Request ID', 'Pickup Loc', 'Drop Loc'],tablefmt='rounded_outline'))
        
def q8(): #Find the taxi ID, taxi type and driver ID
        cursor.execute("select taxi.taxi_ID, taxi.taxi_type, driver.driver_ID from taxi join driver on taxi.taxi_ID= driver.taxi_ID;")
        results = cursor.fetchall()
        print(tabulate(results, headers=['Taxi ID', 'Taxi Type', 'Driver ID'], tablefmt='rounded_outline'))
            
def q9(): #Find the number of passengers
        cursor.execute("SELECT COUNT(*) FROM passenger")
        results = cursor.fetchall()
        print(tabulate(results, tablefmt='rounded_outline'))
        
def q10(): #Find the popular drop locations
        cursor.execute("SELECT drop_loc, COUNT(*) AS count FROM ride_request GROUP BY drop_loc ORDER BY count DESC LIMIT 10")
        results = cursor.fetchall()
        print(tabulate(results, headers=['Destination', 'Number of rides'], tablefmt='rounded_outline'))  
        
def ten_queries():
    menu = {
            "1": ["Find the price of rides with their taxi types", q1],
            "2": ["Find rides with less fare", q2],
            "3": ["Find the username of everyone", q3],
            "4": ["Find passengers with the same rating as drivers", q4],
            "5": ["Find passenger and their requests ", q5],
            "6": ["Find whether the ride is accepted or rejected", q6],
            "7": ["Find passengers with the same pickup and drop location", q7],
            "8": ["Find the taxi ID, taxi type and driver ID", q8],
            "9": ["Find Number of Passengers", q9], 
            "10": ["Find the popular drop locations", q10],
            "0": ["Logout", logout]
            }
    
        
    while True:
                print("\nMenu:")
                for key in menu:
                    print(key, "-", menu[key][0])
                choice = input("Enter a menu option: ")

                # check if input is valid
                if choice in menu:
                    # call function associated with menu option
                    menu[choice][1]()
                else:
                    print("Invalid input. Please try again.")
                      
###############################
#### Passenger Functions ######
###############################

def fetch_request_ID(username):
    cursor.execute("SELECT request_ID FROM passenger WHERE username = %s", (username,))
    results = cursor.fetchall()
    if results:
        request_ID = results[0][0]
        return request_ID
    else:
        print("You don't have a ride request.")
        return 0

def fetch_ride_ID(username):
    request_ID = fetch_request_ID(username)
    if request_ID:
        cursor.execute("SELECT ride_ID FROM ride WHERE request_ID = %s", (request_ID,))
        results = cursor.fetchall()
        if results:
            ride_ID = results[0][0]
            return ride_ID
        else:
            print("No ride found for the given ride request.")
            return 0
    else:
        return 0

def view_ride_request(username):
    cursor.execute("SELECT * FROM ride_request WHERE passenger_username = %s", (username,))
    results = cursor.fetchall()  # consume all the results
    
    if not results:
        print("You don't have a ride request")
        return
    
    print(tabulate(results, headers=['request_ID', 'passenger_username', 'pickup_loc', 'drop_loc', 'pickup_time', 'drop_time', 'fare', 'taxi_type', 'status'], tablefmt='rounded_outline'))
       
def view_payment(username):
    
    request_ID = fetch_request_ID(username)
    ride_ID = fetch_ride_ID(username)
    
    cursor.execute("SELECT * FROM ride WHERE request_ID = %s", (request_ID,))
    results = cursor.fetchall()# consume all the results
    
    if not results:
        print("You don't have a Accepted Ride")
        return
       
    b = fetch_ride_ID(username)
    cursor.execute("SELECT * FROM payment where ride_ID = %s", (b,))
    result = cursor.fetchall()
    print(tabulate(result, headers=['payment_ID', 'ride_ID', 'payment mode'], tablefmt='rounded_outline'))

def update_pass_profile(username):
    print("Which Detail do you want to update?")
    print("1. First Name")
    print("2. Last Name")
    print("3. Phone Number")
    print("4. Email")
    
    input = int(input("Enter your choice: "))
    if input == 1:
        f_name = input("Enter your first name: ")
        cursor.execute("UPDATE passenger SET f_name = %s WHERE username = %s", (f_name, username))
    if input == 2:
        l_name = input("Enter your last name: ")
        cursor.execute("UPDATE passenger SET l_name = %s WHERE username = %s", (l_name, username))
    if input == 3:
        ph_num = input("Enter your phone number: ")
        cursor.execute("UPDATE passenger SET ph_num = %s WHERE username = %s", (ph_num, username))
    if input == 4:
        email = input("Enter your email: ")
        cursor.execute("UPDATE passenger SET email = %s WHERE username = %s", (email, username))
    return 0

def view_pass_profile(username):
    cursor.execute("SELECT * FROM passenger WHERE username = %s", (username,))
    result = cursor.fetchall()
    print(tabulate(result, headers=['username', 'f_name', 'l_name', 'ph_num', 'rating', 'request_ID'], tablefmt='rounded_outline'))
    print(input("Do you want to update your profile? (y/n)"))
    if input == 'y':
        update_pass_profile(username)
    else:
        return
        
def view_pass_ride(username):
    request_ID = fetch_request_ID(username)
    ride_ID = fetch_ride_ID(username)
    
    cursor.execute("SELECT * FROM ride WHERE request_ID = %s", (request_ID,))
    results = cursor.fetchall()# consume all the results
    
    if not results:
        print("You don't have a Accepted Ride")
        return
    
    print(tabulate(results, headers=['ride_ID', 'request_ID', 'driver_ID', 'pickup_time', 'drop_time'], tablefmt='rounded_outline'))

def price_checker(pickup, drop):
    fares = {
        'A': {
            'B': 200,
            'C': 400,
            'D': 600
        },
        'B': {
            'A': 200,
            'C': 200,
            'D': 400
        },
        'C': {
            'A': 400,
            'B': 200,
            'D': 200
        },
        'D': {
            'A': 600,
            'B': 400,
            'C': 200
        }
    }
    
    fare = fares.get(pickup, {}).get(drop, 0)
    
    fares_with_taxi = {
        'Go': fare + 20,
        'Sedan': fare + 40,
        'XL': fare + 60
    }
    
    table = [[taxi_type, fare] for taxi_type, fare in fares_with_taxi.items()]
    headers = ['Taxi Type', 'Fare']
    print("Here are different taxi types and their fares:")
    print(tabulate(table, headers, tablefmt='rounded_outline'))

def ride_request(username):
    
    pass_username = username
    
    cursor.execute("SELECT * FROM ride_request WHERE passenger_username = %s AND status IN ('Pending', 'Accepted')", (pass_username,))
    result = cursor.fetchall()
    
    if result:
        print("You already have a ride request that is Accepted or Pending.")
        return
    
    pickup = input("Enter your pickup location: ")
    drop = input("Enter your drop location: ")
    
    if pickup == drop:
        print("Pickup and drop locations cannot be the same.")
        return
    fare = fare_dict.get((pickup, drop), None)
    
    if fare is None:
        print("Invalid pickup or drop location.")
        return
    
    price_checker(pickup, drop)
    
    taxi_type = input("Enter your taxi type: ")
    
    if taxi_type not in ['Go', 'Sedan', 'XL']:
        print("Invalid taxi type.")
        return
    fare += {'Go': 20, 'Sedan': 40, 'XL': 60}.get(taxi_type)
    
    while True:
        request_ID = random.randint(52, 100)
        cursor.execute("SELECT request_ID FROM ride_request WHERE request_ID=%s", (request_ID,))
        result = cursor.fetchone()
        if not result:
            break
    
    cursor.execute("INSERT INTO ride_request (request_ID, passenger_username, pickup_loc, drop_loc, fare, taxi_type, status) VALUES (%s, %s, %s, %s, %s, %s, %s)", (request_ID, pass_username, pickup, drop, fare, taxi_type, 'Pending'))
    cursor.execute("UPDATE passenger SET request_ID = %s WHERE username = %s", (request_ID, pass_username))
    
    mydb.commit()
    print("Your ride request has been submitted successfully!")
    print("Your request ID is: ", request_ID)
    print("Your fare is: ", fare)
    view_ride_request(username)
    return 0

###############################
#### Driver Functions ######
###############################

def fetch_taxi_type(username):
    cursor.execute("SELECT * FROM driver WHERE username = %s", (username,))
    result = cursor.fetchall()
    my_taxi_type = result[0][6]
    return my_taxi_type

def view_taxi(username): 
    cursor.execute("SELECT * FROM driver WHERE username = %s", (username,))
    result = cursor.fetchall()
    a = result[0][6]
    cursor.execute("SELECT * FROM taxi WHERE  taxi_ID= %s", (a,))
    results = cursor.fetchall()
    print(tabulate(results, headers=['Taxi ID', 'Number Plate', 'Taxi Type'], tablefmt='rounded_outline'))
    my_taxi = results[0][2]
    return my_taxi
    
def view_drive_ride(username):
    
    cursor.execute("SELECT * FROM driver WHERE username = %s", (username,))
    result = cursor.fetchall()
    a = result[0][0] 
    
    cursor.execute("SELECT * FROM ride where driver_ID = %s", (a,))
    result = cursor.fetchall()
    
    if not result:
        print("You don't have a Accepted Ride")
        return
    
    print(tabulate(result, headers=['Ride ID', 'Ride Request ID', 'Driver ID', 'Pickup Time', 'Dropoff Time'], tablefmt='rounded_outline'))

def update_driver_profile(username):
    print("What do you want to update?")
    print("1. First Name")
    print("2. Last Name")
    print("3. Phone Number")
    input2 = int(input())
    if input2 == 1:
        new_f_name = input("Enter your new first name: ")
        cursor.execute("UPDATE driver SET f_name = %s WHERE username = %s", (new_f_name, username))
        mydb.commit()
        print("Your first name has been updated successfully!")
        view_driver_profile(username)
    if input2 == 2:
        new_l_name = input("Enter your new last name: ")
        cursor.execute("UPDATE driver SET l_name = %s WHERE username = %s", (new_l_name, username))
        mydb.commit()
        print("Your last name has been updated successfully!")
        view_driver_profile(username)
    if input2 == 3:
        new_ph_num = input("Enter your new phone number: ")
        cursor.execute("UPDATE driver SET ph_num = %s WHERE username = %s", (new_ph_num, username))
        mydb.commit()
        print("Your phone number has been updated successfully!")
        view_driver_profile(username)
        return
    return

def view_driver_profile(username):
    cursor.execute("SELECT * FROM driver WHERE username = %s", (username,))
    result = cursor.fetchall()
    
    print(tabulate(result, headers=['driver_ID', 'username','f_name', 'l_name', 'ph_num', 'rating', 'taxi_ID'], tablefmt='rounded_outline'))
    z = input("Do you want to update your profile? (Y/N)")
    if z == 'Y' or z == 'y':
        update_driver_profile(username)
    else:
        return
    
def find_ride(username):
    my_taxi = fetch_taxi_type(username)
    
    cursor.execute("SELECT * FROM driver WHERE username = %s", (username,))
    result = cursor.fetchall()
    a = result[0][0]
    
    cursor.execute("SELECT * FROM ride WHERE driver_ID = %s", (a,))
    result = cursor.fetchall()
    if result:
        print("You already have a ride.")
        return
    
    cursor.execute("SELECT * FROM ride_request WHERE status = 'Pending' AND taxi_type = %s", (my_taxi,))
    result = cursor.fetchall()
    
    if result:
        print("Here are the pending ride requests:")
        
        print(tabulate(result, headers=['request_ID', 'passenger_username', 'pickup_loc', 'drop_loc', 'fare', 'taxi_type', 'status'], tablefmt='rounded_outline'))
        
        request_ID = input("Enter the request ID of the ride you want to accept: ")
        
        cursor.execute("SELECT * FROM ride_request WHERE request_ID = %s", (request_ID,))
        
        result = cursor.fetchone()
        
        if result:
            cursor.execute("UPDATE ride_request SET status = 'Accepted' WHERE request_ID = %s", (request_ID,))
            mydb.commit()
            print("Ride request accepted!")
            
            ride_ID = "R" + str(random.randint(42, 100))
            cursor.execute("SELECT ride_ID FROM ride WHERE ride_ID=%s", (request_ID,))
            result = cursor.fetchone()
            while result is not None:
                ride_ID = "R" + str(random.randint(42, 100))
                cursor.execute("SELECT ride_ID FROM ride WHERE ride_ID=%s", (request_ID,))
                result = cursor.fetchone()

            
            pickup_time = input("Enter the pickup time: ")
            drop_time = input("Enter the drop time: ")
            
            cursor.execute("INSERT INTO ride (ride_ID,request_ID, driver_ID, pickup_time, drop_time) VALUES (%s, %s, %s, %s, %s)", (ride_ID, request_ID, a, pickup_time, drop_time))
            mydb.commit()
            
            print("Ride added!")
            view_drive_ride(username)
        else:
            print("Invalid request ID.")
    else:
        print("There are no pending ride requests for your Taxi Type.")

##################
#### Menus #######
##################
def logout():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Logging out...")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('python dbms.py')    
    
def passenger_menu(username):
    cursor.execute("SELECT * FROM passenger WHERE username = %s", (username,))
    result = cursor.fetchone()
    print("Welcome, " + result[1] + " " + result[2] + "!")
    
    menu = {
        "1": ["View My Ride Request", view_ride_request],
        "2": ["View My Ride", view_pass_ride],
        "3": ["View My Payments", view_payment],
        "4": ["View My Profile", view_pass_profile],
        "5": ["Request a Ride", ride_request],
        "0": ["Logout", logout]
        }
    
    while True:
            print("-------------")
            print("Menu:")
            for key in menu:
                print(key, "-", menu[key][0])
            print("-------------")
            choice = input("Enter a menu option: ")

            # check if input is valid
            if choice in menu:
                if choice == "0":
                    # logout
                    logout()
                    return
                # call function associated with menu option
                menu[choice][1](username)
            else:
                print("Invalid input. Please try again.")
    
def driver_menu(username):
    cursor.execute("SELECT * FROM driver WHERE username = %s", (username,))
    result = cursor.fetchone()
    print("Welcome, " + result[2] + " " + result[3] + "!")
    
    menu = {
        "1": ["View My Ride", view_drive_ride],
        "2": ["View My Taxi", view_taxi],
        "3": ["View My Profile", view_driver_profile],
        "4": ["Find a Ride", find_ride],
        "0": ["Logout", logout]
        }
    
    while True:
            print("-------------")
            print("Menu:")
            for key in menu:
                print(key, "-", menu[key][0])
            print("-------------")
            choice = input("Enter a menu option: ")

            # check if input is valid
            if choice in menu:
                if choice == "0":
                    # logout
                    logout()
                    return
                # call function associated with menu option
                menu[choice][1](username)
            else:
                print("Invalid input. Please try again.")

def admin_menu():
    menu = {
        "1": ["View Drivers", view_drivers],
        "2": ["View Admins", view_admins],
        "3": ["View Passengers", view_passengers],
        "4": ["View Rides", view_rides],
        "5": ["View Ride Requests", view_ride_requests],
        "6": ["View Payments", view_payments],
        "7": ["Custom Query", custom_query],
        "8": ["Ten Queries", ten_queries],
        "9": ["Run Transactions - Delete Ride", run_transactions],
        "0": ["Logout", logout]
        }
        
    while True:
            print("-------------")
            print("Menu:")
            for key in menu:
                print(key, "-", menu[key][0])
            print("-------------")
            choice = input("Enter a menu option: ")

            # check if input is valid
            if choice in menu:
                if choice == "0":
                    # logout
                    logout()
                    return
                # call function associated with menu option
                menu[choice][1]()
            else:
                print("Invalid input. Please try again.")
                
def login():
    
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Check if the username and password match a record in the database
    cursor.execute("SELECT * FROM login WHERE username = %s AND passwor = %s", (username, password))
    result = cursor.fetchone()
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    time.sleep(1)
    if result:
        print("Login successful!")
        print("-----------------")
        if result[2] == 'admin':
            print("Welcome, Admin!",(username))
            admin_menu()
        elif result[2] == 'driver':
            print("Welcome, Driver!",(username))
            print("-----------------")
            driver_menu(username)
        elif result[2] == 'passenger':
            print("Welcome, Passenger!",(username))
            print("-----------------")
            passenger_menu(username)
        
    else:
        print("Invalid username or password. Please try again.")
        login()

def maggi(percent=0, width=30):
    def progress(percent=0, width=30):
        # The number of hashes to show is based on the percent passed in. The
        # number of blanks is whatever space is left after.
        hashes = width * percent // 100
        blanks = width - hashes

        print('\r[', hashes*'#', blanks*' ', ']', f' {percent:.0f}%', sep='',
            end='', flush=True)

    print('This will take a moment')
    for i in range(101):
        progress(i)
        sleep(0.01)
    
    # Newline so command prompt isn't on the same line
    print() 
        
maggi()
os.system('cls' if os.name == 'nt' else 'clear')
print("Welcome to Cab-Connect!\n")
cab = '''
   ██████╗ █████╗ ██████╗  ██████╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗ ██████╗████████╗
  ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔════╝██╔════╝╚══██╔══╝
  ██║     ███████║██████╔╝██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║        ██║   
  ██║     ██╔══██║██╔══██╗██║     ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║        ██║   
  ╚██████╗██║  ██║██████╔╝╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║███████╗╚██████╗   ██║   
   ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝                                                                                           
'''
print(cab)
taxi = '''                                              :^^:                                                     
                          .   ...:^^~!77??JJJ777?77!!~:......                                       
                     ..:^^~^~!77?JJJ?77777J@@J^~!77?JYP5?~^!!~^.                                    
                 .:^^^^^^?J??!~^:^^~^^:::^^&@B^^::^~~~^!?55J!~~!!~^.                                
          ....::::::...~:YJ77777!!!7777!~~~G@@7!~~^~~!!~^^^75P^::^~!!~^:.                           
         ^^^::.........::......::::::::::^^^!?~~~~~~~!!!!!~~!!::::^.:^~~^::::....                   
        ~GPPP~...:^::^..^^:::::..............~....................^............:::::^:::..          
        :???~....:::::...:::^:::^YP~YP~YP~5P~!:^JG~YP~YP~YP~YP~Y5.~:...............:!^...::.        
        ..^::::::::::~?5PP5?~:^~P7^P!^P!^P!~P7^P7^P7^P!^P!^P!^P!:.~:..:!J5PPY7~:::::~~:....^        
       .:..:::::::.^G#&####&#G~^^............^^..^!:.:!..^!:.^^...~:.7B&&B#B#&#5::::..:::::.        
        ::::::::::^B&#P?7??P#&#^^~:::::::::::^~::^J::7?~:~J~:!!:::!:!&#B5!J!YG#&P:::::::::::        
        .:^^^^^^^^~###7J~~?7B##!^~!~~~~~~~~~~!!~~~~~~!~!~!~!~~~~~!~^J&#P?7~!J?##B^^^^^^^^^^^.       
                   .5##555Y#&P.                                      ^B&BJPJP##?                    
                     :?PGGPJ^                                          ~YPGG57.                     
'''                                                                                                
print(taxi)
# Ask the user for login or register

while True:
    action = input('''
_______________________________________________________
Please choose one of the following options:
1. l - Login
2. r - Register 
3. e - Exit the program
_______________________________________________________
INPUT: ''')
    
    if action == 'l':
        login()
    elif action == 'r':
        # Ask the user for their user type
        user_type = input("Are you a driver, passenger or admin? Enter 'd'for driver, 'p' for passenger, and 'a' for admin: ")
        
        # Insert the user data into the database
        if user_type == 'a' or user_type == 'A':
            insert_admin()
            print('Ok, you are an admin.')
        
        elif user_type == 'd' or user_type == 'D':
            insert_driver()
            print('Ok, you are a driver.')

        elif user_type == 'p' or user_type == 'P':
            insert_passenger()
            print('Ok, you are a passenger.')

        mydb.commit()

        print("Registration successful!")
        print("Please log in to your new account.")
        login()   
    elif action == 'e':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Goodbye!")
        break
    else:
        print("Invalid action. Please try again.")

    


