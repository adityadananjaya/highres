import label_convertor
import sys
import traceback

# Check if user provided valid number of command-line arguments
if (len(sys.argv) != 3):
    print("Insufficient Number of Arguments")
    sys.exit()

if (sys.argv[1] == 'yolotxt_to_voc'): # From Yolo labels to VOC labels
        try: # Error handling
            outputs = label_convertor.yolotxt_to_voc(sys.argv[2])
            print(outputs)
        except OSError as e:
            print(traceback.print_exc())

# Print error message if invalid command-line arguments
else:
    print("Invalid Arguments")