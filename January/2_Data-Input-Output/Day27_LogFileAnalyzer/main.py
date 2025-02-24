STD_PATH: str = "January/2_Data-Input-Output/Day27_LogFileAnalyzer/server.log"

def read_log(file_path: str = STD_PATH) -> list[dict[str, str]]:
    o: list[dict[str, str]] = []
    with open(file_path, "r") as file:
        for line in file:
            if line == "" or line == None:
                pass
            line = line.split(" ")
            o.append(
                {
                    "Date": line[0],
                    "Time": line[1],
                    "Level": line[2].replace(":", ""),
                    "Message": " ".join(line[3:]).replace("\n", "")
                }
            )
    return o

logs = read_log()
for log in logs:
    print(log)