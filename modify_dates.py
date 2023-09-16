import os  # get all files within a folder, access PowerShell commands
import re
from datetime import datetime as dt

path = input("Please provide your directory: ")
files_list = os.listdir(path)
pattern = r"(\d{4}.\d{2}.\d{2}) - (\d{2}.\d{2}.\d{2})"

loading = 0
unmodified = []
for file in files_list:
    match = re.search(pattern, file)
    if match:
        datetime = dt.strptime(match[0], "%Y.%m.%d - %H.%M.%S")
    else:
        loading += 1
        unmodified.append(file)
        print(f"Error: No date was found in <{file}>. Progress: {loading}/{len(files_list)}")
        continue
    os.system(f"powershell (Get-Item '{path}/{file}').CreationTime=('{datetime}')")  # creation attribute
    os.system(f"powershell (Get-Item '{path}/{file}').LastWriteTime=('{datetime}')")  # modified attribute
    loading += 1
    print(f"Attributes for <{file}> was successfully modified. Progress: {loading}/{len(files_list)}")

print("\nCould not change attributes for the following files: ")
for i in range(len(unmodified)):
    print(f"\t> {unmodified[i]}")