import os
import csv
import random

def load_flower_mapping(filename):
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' does not exist.")
        return None
    try:
        flower_mapping = {}
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    flower_letter = parts[0].strip()
                    flower_mapping[flower_letter] = parts[2].strip()  # Assuming pollen count is the third element
        return flower_mapping
    except Exception as e:
        print(f"Failed to read the flower mapping file: {e}")
        return None

def generate_field(width, height, num_flowers, num_pitcher_plants, flower_mapping):
    field = [[' ' for _ in range(width)] for _ in range(height)]
    placements = [(x, y) for x in range(width) for y in range(height)]
    random.shuffle(placements)

    # Places the flowers
    flowers = random.choices(list(flower_mapping.keys()), k=num_flowers)
    for flower in flowers:
        x, y = placements.pop()
        field[y][x] = flower

    # Places the pitcher plants
    for _ in range(num_pitcher_plants):
        x, y = placements.pop()
        field[y][x] = 'P'

    # Places the beehive
    x, y = placements.pop()
    field[y][x] = 'H'

    return field

def save_field(filename, field):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in field:
            writer.writerow(row)

def main():
    file_name = input("Enter the name of the file to save to: ")
    width = int(input("Enter the width of the field: "))
    height = int(input("Enter the height of the field: "))
    num_flowers = int(input("Enter the number of flowers: "))
    num_pitcher_plants = int(input("Enter the number of pitcher plants: "))
    flower_file = input("Enter the path to the flower to pollen mapping file (e.g., 'flower_mapping.txt'): ")

    flower_mapping = load_flower_mapping(flower_file)
    if flower_mapping is None:
        print("Please ensure the flower to pollen mapping file exists and is in the correct format.")
        return
    
    field = generate_field(width, height, num_flowers, num_pitcher_plants, flower_mapping)
    save_field(file_name, field)
    print(f"Field saved to {file_name}.")

if __name__ == "__main__":
    main()
