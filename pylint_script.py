import subprocess
import sys

'''
Command line arguments are python programs you want to run pylint against
'''

# Add all valid files here
checked_files = []

for python_file in sys.argv[1:]:
    # Check if given file is a python file
    if len(python_file) < 3 or python_file[-3:] != '.py':
        print(f'\n{python_file} is not a valid Python file\n')
    else:
        checked_files.append(python_file)

# Run pylint
command = f'pylint {" ".join(checked_files)}'
process = subprocess.run(command, shell=True)