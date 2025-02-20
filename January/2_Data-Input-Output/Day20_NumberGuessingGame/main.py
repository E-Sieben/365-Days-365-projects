from random import randint

def start_game(min: int, max: int) -> bool:
   inp: int = input(f"Guess the number between {min} and {max}: ")
   num: int = randint(min, max)
   if int(inp) == num:
      print(f"You've won! The Number really was {num}")
      return True
   print(f"You've lost! The Number was {num}")
   return False

start_game(0, 1)