# mushroom_import_unlimited.py

# Step 1: ask for map filename
filename = input("Enter map file name (e.g. map1.txt): ")

# Step 2: read the map from file
with open(filename, "r") as file:
    lines = [list(line.strip()) for line in file.readlines()]

game_map = lines

# Step 3: find player and mushroom positions
player_x = player_y = 0
mushroom_x = mushroom_y = 0

for y in range(len(game_map)):
    for x in range(len(game_map[y])):
        if game_map[y][x] == "P":
            player_x, player_y = x, y
        elif game_map[y][x] == "M":
            mushroom_x, mushroom_y = x, y

print("\nUse W A S D to move toward the mushroom (M).")
print("Unlimited moves. Borders (#) block you.\n")

# Step 4: main game loop — runs until player reaches mushroom
while True:
    # print the map
    for row in game_map:
        print(" ".join(row))
    print()

    move = input("Move (W/A/S/D): ").lower()

    # remove old player symbol
    game_map[player_y][player_x] = "-"

    # compute new position
    new_x, new_y = player_x, player_y
    if move == "w":
        new_y -= 1
    elif move == "s":
        new_y += 1
    elif move == "a":
        new_x -= 1
    elif move == "d":
        new_x += 1
    else:
        print("Invalid key!\n")
        new_x, new_y = player_x, player_y

    # check if hitting wall
    if game_map[new_y][new_x] == "#":
        print("You hit a wall!\n")
        new_x, new_y = player_x, player_y

    # update player position
    player_x, player_y = new_x, new_y

    # check if mushroom found
    if player_x == mushroom_x and player_y == mushroom_y:
        game_map[player_y][player_x] = "P"
        for row in game_map:
            print(" ".join(row))
        print("\nYou found the mushroom! 🍄 You win!")
        break

    # put player symbol back
    game_map[player_y][player_x] = "P"
