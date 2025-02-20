
from os import rename

STD_PATH = "January/1_File-System-System-Info/Day19_FileExtensionChanger/test.txt"
def change_Extension(type: str = "", file_path: str = STD_PATH) -> None:
   dirPath = file_path.split("/")
   name = dirPath[-1].split(".")[0]
   dirPath.pop(-1)
   if type == "":
      rename(file_path, f"{"/".join(dirPath)}/{name}")
      return
   rename(file_path, f"{"/".join(dirPath)}/{name}.{type}")

change_Extension()