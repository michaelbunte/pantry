import re
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
        get_date_obj(second_string)
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
    output_path = "./"
    group_names = ["fridge", "frozen", "shopping list"]
    output_file_name = "inputfile.txt"
    input_text_arr = file_to_array(output_path + output_file_name)
    groups = separate(input_text_arr)
    print(groups)

    for group_name in group_names:
        entries = groups[group_name]
        


      
main()