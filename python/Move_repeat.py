import os
import shutil
import random
import string

list_1 = []
list_2 = []
repeated = []

def repeat_verify():
    count = 0
    for num, item_1 in enumerate(list_1):
        for item_2 in list_2:
            if item_1[0] == item_2[0]:
                repeated.append([item_1[1], item_2[1], item_1[0], item_2[0]])
                count += 1
    print("\n" * 20)
    print(f"\n\n TOTAL === {count} ===\n")
    print(f"--= Directory {dir_1} Contains == {len(list_1)} == items =--\n")
    print(f"--= Directory {dir_2} Contains == {len(list_2)} == items =--")

def add_to_list(directory, num):
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            item_name = item_path.split("\\")[-1]
            if num == 1:
                list_1.append([item_name, item_path])
            elif num == 2:
                list_2.append([item_name, item_path])
    except PermissionError as e:
        return
    except Exception as e:
        return

def generate_random_folder_name():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def move_files_random_folder():
    random_folder_name = generate_random_folder_name()
    destination_dir = os.path.join("C:\\TESTE\\Repetidos", random_folder_name)
    os.makedirs(destination_dir, exist_ok=True)
    for item in repeated:
        source_path = item[0]
        destination_path = os.path.join(destination_dir, os.path.basename(source_path))
        try:
            shutil.move(source_path, destination_path)
            print(f"Moved: {source_path} -> {destination_path}")
        except Exception as e:
            print(f"Error moving {source_path} to {destination_path}: {e}")

dir_1 = "C:\\Users\\CLIENTE\\Downloads"
dir_2 = "E:\\"

add_to_list(dir_2, 2)
add_to_list(dir_1, 1)

for item in list_1:
    if "." not in item[0]:
        dir_1 = item[1]
        add_to_list(dir_1, 1)

for item in list_2:
    if "." not in item[0]:
        dir_2 = item[1]
        add_to_list(dir_2, 2)

repeat_verify()

# Move arquivos repetidos para uma pasta com nome aleatório
move_files_random_folder()

print(f"\n\n List 1 = {list_1}")
print(f"\n List 2 = {list_2}\n\n")
print(f"\n\n Repeated = {repeated}")

#python Verific_repeat.py
