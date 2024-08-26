import label_convertor
import sys

if (len(sys.argv) != 3):
    print("Insufficient Number of Arguments")
    sys.exit()

if (sys.argv[1] == 'yaml_to_voc'):
        try:
            label_convertor.yaml_to_voc(sys.argv[3])
        except(OSError):
            print("Directory does not exist")

else:
    print("Invalid Arguments")