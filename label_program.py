import label_convertor
import sys
import traceback

if (len(sys.argv) != 3):
    print("Insufficient Number of Arguments")
    sys.exit()

if (sys.argv[1] == 'yolotxt_to_voc'):
        try:
            outputs = label_convertor.yolotxt_to_voc(sys.argv[2])
            print(outputs)
        except OSError as e:
            print(traceback.print_exc())

else:
    print("Invalid Arguments")