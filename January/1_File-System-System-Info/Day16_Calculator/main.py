def calc(expr: str) -> float:
   try:
      return eval(expr)
   except:
      return None
   
print(calc("3 + 3 * 2"))
print(calc("(3 + 3) * 2"))
print(calc("(3 + 3) / 2.3"))
