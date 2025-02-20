def rename_file(path: str, name: str) -> None:
   from os import rename
   dirPath = path.split("/")
   dirPath.pop(-1)
   rename(path, f"{"/".join(dirPath)}/{name}")

rename_file("January/1_File-System-System-Info/Day11_FileRenamer/test.txt", "hi.txt")
