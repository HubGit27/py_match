"""
File:    py_match.py
Author:  Brandon Ta
Date:    4/20/2022
Section: 23
E-mail:  bta1@umbc.edu
Description:
  This simulates a card matching game
"""

from ast import Pass
import random


def create_map(row, col, seed):
    '''
    Creates the map of random cards
    :param row: How many rows of cards the user wants
    :param col: How many columns of cards the user wants
    :param seed: seed to determine the random cards
    :returns: 2d array of cards
    '''

    random.seed(seed)
    #Opens the file with random characters/ cards
    file_name = input("What is the symbol file name?")
    with open(file_name, 'r') as my_file:
        symbol = my_file.read()
    symbols = list(symbol.split(" "))

    #Creates the main map with the random letters
    the_map = []
    for i in range(col):
        the_map.append(list())
        for j in range(row):
            the_map[i].append(random.choice(symbols))

    return the_map


def display_map(my_map, coordinates):
    '''
    Displays the map and if the card is flipped over
    :param my_map: 2D array of all the map
    :param coordinates: array of coordinates to have flipped over
    :returns: None
    '''
    #Displays the map and the correct guesses
    for i in range(len(my_map)):
        for j in range(len(my_map[i])):
            if [i,j] in coordinates:
                print(my_map[i][j], end=" ")
            else: print(".", end=" ")
        print()


def invalid_coordinate(guess, my_map, coordinates):
    '''
    Ensures that the users guess are valid coordinates that won't be out of bounds
    or already guessed
    :param guess: string of the users guess
    :param my_map: 2D array of all the map
    :param coordinates: array of coordinates already guessed
    :returns: boolean
    '''

    guess = guess.split(" ")
    y = int(guess[0])
    x = int(guess[1])

    #Checks if the coodinates are out of bounds or already called
    if x > len(my_map[0]):
        return True
    elif y > len(my_map):
        return True
    elif [y-1,x-1] in coordinates:
        return True
    else:
        return False


def play_game(my_map):
    '''
    Runs the game until all the cards are found
    :param my_map: 2-D array of all the cards
    :returns: none
    '''

    all_cards_list = list()
    all_cards = {}
    temp_cards = {}
    finished_coordinates = list()
    temp_coordinates = list()
    game_over = False

    #Adds all of the cards to a dictionary and list
    for i in my_map:
        for j in i:
            all_cards_list.append(i)
            if j in all_cards:
                all_cards[j] += 1

            else:
                all_cards[j] = 1
                temp_cards[j] = 0

    #Ask the user to enter coordinates and makes sure that it is valid
    guess = input("Enter the position to guess: ")
    while invalid_coordinate(guess, my_map, finished_coordinates):
        guess = input("Position is out of bounds, enter again ")

    #Loop to keep the game going until everything is guessed
    while game_over == False:

        same_letter = False

        #Adds letters already guessed to game
        for i in finished_coordinates:
            temp_coordinates.append(i)

        #Takes the guess and makes it a coordinate
        coordinate = guess.split(" ")
        coordy = int(coordinate[0]) - 1
        coordx = int(coordinate[1]) - 1
        coordinate = [coordy, coordx]

        #Adds the coordinate to the list of coordinates
        temp_coordinates.append(coordinate)
        symbol = (my_map[coordy][coordx])
        temp_cards[symbol] += 1

        #If all of the same card has been guessed
        if temp_cards[symbol] == all_cards[symbol]:
            print(f"You have found all of the {symbol}")
            all_cards[symbol] = 0
            finished_coordinates = []
            for i in temp_coordinates:
                finished_coordinates.append(i)
            same_letter = True
        
        display_map(my_map, temp_coordinates)

        #Makes the user guess the same card if there are other matches
        while same_letter == False:
            guess = input(f"Enter position to guess that matches {symbol}, there are {all_cards[symbol] - temp_cards[symbol]} remaining: ")
            while invalid_coordinate(guess, my_map, temp_coordinates):
                guess = input("Invalid coordinate, enter again ")
            coordinate = guess.split(" ")
            coordy = int(coordinate[0]) - 1
            coordx = int(coordinate[1]) - 1
            coordinate = [coordy, coordx]
            temp_coordinates.append(coordinate)
            symbol1 = (my_map[coordy][coordx])

            #If the right card was flipped
            if symbol1 == symbol:
                temp_cards[symbol] += 1
                if temp_cards[symbol] == all_cards[symbol]:
                    print(f"You have found all the {symbol}")
                    same_letter = True
                    finished_coordinates = []
                    for i in temp_coordinates:
                        finished_coordinates.append(i)
                display_map(my_map, temp_coordinates)

            #If the wrong card was flipped
            else:
                print("No match this time: ")
                display_map(my_map, temp_coordinates)
                print("Try again!")
                temp_coordinates = []
                temp_cards[symbol] = 0
                same_letter = True

        #Finishes the game
        if len(finished_coordinates) >= len(all_cards_list):
            game_over = True
            print("Congratulations, you win!")
        else:
            guess = input("Enter position to guess: ")
            while invalid_coordinate(guess, my_map, finished_coordinates):
                guess = input("Invalid coordinate, enter again ")

            temp_coordinates = []


if __name__ == '__main__':
    the_map = create_map(*list(map(int, input('Enter Row, Col, Seed: ').split(","))))
    display_map(the_map, [])
    play_game(the_map)

