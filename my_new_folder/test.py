# shroom_game.py
import os
import sys
import argparse
import platform

# Cross-platform single-key reader
if platform.system() == "Windows":
    import msvcrt

    def getkey():
        return msvcrt.getwch().lower()
else:
    import tty
    import termios

    def getkey():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            return ch.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

# Small utilities
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def load_map_from_text(text):
    return [list(line.rstrip("\n")) for line in text.splitlines()]

def find_player(game_map):
    for y, row in enumerate(game_map):
        for x, ch in enumerate(row):
            if ch == "P":
                return x, y
    return None

def print_map_with_player(game_map, px, py):
    for y, row in enumerate(game_map):
        line = ""
        for x, ch in enumerate(row):
            if x == px and y == py:
                line += "P"
            else:
                line += ch
        print(line)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def main():
    parser = argparse.ArgumentParser(description="Tiny Shroom-like mover")
    parser.add_argument("stage", nargs="?", help="Optional stage file (text)")
    args = parser.parse_args()

    default_stage = """\
....T....
..M...T..
...P.....
....T....
........."""
    if args.stage:
        try:
            with open(args.stage, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print("Failed to read stage file:", e)
            return
    else:
        text = default_stage

    game_map = load_map_from_text(text)
    pos = find_player(game_map)
    if pos:
        px, py = pos
        # remove original 'P' in map so we draw player separately
        game_map[py][px] = "."
    else:
        # if not found, start at top-left
        px, py = 0, 0

    instructions = "W/A/S/D to move, q to quit. Trees (T) block movement. M = mushroom (can be collected)."

    collected = 0
    while True:
        clear_screen()
        print(instructions)
        print()
        print_map_with_player(game_map, px, py)
        print()
        print(f"Collected mushrooms: {collected}")
        print("Press a key...")

        key = getkey()
        if key == "q":
            print("Quitting. Bye!")
            break
        dx = dy = 0
        if key == "w":
            dy = -1
        elif key == "s":
            dy = 1
        elif key == "a":
            dx = -1
        elif key == "d":
            dx = 1
        else:
            # ignore other keys
            continue

        nx = clamp(px + dx, 0, len(game_map[0]) - 1)
        ny = clamp(py + dy, 0, len(game_map) - 1)

        target = game_map[ny][nx]
        if target == "T":
            # blocked by tree
            continue
        elif target == "M":
            collected += 1
            game_map[ny][nx] = "."  # remove mushroom after collecting

        # move player
        px, py = nx, ny

if __name__ == "__main__":
    main()
