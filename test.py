import os
import re
def replace_import_statement(original_file ,test_file, mutant_file,reverse = False):


    with open(test_file, 'r') as f:
        lines = f.readlines()
    with open(test_file, 'w') as f:
        for line in lines:
            if 'from ' in line or 'import' in line:
                if not reverse:
                    if original_file[:-3] in line :
                        line = line.replace(original_file[:-3],mutant_file)
                        print(line)
                else:
                    if mutant_file in line :
                        line = line.replace(mutant_file,original_file[:-3])
                        print(line)

            f.write(line)
    # f.close()

replace_import_statement('example2.py','example2-test.py','example2.mutant0',True)