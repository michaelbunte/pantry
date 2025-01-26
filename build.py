import re
import json
from datetime import date

def extract_name(line):
    return line.split('#', 1)[0].strip()

def get_second_string(line):
    try:
        return line.split('#', 1)[1].strip()
    except:
        return None
    
def get_date_obj(date_string):
    date_arr = date_string.split("/")
    day = int(date_arr[0])
    month = int(date_arr[1])
    year = int(date_arr[2])
    return date(year, month, day)

def extract_date(line):
    second_string = get_second_string(line)
    if second_string is None:
        return None
    try:
        return get_date_obj(second_string)
    except:
        raise Exception()


def file_to_array(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def remove_equals(string):
    return re.sub(r"=", "", string).strip()

def separate(input_text_arr):
    groups = {}
    last_group = None
    for line in input_text_arr:

        # remove comments
        line = line.split(">")[0].strip()
        if len(line) == 0:
            continue

        elif line[0] == '=' and line[len(line) - 1] == '=':
            inner_text = remove_equals(line)
            groups[inner_text] = []
            last_group = inner_text
            continue

        if last_group is None:
            raise Exception()

        cleaned = line.strip()
        if len(cleaned) == 0:
            continue
        entry = {}
        entry["name"] = extract_name(cleaned)
        entry["date"] = extract_date(cleaned)
        groups[last_group].append(entry)
    return groups


def main():
    with open('config.json', 'r') as file:
        config_data = json.load(file)
    path = config_data["path"]
    group_names = config_data["group_names"]
    input_file_name = config_data["input_file_name"]
    output_file_name = config_data["output_file_name"]

    input_text_arr = file_to_array(path + input_file_name)
    groups = separate(input_text_arr)

    current_date = date.today()


    with open(path + output_file_name, "w") as file:
        for group_name in group_names:
            
            has_reached_not_expired = False
            has_reached_expired = False

            file.write("=" * 5 + " " + group_name + " " + "=" * 5 + "\n")
            entries = groups[group_name]
            sorted_entries = sorted(entries, key=lambda entry: entry["date"] if not (entry["date"] is None) else date(1000,1,1))

            for i in range(len(sorted_entries)):
                if not(sorted_entries[i]["date"] is None) and sorted_entries[i]["date"] < current_date and not has_reached_expired:
                    has_reached_expired = True
                    if i != 0:
                        file.write("\n")
                    file.write("EXPIRED\n")
                elif not(sorted_entries[i]["date"] is None) and sorted_entries[i]["date"] >= current_date and not has_reached_not_expired:
                    has_reached_not_expired = True
                    if i != 0:
                        file.write("\n")
                    file.write("FRESH\n")

                file.write(sorted_entries[i]["name"])
                if sorted_entries[i]["date"] is None:
                    file.write("\n")
                    continue

                file.write( " - " + sorted_entries[i]["date"].strftime("%d/%m/%Y") + "\n")

            file.write("\n")
    

      
main()