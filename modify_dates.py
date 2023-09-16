import os  # get all files within a folder, access PowerShell commands
import re
from datetime import datetime as dt

path = input("Please provide your directory: ")
files_list = os.listdir(path)
pattern_map = {r"(\d{4}.\d{2}.\d{2}) - (\d{2}.\d{2}.\d{2})": "%Y.%m.%d - %H.%M.%S",
               r"(\d{4}-\d{2}-\d{2})-(\d{2}-\d{2}-\d{2})": "%Y-%m-%d-%H-%M-%S",
               r"(\d{4}\d{2}\d{2})-(\d{2}\d{2}\d{2})": "%Y%m%d-%H%M%S"}

loading = 0
unmodified_files = []
for file in files_list:
    modified = False
    for pattern, dt_format in pattern_map.items():
        match = re.search(pattern, file)
        if match:
            datetime = dt.strptime(match[0], dt_format)
            try:
                os.system(f"powershell (Get-Item '{path}/{file}').CreationTime=('{datetime}')")  # creation attribute
                os.system(f"powershell (Get-Item '{path}/{file}').LastWriteTime=('{datetime}')")  # modified attribute
                modified = True
                break  # current file was successfully processed, so move onto next file
            except ValueError:
                pass  # try next pattern-format pair
    if not modified:
        loading += 1
        unmodified_files.append(file)
        print(f"Error: No date was found in <{file}>. Progress: {loading}/{len(files_list)}")
    else:
        loading += 1
        print(f"Attributes for <{file}> was successfully modified. Progress: {loading}/{len(files_list)}")

print("\nCould not change attributes for the following files: ")
for i in range(len(unmodified_files)):
    print(f"\t> {unmodified_files[i]}")
