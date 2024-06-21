import os
import csv
#creating a function to load flowerlist file.
def loadflowerlist():
    flowerdict = {}
    while True:
        filename = input("enter the name of the flower list file: ").strip()
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()  # we are using strip function to remove leading and trailing whitespaces
                    parts = line.split(',')  # split 
                    if len(parts) == 3:
                        flower_letter = parts[0].strip()
                        flower_name = parts[1].strip()
                        pollen_count = int(parts[2].strip())
                        flowerdict[flower_letter] = (flower_letter, flower_name, pollen_count)
            break  
        else:
            print(f"The file {filename} does not exist. Please try again.")

    return flowerdict
#creating a function to load the field layout
def field_(flower_info):
    """Creating the game field through a CSV file that ww will load."""
    field = []
    while True:
        filename = input("Please enter the name of the file containing the field: ")
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    field_row = []
                    for char in row:
                        char = char.strip()
                        # To Treat empty strings as spaces
                        if char == '':
                            char = ' '
                        if char not in flower_info and char not in ['H', 'P', ' ', 'U']:
                            raise TypeError(f"Unknown flower type '{char}' is not a known flower type.")
                        field_row.append(char)
                    field.append(field_row)
            break
        else:
            print(f"The file {filename} does not exist. Please try again.")
    return field
#creating a copy of the field
def fieldcopy(original_field):
    """
    Creates a copy of the field with all flowers
    Parameters:
        original_field (list): list representing the original game field. 
    Returns:
        list: list representing the copied field.
    """
    # Creating a new two-dimensional list with the same dimensions as original_field
    field_copy = [[' ' for _ in row] for row in original_field]
    
    # To Iterate over the original field to copy the hive 
    for i, row in enumerate(original_field):
        for j, char in enumerate(row):
            if char == 'H':  #To Keep the hive in the same position
                field_copy[i][j] = 'H'
    
    return field_copy
def print_the_field(field):
    """
    Print the game field in a grid format with row and column index.

    Parameters:
    - field (list of lists): The game field to be printed.
    """
    # Print column headers
    num_columns = len(field[0])
    print("   " + " ".join(str(i).rjust(2) for i in range(num_columns)))
    print("  +" + "---" * num_columns)

    # Printing each row with row index
    for i, row in enumerate(field):
        formatted_row = " | ".join(row)
        print(f"{str(i).rjust(2)}| {formatted_row} ")
def gameintro(flower_info, num_scout_bees, num_worker_bees, pollen_needed):
    """
    Will output the game's rules and information

    Parameters:
    - flower_info: A dictionary of tuples containing flower information.
    - num_scout_bees: The number of scout bees.
    - num_worker_bees: The number of worker bees.
    - pollen_needed: The amount of pollen  that needs to be collected to  win the game.
    """
    print("Welcome to Beeline!")
    print("You are the queen bee trying to produce honey from the pollen of flowers.")
    print("You have two kinds of bees, scouts and workers:")
    print("- Scouts fly to a location and reveal the flowers in a 3x3 grid centered on that location.")
    print("- Workers fly to a location and harvest pollen from any unharvested flowers.")
    print(f"You only have {num_scout_bees} scout bees and {num_worker_bees} worker bees to harvest at least {pollen_needed} units of pollen.")
    print("A bee can only be sent out once, and a flower can only be harvested once.")
    print("Beware of pitcher plants! They'll trap your bees and prevent them from returning to the hive.")
    print("\nThe flowers in the area contain the following units of pollen:")

    # Listing flowers and their pollen values
    for flower_letter, (letter, name, pollen) in flower_info.items():
        print(f"{letter}: {name}, {pollen} units of pollen")

    print("\nGood luck and have fun playing Beeline!")
def area_check(hidden_field, visible_field, x, y, bee_type, flower_info):
    """
    Checks the area a bee is sent to and calculates the  pollen harvested.

    Parameters:
    - hidden_field: The game field with all items hidden except the hive.
    - visible_field: The game field that is visible to the player.
    - x: The x coordinate the bee will be sent to
    - y : The y coordinate the bee will be sent to.
    - bee_type: types of bee
    - flower_info: Information about flowers 

    Returns:
    -  The amount of pollen that will be harvested.
    """
    pollen_harvested = 0
    field_size_x = len(hidden_field)
    field_size_y = len(hidden_field[0]) if field_size_x > 0 else 0

    if x < 0 or y < 0 or x >= field_size_x or y >= field_size_y:
        print("Your bee has left the field and has been lost!")
        return pollen_harvested

    # the range for the 3x3 grid
    x_range = range(max(0, x - 1), min(x + 2, field_size_x))
    y_range = range(max(0, y - 1), min(y + 2, field_size_y))

    for i in x_range:
        for j in y_range:
            current_char = hidden_field[i][j]
            # Checks for pitcher plants
            if current_char == 'P':
                print("Your bee must have fallen into a pitcher plant because it did not return!")
                return 0 
            #bee lost in pitcher plants
            # For scout bees: reveal flowers and used spots
            if bee_type == 'S':
                if current_char in flower_info or current_char == 'U':
                    visible_field[i][j] = current_char

            #writting for worker bees: harvest flowers
            elif bee_type == 'W':
                if current_char in flower_info:
                    visible_field[i][j] = 'U'
                    hidden_field[i][j] = 'U'
                    pollen_harvested += flower_info[current_char][2]
                elif current_char == 'U': 
                    visible_field[i][j] = 'U'

    return pollen_harvested

