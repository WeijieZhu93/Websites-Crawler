import json
if __name__ == "__main__":
    f = open("websites_info.txt")
    line = f.readline()
    while line :
        json_to_python = json.loads(line)
        print(json_to_python)
        line = f.readline()
    f.close()