import json
import urllib.request
import os
import shutil


url = "https://raw.githubusercontent.com/titaniummachine1/Api_Snippet_Hub/main/Lua_Database.json"
filename = "database.json"


def download_database():
    if not os.path.exists(filename) or "new_data" in json.load(open(filename)):
        print("Downloading database...")
        with urllib.request.urlopen(url) as response:
            data = response.read()
            with open(filename, "wb") as file:
                file.write(data)
            print("Database downloaded successfully!")
            with open(filename, "r") as file:
                data = json.load(file)
            if "new_data" in data:
                data["existing_data"].append(data["new_data"])
                del data["new_data"]
                with open(filename, "w") as file:
                    json.dump(data, file)
                print("Database updated successfully!")
            else:
                with open(filename, "r") as file:
                    data = json.load(file)
    else:
        with open(filename, "r") as file:
            data = json.load(file)

    tables = {}

    try:
        with open(filename, 'r') as f:
            tables = json.load(f)
    except FileNotFoundError:
        print("Error: file not found.")
    except json.JSONDecodeError:
        print("Error: invalid JSON format.")
    return tables


if __name__ == "__main__":
    tables = download_database()

    # remove __pycache__ directory
    shutil.rmtree("__pycache__")
