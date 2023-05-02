import os

def get_python_files(path):
    python_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


def get_source_and_test_files(path):
    test_dict = {}
    source_dict = {}
    python_files = get_python_files(path)

    for file_path in python_files:
        file_name = file_path.split('/')[-1]
        if file_name.startswith('test_'):
            test_dict[file_name[5:]] = file_path
    print(len(test_dict))
    for k,v in test_dict.items():
        print(k,v)

    source_files = list(test_dict.keys())
    print(source_files)

    for file_path in python_files:
        print(file_path.split('/')[-1])
        if file_path.split('/')[-1] in source_files:
            source_dict[file_path.split('/')[-1]] = file_path
    
    print('YOLO')
    print(len(source_dict))
    for k,v in source_dict.items():
        print(k,v)

    return source_dict, test_dict

x,y = get_source_and_test_files('/Users/yashdamania/Downloads/theano/')




