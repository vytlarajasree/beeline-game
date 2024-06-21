from BeeFunctions import loadflowerlist,field_, fieldcopy, print_the_field, gameintro, area_check
import sys

def main():
    try:
        # Loading the flower list
        flower_info = loadflowerlist()

        # Creating the hidden field
        hidden_field = field_(flower_info)

        # Creating a visible copy of the field
        visible_field = fieldcopy(hidden_field)
    except TypeError as e:
        print(e)
        sys.exit(-1)

    # Requirements and game rules 
    scout_bees = 5
    worker_bees = 5
    pollen_collected = 0
    pollen_needed = 20

    # Introductory information
    gameintro(flower_info, scout_bees, worker_bees, pollen_needed)
    # Game logic loop
    while worker_bees > 0 and pollen_collected < pollen_needed:
        print_the_field(visible_field)
        print(f"Scout bees left: {scout_bees}, Worker bees left: {worker_bees}, Pollen collected: {pollen_collected}")
        print("H is the hive, U is a used flower")
        bee_type = input("What type of bee would you like to send out (S for scout, W for worker): ").upper()
        if bee_type not in ['S', 'W']:
            print("That is not a valid bee type!")
            continue
        try:
            x = int(input("Enter x coordinate (0-9): "))
            y = int(input("Enter y coordinate (0-9): "))
        except ValueError:
            print("Invalid input. Please enter numbers for coordinates.")
            continue
        if bee_type == 'S' and scout_bees > 0:
            scout_bees -= 1
            pollen_collected += area_check(hidden_field, visible_field, x, y, 'S', flower_info)
        elif bee_type == 'W' and worker_bees > 0:
            worker_bees -= 1
            pollen_collected += area_check(hidden_field, visible_field, x, y, 'W', flower_info)
        else:
            print(f"No more {bee_type} bees left!")
            continue
    if pollen_collected >= pollen_needed:
        print("Congratulations! You've collected enough pollen and won the game!")
    else:
        print("Unfortunately, you didn't manage to collect enough pollen. Better luck next time!")

if __name__ == "__main__":
    main()
