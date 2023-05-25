import os

# folder path

# list to store files
def get_files_in_dir(dir_path, endwith='.pdf'):
    # dir_path = os.getcwd()
    print(dir_path)
    res = []

    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            if path.endswith(endwith):
                res.append(path)
    # print(res)
    return res

if __name__=="__main__":
    print(get_files_in_dir(os.getcwd(), '.pdf'))