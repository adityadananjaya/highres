#!/bin/bash

test_program=$(<valid_convertor_test.in)
cd .. 
eval "$test_program" > ./hf_labelling_test/valid_convertor_test.out
cd hf_labelling_test
diff valid_convertor_test.out valid_convertor_test.expected

if [ $? -eq 0 ]; then
    echo "Success!"
else
    echo "Fail"
fi

rm valid_convertor_test.out