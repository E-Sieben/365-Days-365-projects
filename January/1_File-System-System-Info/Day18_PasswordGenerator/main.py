def generate_password(l: int) -> str:
   '''
   It's basically Day 6
   '''
   from random import choice
   from string import printable
   print(printable)
   o = ""
   i = 0
   while i < l:
      o = o + choice(printable)
      i += 1
   return o

print(generate_password(16))