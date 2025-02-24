from random import randint

def roll_dices(*args: int) -> int:
    """Rolls multiple dices and returns the sum of the results.
        Args:
            *args: Variable number of integers representing the number of sides for each dice.
                If no arguments are provided, it defaults to a single 6-sided dice.
        Returns:
            int: The sum of the results of rolling each dice.
        """

    if not args:
        args = (6,)
    sol: int = 0
    for k, i in enumerate(args):
        dice_throw = randint(0, i)
        sol += dice_throw
        print(f"Dice {k+1} rolled a {dice_throw}")
    return sol

print(f"The summed rolled number is: {roll_dices(0, 6, 12, 18, 24, 30)}")