import os

def read_file(path):
    if os.path.isfile(path):
        with open(path, 'r') as file:
            data = file.read()
    else:
        with open(path, 'w') as file:
            file.write('0')
        data = '0'
    return data

def write_data(path, data):
    with open(path, 'w') as file:
        file.write(str(data))
