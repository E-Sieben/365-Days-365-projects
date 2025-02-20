
def show_file_size(path: str) -> str:
   from os import stat 
   o: int = stat(path).st_size
   match o:
      case _ if o < 1000:
         unit = "bytes"
      case _ if o < 1_000_000:
         o /= 1_000
         unit = "KB"
      case _:
         o /= 1_000_000
         unit = "MB"
   return f"{o:.2f} {unit}"

print(show_file_size("January/README.md"))