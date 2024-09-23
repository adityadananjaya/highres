import subprocess
import sys
import os

'''
Command line arguments are python programs you want to run pylint against or given directories
Outputs are dumped into text files
'''

# Add all valid files here
checked_directories = []
checked_files = []

for file in sys.argv[1:]:
    # Check if given file is a directory
    if os.path.isdir(file):
        checked_directories.append(file)
        continue

    # Check if given file is a python file
    if len(file) < 3 or file[-3:] != '.py':
        print(f'\n{file} is not a valid Python file\n')
    else:
        checked_files.append(file)


# Create directory to dump text files in
if len(checked_directories) > 0 or len(checked_directories) > 0:
    try:
        os.mkdir("pylint_output_dump")
    except FileExistsError:
        pass
else:
    print("Nothing to run pylint against.")
    sys.exit()

# Run pylint against directories
if len(checked_directories) > 0:
    for dir in checked_directories:
        command = f'pylint {dir}'
        text_dump_dest = './pylint_output_dump/' + dir + '_pylint_dump.txt'
        with open(text_dump_dest, 'w') as f:
            process = subprocess.run(command, stdout = f, shell=True)

# Run pylint on files
if len(checked_files) > 0:
    command = f'pylint {" ".join(checked_files)}'
    text_dump_dest = './pylint_output_dump/individual_files_pylint_dump.txt'
    with open(text_dump_dest, 'w') as f:
        process = subprocess.run(command, stdout = f, shell=True)