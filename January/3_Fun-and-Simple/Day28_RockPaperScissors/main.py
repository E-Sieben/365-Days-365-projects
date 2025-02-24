from random import randint

def eval(human_move: int, cpu_move: int) -> bool:
    """
    Evaluates who won in Rock, Paper, Scissors.
    Params:
        human_move (int): 0 for Rock, 1 for Paper, 2 for Scissors.
        cpu_move (int): 0 for Rock, 1 for Paper, 2 for Scissors.
    Return:
        bool: True if the human won, False if not, None if draw.
    """
    match (human_move, cpu_move):
        case (0, 2):
            return True
        case (1, 0):
            return True
        case (2, 1):
            return True
        case (x, y) if x == y:
            return
        case _:
            return False

def get_human_move() -> int:
    "Take a user Input and give out in Number form"
    inp: str = input("Please use \"Rock\", \"Paper\" or \"Scissor\"\n").lower()
    match inp[0]:
        case "r":
            return 0
        case "p":
            return 1
        case "s":
            return 2
        case _:
            print("Please give a proper answer: Rock/Paper/Scissor")
            return get_human_move()
        
def get_impossible_move(human_move: int) -> int:
    "Take a move and output the winning move"
    human_move += 1
    return human_move if human_move != 3 else 0

def get_cpu_move() -> int:
    "Pick a random number from 0-2"
    return randint(0, 2)

def make_move_readable(move: int) -> str:
    """
    Converts normal move to readable form
    Params:
        move (int): the move to be converted in it's integer form
    Return:
        str: the given move in human readable form
    """
    match move:
        case 0:
            return "Rock"
        case 1:
            return "Paper"
        case 2:
            return "Scissor"
        case _:
            raise ValueError("Not a valid move")

def start_rpc(impossible_difficulty: bool = False) -> None:
    """
    Starts the Rock Paper Scissors game.
    The game continues until the user interrupts it with a KeyboardInterrupt.
    In each round, the user is prompted to enter their move, and the computer
    makes a move. The outcome of the round is then printed to the console.
    Args:
        impossible_difficulty (bool, optional): If True, the computer will
            always choose the move that wins against the human player.
            Defaults to False.
    Returns:
        None: The function does not return any value.  It prints the game
            results to the console.
    Raises:
        KeyboardInterrupt: If the user interrupts the game.
    """
    
    try:
        while True:
            human_move: int = get_human_move()
            if impossible_difficulty:
                cpu_move: int = get_impossible_move(human_move)
            else:
                cpu_move: int = get_cpu_move()
            print(f"You picked: {make_move_readable(human_move)}")
            print(f"It picked:  {make_move_readable(cpu_move)}")
            outcome: bool = eval(human_move, cpu_move)
            if outcome == None:
                print("I'm so sorry, but that's a tie")
            elif outcome:
                print("Congratulation! You won! ^^")
            else:
                print("Booo Looser, you lost!")
    except KeyboardInterrupt:
        print("Bye ^^ <3")
        return

start_rpc(True)