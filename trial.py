import mysql.connector
from geopy.distance import geodesic, distance

import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    database="airports",
    user="nirajan",
    password="pass_word"
)

print(connection, "connection established")


# for airport location in game

def airport_type():
    db = """SELECT iso_country, ident, name, type, latitude_deg, longitude_deg 
    FROM airports
    WHERE type='large_airport'   
    """
    db_cursor = connection.cursor(dictionary=True)
    db_cursor.execute(db)
    result = db_cursor.fetchall()
    return result


# get airport information
def get_airport_info(ident):
    db = """select ident, name, continent, iso_country, latitude_deg, longitude_deg 
    from airports 
    where ident=%s"""

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
        if distance <= distance_range and distance != 0:
            travel_range.append(airport)
    return travel_range


def update_location(co2_consumed, money_spent, distance_range):
    db_game1 = "INSERT INTO flight_game.game1(co2_consumed,money_spent,distance_range) VALUES (%s,%s,%s)"
    db_cursor = connection.cursor(dictionary=True)
    db_cursor.execute(db_game1, (co2_cost1, money_spent, distance_range))


"""
def co2_range():
    co2_cost= []
    for airport in co2_range:
        distance_range = calculate_distance(icao, airport['ident'])
        if distance_range <= cost_range  and not distance_range == 0:
            travel_range.append(distance_range * 0.4)
"""


# to create new game

def create_game(co2_consumed, money_spent):
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

create_game(0, 0)

while True:
    airport = get_airport_info(current_airport)
    print(f"Your are at {airport['name']}.")
    print(f"you have \nMONEY :€{money:.0f} \nRANGE :{distance_range:.0f}km \nALLOCATED Co2 :{allocated_co2:.0f} ")

    input('\033[32mPress Enter to continue...\033[0m')

    if money > 0:

        question_fuel = input("Do you want to by Fuel ? if yes type y if no type n. : ").upper()
        if question_fuel == "Y":

            question_cost = input(f"please enter amount you want to buy.(you have €{money} and €1=2km). :")
            question_cost = int(question_cost)

            if question_cost > money:
                print("Not enough money.")
            else:
                money -= question_cost
                distance_range += question_cost * 2
                print(
                    f"Updated values: \nMONEY :€{money:.0f} \nRANGE :{distance_range:.0f}km \nALLOCATED Co2 :{allocated_co2:.0f} ")
        else:
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
            print(
                f'''{airport['name']}, icao: {airport['ident']}, county:{airport['iso_country']}, continent:{airport.get('continent','Unknown')}, distance: {ap_distance:.0f}km, Co2 cost: {co2_cost:.0f}\n''')

        # ask for destination
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

