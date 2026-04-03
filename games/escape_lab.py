# Escape the Lab - A Text Adventure by Jules (2026)

import sys

# Game Data
ROOMS = {
    "Lab": {
        "description": "You are in a sterile, high-tech lab. Fluorescent lights hum above. Experimental parts are scattered on benches.",
        "exits": {"north": "Storage", "east": "Security"},
        "items": ["screwdriver"]
    },
    "Storage": {
        "description": "A dark room filled with crates and robotic chassis. It smells of ozone and machine oil.",
        "exits": {"south": "Lab"},
        "items": ["battery_pack"]
    },
    "Security": {
        "description": "The security station for the facility. Monitors show various parts of the lab. The main exit is here, but it's locked.",
        "exits": {"west": "Lab"},
        "items": ["keycard"]
    }
}

class GameState:
    def __init__(self):
        self.current_room = "Lab"
        self.inventory = []
        self.is_running = True
        self.door_locked = True

def print_help():
    print("\nCommands:")
    print("  look        - Look around the current room")
    print("  go <dir>    - Move in a direction (north, south, east, west)")
    print("  take <item> - Pick up an item")
    print("  use <item>  - Use an item from your inventory")
    print("  inventory   - Show your current inventory")
    print("  help        - Show this help message")
    print("  quit        - Exit the game")

def main():
    state = GameState()

    print("Welcome to 'Escape the Lab' (2026 Edition)")
    print("Find a way to unlock the security door and escape!")
    print_help()

    while state.is_running:
        print(f"\n--- {state.current_room} ---")
        try:
            command_input = input("> ").lower().strip().split()
        except EOFError:
            break

        if not command_input:
            continue

        action = command_input[0]
        args = command_input[1:]

        if action == "quit":
            state.is_running = False
            print("Thanks for playing!")

        elif action == "help":
            print_help()

        elif action == "look":
            room = ROOMS[state.current_room]
            print(room["description"])
            exits = ", ".join(room["exits"].keys())
            print(f"Exits: {exits}")
            if room["items"]:
                items = ", ".join(room["items"])
                print(f"Items here: {items}")

        elif action == "inventory":
            if state.inventory:
                print(f"Inventory: {', '.join(state.inventory)}")
            else:
                print("Your inventory is empty.")

        elif action == "go":
            if not args:
                print("Go where? (e.g., go north)")
                continue

            direction = args[0]
            room = ROOMS[state.current_room]

            # Special logic for the locked exit in Security
            if state.current_room == "Security" and direction == "east":
                if state.door_locked:
                    print("The door is locked! You need to use a keycard.")
                else:
                    print("You push through the heavy doors and escape into the sunlight!")
                    print("CONGRATULATIONS! YOU ESCAPED!")
                    state.is_running = False
                continue

            if direction in room["exits"]:
                next_room = room["exits"][direction]
                state.current_room = next_room
            else:
                print(f"You can't go {direction} from here.")

        elif action == "take":
            if not args:
                print("Take what?")
                continue

            item = args[0]
            room = ROOMS[state.current_room]

            if item in room["items"]:
                room["items"].remove(item)
                state.inventory.append(item)
                print(f"You picked up the {item}.")
            else:
                print(f"There is no {item} here.")

        elif action == "use":
            if not args:
                print("Use what?")
                continue

            item = args[0]
            if item not in state.inventory:
                print(f"You don't have a {item}.")
                continue

            if item == "keycard" and state.current_room == "Security":
                state.door_locked = False
                print("You swipe the keycard. The security door's light turns green. You can now go east to escape!")
            else:
                print(f"Using the {item} doesn't seem to do anything here.")

        else:
            print(f"Unknown command: {action}")

if __name__ == "__main__":
    main()
