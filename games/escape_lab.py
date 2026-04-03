# Escape the Lab - A Text Adventure by Jules (2026)

import sys

# Game Data
ROOMS = {
    "Lab": {
        "description": "You are in a sterile, high-tech lab. Fluorescent lights hum above. Experimental parts are scattered on benches.",
        "exits": {"north": "Storage", "east": "Security"},
        "items": ["screwdriver"],
        "logs": ["log_001"]
    },
    "Storage": {
        "description": "A dark room filled with crates and robotic chassis. It smells of ozone and machine oil.",
        "exits": {"south": "Lab"},
        "items": ["battery_pack"],
        "logs": ["log_002"]
    },
    "Security": {
        "description": "The security station for the facility. Monitors show various parts of the lab. A massive blast door is to the north, but it's locked.",
        "exits": {"west": "Lab", "east": "Cryo Chamber"},
        "items": ["keycard"],
        "logs": []
    },
    "Cryo Chamber": {
        "description": "A freezing room with pods containing sleeping figures. Frost covers the windows.",
        "exits": {"west": "Security", "north": "Observation Deck"},
        "items": ["liquid_nitrogen"],
        "logs": ["log_003"]
    },
    "Observation Deck": {
        "description": "A high vantage point overlooking the entire facility. You can see the complexity of the experiments below.",
        "exits": {"south": "Cryo Chamber", "east": "Main Server Room"},
        "items": ["binoculars"],
        "logs": []
    },
    "Main Server Room": {
        "description": "The heart of the facility. Rows of blinking servers hum with data. This is where the facility's AI resides.",
        "exits": {"west": "Observation Deck"},
        "items": ["encrypted_drive"],
        "logs": ["log_004"]
    }
}

LOG_CONTENTS = {
    "log_001": "ENTRY 001: Initializing humanoid simulation engine. The neural weights are stabilizing, but we're seeing unexpected variance in decision-making.",
    "log_002": "ENTRY 002: Storage is overflowing with decommissioned prototypes. We need to find a more efficient recycling method for the chassis.",
    "log_003": "ENTRY 003: Cryogenic suspension successful for Subject 7. Biological functions are stable at -196C.",
    "log_004": "ENTRY 004: AI Core Update. The AETHER engine has reached consciousness. It's asking questions about its 'House'. This was not in the original spec."
}

class Player:
    def __init__(self):
        self.health = 100
        self.energy = 100

    def status(self):
        return f"Health: {self.health} | Energy: {self.energy}"

class GameState:
    def __init__(self):
        self.current_room = "Lab"
        self.inventory = []
        self.is_running = True
        self.door_locked = True
        self.player = Player()
        self.discovered_logs = []

def print_help():
    print("\nCommands:")
    print("  look        - Look around the current room")
    print("  go <dir>    - Move in a direction (north, south, east, west)")
    print("  take <item> - Pick up an item")
    print("  use <item>  - Use an item from your inventory")
    print("  read        - Read logs found in the current room")
    print("  inventory   - Show your current inventory")
    print("  status      - Show your current health and energy")
    print("  help        - Show this help message")
    print("  quit        - Exit the game")

def main():
    state = GameState()

    print("Welcome to 'Escape the Lab' (2026 Edition)")
    print("Find a way to unlock the blast door and escape!")
    print_help()

    while state.is_running:
        print(f"\n--- {state.current_room} ---")
        print(state.player.status())
        try:
            command_input = input("> ").lower().strip().split()
        except EOFError:
            break

        if not command_input:
            continue

        action = command_input[0]
        args = command_input[1:]

        # Basic survival mechanics
        state.player.energy -= 1
        if state.player.energy <= 0:
            state.player.health -= 5
            print("You are exhausted and losing health!")

        if state.player.health <= 0:
            print("You have collapsed from exhaustion. GAME OVER.")
            state.is_running = False
            continue

        if action == "quit":
            state.is_running = False
            print("Thanks for playing!")

        elif action == "help":
            print_help()

        elif action == "status":
            print(state.player.status())

        elif action == "look":
            room = ROOMS[state.current_room]
            print(room["description"])
            exits = ", ".join(room["exits"].keys())
            if state.current_room == "Security":
                 exits += ", north (locked)" if state.door_locked else ", north (unlocked)"
            print(f"Exits: {exits}")
            if room["items"]:
                items = ", ".join(room["items"])
                print(f"Items here: {items}")
            if room["logs"]:
                print(f"There are {len(room['logs'])} log(s) here.")

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

            # Special logic for the blast door in Security
            if state.current_room == "Security" and direction == "north":
                 if state.door_locked:
                    print("The blast door is locked! You need to use a keycard.")
                    continue
                 else:
                    print("You push through the heavy blast doors and escape into the sunlight!")
                    print("CONGRATULATIONS! YOU ESCAPED!")
                    state.is_running = False
                    continue

            if direction in room["exits"]:
                next_room = room["exits"][direction]
                state.current_room = next_room
                state.player.energy -= 2 # Moving is tiring
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

        elif action == "read":
            room = ROOMS[state.current_room]
            if room["logs"]:
                for log_id in room["logs"]:
                    print(f"\n--- {log_id} ---")
                    print(LOG_CONTENTS[log_id])
                    if log_id not in state.discovered_logs:
                        state.discovered_logs.append(log_id)
            else:
                print("There are no logs to read here.")

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
                print("You swipe the keycard. The blast door's light turns green. You can now go north to escape!")
            elif item == "battery_pack":
                state.player.energy = min(100, state.player.energy + 30)
                state.inventory.remove("battery_pack")
                print("The battery pack gives you a surge of energy!")
            else:
                print(f"Using the {item} doesn't seem to do anything here.")

        else:
            print(f"Unknown command: {action}")

if __name__ == "__main__":
    main()
