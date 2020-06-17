#!/usr/bin/env python

__author__ = 'Amanda Yonce and Stack Overflow for geocoder user location\
     and python docs for turtle stuff'

import geocoder
import requests
import time
import turtle


indy_coords = [39.76838, -86.15804]


def get_user_location():
    """gets the coords of the users location"""
    g = geocoder.ip('me')
    print(g.latlng)
    return g.latlng


def get_astronauts():
    """
    Obtains a list of the astronauts who\
    are currently in space, prints their full names, the spacecraft\
    they are currently on board, and the total\
    number of astronauts in space.
    """
    r = requests.get('http://api.open-notify.org/astros.json').json()
    for astro in r['people']:
        print("Craft: " + astro['craft'] + " Astronaut: " + astro['name'])
    print(f"Total # of Astronauts in space is: {len(r['people'])}")
    return(r)


def current_loc_iss():
    """
    Obtains the current geographic coordinates (lat/lon)\
    of the space station, along with a timestamp.
    """
    r = requests.get('http://api.open-notify.org/iss-now.json').json()
    iss_loc = {
        'iss_position': r['iss_position'],
        'timestamp': time.ctime(r['timestamp'])
    }
    print(f"Current ISS Location is {iss_loc['iss_position']}\
          on {iss_loc['timestamp']}")
    return iss_loc


def next_iss_passover(user_coords):
    """
    Sends an api request to get the next time the iss will pass over
    Indy, IN and also the users current location and displays this info on
    the turtle screen
    """
    api_url = 'http://api.open-notify.org/iss-pass.json'
    r_indy = requests.get(f'{api_url}?lat={indy_coords[0]}&lon=\
        {indy_coords[1]}').json()
    indy_next_pass = time.ctime(r_indy['response'][0]['risetime'])
    r_user = requests.get(f'{api_url}?lat={user_coords[0]}&lon=\
        {user_coords[1]}').json()
    user_next_pass = time.ctime(r_user['response'][0]['risetime'])
    return [indy_next_pass, user_next_pass]


def graphics_screen(user_coords, iss_current_loc, next_passes_list):
    """
    Creats a turtle graphics screen to display the location of Indy, IN\
    and the users current location and the ISS current location and\
    the next passover of the ISS at the respective locations
    """
    # Create the screen, add map and iss
    my_turtle = turtle.Screen()
    my_turtle.title("Amanda's ISS Locator")
    my_turtle.bgcolor("grey")
    my_turtle.setup(width=1000, height=500, startx=None, starty=None)
    my_turtle.setworldcoordinates(-180, -90, 180, 90)
    my_turtle.bgpic("map.gif")
    my_turtle.register_shape("iss.gif")
    # place the iss in its current location
    iss = turtle.Turtle()
    iss.shape("iss.gif")
    iss.setheading(90)
    lon = round(float(iss_current_loc['iss_position']['longitude']))
    lat = round(float(iss_current_loc['iss_position']['latitude']))
    iss.penup()
    iss.goto(lon, lat)
    # Place a dot for Indy, IN
    indy = turtle.Turtle()
    indy.shape("circle")
    indy.color("yellow")
    indy.setheading(90)
    indy_lon = round(float(indy_coords[1]))
    indy_lat = round(float(indy_coords[0]))
    indy.penup()
    indy.goto(indy_lon, indy_lat)
    indy.write(next_passes_list[0], font=("Arial", 16, "bold"))
    # Place a dot for user current location
    user = turtle.Turtle()
    user.shape("circle")
    user.color("orange")
    user.setheading(90)
    user_lon = round(float(user_coords[1]))
    user_lat = round(float(user_coords[0]))
    user.penup()
    user.goto(user_lon, user_lat)
    user.write(next_passes_list[1], font=("Arial", 16, "bold"))
    turtle.done()


def main():
    """Gets users current location and maps the ISS and passovers relative\
        to the users location and Indy, IN."""
    user_coords = get_user_location()
    get_astronauts()
    iss_current_loc = current_loc_iss()
    next_passes_list = next_iss_passover(user_coords)
    graphics_screen(user_coords, iss_current_loc, next_passes_list)


if __name__ == '__main__':
    main()
