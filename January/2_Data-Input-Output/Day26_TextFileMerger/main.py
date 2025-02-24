STD_DEST: str = "January/2_Data-Input-Output/Day26_TextFileMerger/merge.txt"
STD_ONE: str = "January/2_Data-Input-Output/Day26_TextFileMerger/test1.txt"
STD_TWO: str = "January/2_Data-Input-Output/Day26_TextFileMerger/test2.txt"

def merge_text(file_path_one: str, file_path_two: str, dest_file_path: str = STD_DEST) -> None:
    Output: str = f""
    with open(file_path_one, "r") as file:
        Output += f"".join(file.read())
    Output += f"\n"
    with open(file_path_two, "r") as file:
        Output += f"".join(file.read())
    with open(dest_file_path, "w") as file:
        file.write(Output)

print(merge_text(STD_ONE, STD_TWO))