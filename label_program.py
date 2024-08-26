import label_convertor
import sys

if (len(sys.argv) != 3):
    print("Insufficient Number of Arguments")

if (sys.argv[1] == 'yaml_to_voc'):
    try:
        label_convertor.yaml_to_voc(sys.argv[2])
    except(FileNotFoundError):
        print("Labels does not exist")

else:
    print("Invalid Arguments")