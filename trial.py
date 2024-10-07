import mysql.connector
from geopy.distance import geodesic

import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    database = "flight_game",
    user="nirajan",
    password="pass_word"
)

print(connection, "connection established")


# for airport location in game

def airport_type():
    db = """SELECT 
    airport.ident, 
    airport.name, 
    airport.type, 
    airport.iso_country, 
    country.continent, 
    airport.latitude_deg, 
    airport.longitude_deg, 
    country.name AS country_name
    FROM 
    airport JOIN 
    country ON airport.iso_country = country.iso_country
    WHERE 
    airport.type = 'large_airport'
    ;

    """
    db_cursor = connection.cursor(dictionary=True)
    db_cursor.execute(db)
    result = db_cursor.fetchall()
    return result


# get airport information
def get_airport_info(ident):
    #db = """select ident, name, continent, iso_country, latitude_deg, longitude_deg
    #from airports
    #where ident=%s"""
    db = """SELECT 
    airport.ident, 
    airport.name AS airport_name, 
    airport.iso_country, 
    country.name AS country_name,
    airport.continent,
    airport.latitude_deg,
    airport.longitude_deg  
    FROM airport 
    JOIN country ON airport.iso_country = country.iso_country
    WHERE airport.ident = %s"""


    db_cursor = connection.cursor(dictionary=True)
    db_cursor.execute(db, (ident,))
    result = db_cursor.fetchone()
    return result


# to calculate distance between airport in the game
def calculate_distance(current, next):
    start = get_airport_info(current)
    end = get_airport_info(next)
    return geodesic((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km


# to get airport in range

def airport_in_range(icao, airports_range, distance_range):
    travel_range = []
    for airport in airports_range:
        distance = calculate_distance(icao, airport['ident'])
        if distance <= distance_range  and distance != 0:
            travel_range.append(airport)
    return travel_range





# to create new game

def create_game(co2_consumed, money_spent ):
    db_game = "INSERT INTO flight_game.game1(co2_consumed,money_spent) VALUES (%s,%s)"
    db_cursor = connection.cursor(dictionary=True)
    db_cursor.execute(db_game, (co2_consumed, money_spent))


# main code

print("WELCOME TO THE GAME")
player_name = input("Enter your name: ")

game_over = False
win = False

# allocation
money = 5000
distance_range = 2000
allocated_co2 = 10000

all_airports = airport_type()

start_airport = all_airports[0]['ident']

current_airport = start_airport

create_game(0,0)

while True:
    airport = get_airport_info(current_airport)
    print(f"Your are at {airport['airport_name']}.")
    print(f"you have \nMONEY :€{money:.0f} \nRANGE :{distance_range:.0f}km \nALLOCATED Co2 :{allocated_co2:.0f} ")

    input('\033[32mPress Enter to continue...\033[0m')

    if money > 0:

        question_fuel = input("Do you want to buy Fuel ? if yes type y if no type n. : ").upper()
        if question_fuel == "y":

            question_cost = input("please enter amount you want to buy.(€1=2km). :")
            question_cost = int(question_cost)
            if question_cost > money:
                print("Not enough money.")
            else:
                money -= question_cost
                distance_range += question_cost * 2
                print(
                    f"you have \nMONEY :€{money:.0f} \nRANGE :{distance_range:.0f}km \nALLOCATED Co2 :{allocated_co2:.0f} ")

    input('\033[32mPress Enter to continue...\033[0m')

    airport1 = airport_in_range(current_airport, all_airports, distance_range)
    print(f'''\033[34mThere are {len(airport1)} airports in range: \033[0m''')
    if len(airport1) == 0:
        print('You are out of range.')
        game_over = True
    else:
        print(f'''Airports: ''')
        for airport in airport1:
            ap_distance = calculate_distance(current_airport, airport['ident'])
            co2_cost = ap_distance * 0.4
            print(f"{airport['name']}, icao: {airport['ident']}, country: {airport['country_name']}, continent: {airport['continent']}, distance: {ap_distance:.0f}km  Co2 cost: {co2_cost:.0f}")

    destination = input("Enter destination icao code: ")
    selected_destination = calculate_distance(current_airport, destination)
    co2_cost1 = selected_destination * 0.4
    update_location(co2_cost1, money, selected_destination)

    current_airport=destination

    if distance_range < 0 or allocated_co2 < 0 :
        print("GAME OVER")
        break
    else:
        continue
