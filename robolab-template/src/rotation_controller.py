from planet import Direction, to_enum

def rotate_to_target(comeFrom, goTo):
    if type(goTo) != Direction:
        goTo = to_enum(goTo)

    if type(comeFrom) != Direction:
        comeFrom = to_enum(comeFrom)

    #amount_of_turns = 0

    if comeFrom == Direction.NORTH:
        if goTo == Direction.NORTH:
            amount_of_turns = 2
        elif goTo == Direction.EAST:
            amount_of_turns = 1
        elif goTo == Direction.SOUTH:
            amount_of_turns = 0
        elif goTo == Direction.WEST:
            amount_of_turns = -1
    elif comeFrom == Direction.EAST:
        if goTo == Direction.NORTH:
            amount_of_turns = -1
        elif goTo == Direction.EAST:
            amount_of_turns = 2
        elif goTo == Direction.SOUTH:
            amount_of_turns = 1
        elif goTo == Direction.WEST:
            amount_of_turns = 0
    elif comeFrom == Direction.SOUTH:
        if goTo == Direction.NORTH:
            amount_of_turns = 0
        elif goTo == Direction.EAST:
            amount_of_turns = -1
        elif goTo == Direction.SOUTH:
            amount_of_turns = 2
        elif goTo == Direction.WEST:
            amount_of_turns = 1
    elif comeFrom == Direction.WEST:
        if goTo == Direction.NORTH:
            amount_of_turns = 1
        elif goTo == Direction.EAST:
            amount_of_turns = 0
        elif goTo == Direction.SOUTH:
            amount_of_turns = -1
        elif goTo == Direction.WEST:
            amount_of_turns = 2
    else:
        print("Some special case appeared!")
        amount_of_turns = 0

    print("Amount of turns: ", amount_of_turns)
    return amount_of_turns