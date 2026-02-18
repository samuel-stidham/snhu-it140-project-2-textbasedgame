"""
Author: Samuel Stidham
Date: 2026-02-14
7-3 Project Two

Deep-sea survival-horror text adventure.
Collect all 6 components before entering the Reactor Core (villain room).
"""

from typing import Optional, Tuple, Union, Dict, List


# ---------- Game Data ----------
RoomsDict = Dict[str, Dict[str, Union[str, Dict[str, str]]]]

REQUIRED_ITEM_COUNT = 6
VILLAIN_ROOM = "Reactor Core"

rooms: RoomsDict = {
    "Airlock": {
        "North": "Hydroponics Lab",
        "South": "Communications Center",
        "West": "Observation Deck",
        "East": {
            "Medical": "Medical Bay",
            "Engineering": "Engineering Bay",
        },
    },
    "Storage Room": {"South": "Observation Deck", "East": "Hydroponics Lab"},
    "Hydroponics Lab": {
        "South": "Airlock",
        "East": "Crew Quarters",
        "West": "Storage Room",
    },
    "Crew Quarters": {"West": "Hydroponics Lab"},
    "Observation Deck": {
        "North": "Storage Room",
        "South": "Bio-Research Wing",
        "East": "Airlock",
    },
    "Medical Bay": {"South": "Engineering Bay", "West": "Airlock"},
    "Engineering Bay": {"North": "Medical Bay", "West": "Airlock"},
    "Bio-Research Wing": {
        "North": "Observation Deck", 
        "East": "Communications Center"
    },
    "Communications Center": {
        "North": "Airlock",
        "West": "Bio-Research Wing",
        "East": "Reactor Core",
    },
    "Reactor Core": {"West": "Communications Center"},
}

# One item per room (except start and villain room)
room_items: Dict[str, Optional[str]] = {
    "Airlock": None,
    "Storage Room": "Pressure Sealant",
    "Hydroponics Lab": "Oxygen Tank",
    "Crew Quarters": "Data Decryptor",
    "Observation Deck": None,
    "Medical Bay": None,
    "Engineering Bay": "Thermal Battery",
    "Bio-Research Wing": "Encrypted Keycard",
    "Communications Center": "Signal Flare",
    "Reactor Core": None,
}


# ---------- UI / Output ----------
def show_instructions() -> None:
    """Print the game title, objective, and available commands.

    This is a simple user-facing help display shown at game start.
    """
    print("Aurelia: Deep-Sea Text Adventure")
    print(f"Collect {REQUIRED_ITEM_COUNT} items to repair your escape pod.")
    print(f"Avoid the {VILLAIN_ROOM} until you're fully prepared.\n")
    print("Commands:")
    print("  go North | go South | go East | go West")
    print("  get <item name>")
    print("  look  (shows exits)")
    print("  exit  (quit the game)\n")


def show_status(current_room: str, inventory: List[str]) -> None:
    """Display the player's current room, inventory, and visible item.

    Args:
        current_room: Name of the room the player is in.
        inventory: List of collected item names.
    """
    print("\n----------------------")
    print(f"You are in the {current_room}")
    print(f"Inventory: {inventory}")

    item = room_items.get(current_room)
    if item:
        print(f"You see a {item}")
    print("----------------------")


def show_exits(current_room: str) -> None:
    """Print the available movement directions from the given room.

    Shows branching options when a direction maps to multiple destinations.
    """
    exits = rooms[current_room]
    pretty: List[str] = []
    for direction, dest in exits.items():
        if isinstance(dest, dict):
            options = ", ".join(dest.keys())
            pretty.append(f"{direction} ({options})")
        else:
            pretty.append(direction)
    print(f"Available directions: {', '.join(pretty)}")


# ---------- Parsing / Helpers ----------
def normalize_tokens(tokens: List[str]) -> List[str]:
    """Strip whitespace and lowercase tokens, filtering out empty strings.

    Args:
        tokens: Sequence of string tokens to normalize.

    Returns:
        A new list of cleaned, lowercase tokens.
    """
    return [t.strip().lower() for t in tokens if t.strip()]


def title_word(s: str) -> str:
    """Return a string with the first character uppercase and the rest
    lowercase.

    This is similar to `str.capitalize()` but preserves empty-string behavior.
    """
    return s[:1].upper() + s[1:].lower() if s else s


def parse_go(raw: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Returns (direction, qualifier)
    Examples:
      "go east" -> ("East", None)
      "go east medical" -> ("East", "Medical")
    """
    parts = normalize_tokens(raw.split())
    if not parts:
        return None, None

    if parts[0] == "go":
        parts = parts[1:]

    if not parts:
        return None, None

    direction = title_word(parts[0])
    qualifier = title_word(parts[1]) if len(parts) > 1 else None
    return direction, qualifier


def parse_get_item(raw: str) -> Optional[str]:
    """
    Returns the requested item string (original spacing preserved as
    title-case-ish), or None if not a valid get command.
    """
    raw = raw.strip()
    if not raw:
        return None

    parts = raw.split()
    if parts[0].lower() != "get":
        return None

    if len(parts) < 2:
        return ""

    # Keep the rest as typed; compare case-insensitively later
    return " ".join(parts[1:]).strip()


#
def same_item(a: str, b: str) -> bool:
    """Compare two item names for equality in a case-insensitive way.

    Leading/trailing whitespace is ignored.
    """
    return a.strip().lower() == b.strip().lower()


# ---------- Game Loop ----------
def main() -> None:
    """Run the main game loop handling input, movement, and item pickup.

    The loop prints status, processes commands, and detects win/lose states.
    """
    show_instructions()

    current_room = "Airlock"
    inventory: List[str] = []

    while True:
        show_status(current_room, inventory)

        # Win/lose trigger occurs when entering the villain room
        if current_room == VILLAIN_ROOM:
            if len(inventory) >= REQUIRED_ITEM_COUNT:
                print(
                    "You repaired the pod systems and slipped past the "
                    "Leviathan. You win!"
                )
            else:
                print(
                    "The Leviathan emerges from the shadows. You have been "
                    "consumed. GAME OVER."
                )
            print("Thanks for playing.")
            break

        raw_input = input("Enter your move: ").strip()
        if not raw_input:
            continue

        cmd = raw_input.split()[0].lower()

        if cmd == "exit":
            print("You abort the dive and retreat. Thanks for playing.")
            break

        if cmd == "look":
            show_exits(current_room)
            continue

        # Handle get command
        requested = parse_get_item(raw_input)
        if requested is not None:
            if requested == "":
                print("Invalid command. Use: get <item name>")
                continue

            item_here = room_items.get(current_room)
            if not item_here:
                print("There is no item to collect here.")
                continue

            if same_item(requested, item_here):
                inventory.append(item_here)
                # remove item from room after pickup
                room_items[current_room] = None
                print(f"You picked up the {item_here}.")
            else:
                print(f'You cannot get "{requested}" here.')
            continue

        # Handle movement
        direction, qualifier = parse_go(raw_input)
        if direction is None:
            print('Invalid command. Use "go <direction>" or '
                  '"get <item name>".')
            continue

        exits = rooms[current_room]
        if direction not in exits:
            print(f'Invalid direction: "{direction}". '
                  'Type "look" to see valid exits.')
            continue

        dest = exits[direction]

        # Branching East from Airlock (or any room with a dict destination)
        if isinstance(dest, dict):
            if qualifier is None:
                options = ", ".join(dest.keys())
                print(f"{direction} is ambiguous. Choose one: {options}.")
                print(f"Use: go {direction} <option>")
                continue

            if qualifier not in dest:
                options = ", ".join(dest.keys())
                print(
                    f'Invalid option for {direction}: "{qualifier}". '
                    f'Choose one: {options}.'
                )
                continue

            current_room = dest[qualifier]
        else:
            current_room = dest


if __name__ == "__main__":
    main()
