# importing required modules
import PyPDF2
from files_in_directory import get_files_in_dir
import os
import shutil
from configparser import ConfigParser

if os.path.exists(os.path.join(os.getcwd(),'config.ini')):
    print("config.ini okay")
else:
    print("")
    print("please create file config.ini :")
    print("[conf]")
    print("fullpath_ori_directory = ")
    print("fullpath_target_directory = ")
    print("")
    print("")
    input("Press anykey to Exit:")
    quit()
config = ConfigParser()
config.read('config.ini')

data_dir='data ori'
# ori_directory_fullpath = os.path.join(os.getcwd(), data_dir)
ori_directory_fullpath = config['conf']['fullpath_ori_directory']

# target_directory_fullpath = os.path.join(os.getcwd(),'targetdir')
target_directory_fullpath = config['conf']['fullpath_target_directory']
print(ori_directory_fullpath, target_directory_fullpath)
if not (os.path.isdir(ori_directory_fullpath) and target_directory_fullpath):
    print("")
    print("Please fill the config.ini with the correct directory")
    print("[conf]")
    print("fullpath_ori_directory = ")
    print("fullpath_target_directory = ")
    print("")
    print("")
    input("Press Enter to Exit:")
    quit()
    
temp_directory = os.path.join(os.getcwd(), 'temp')
# shutil.copytree(ori_directory_fullpath, temp_directory)

def check_or_create_directory(new_DIR):
    # target_dir = os.path.join(target_directory_fullpath, folder, new_DIR)
    # print(target_dir)
    CHECK_FOLDER = os.path.isdir(new_DIR)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(new_DIR)
        print(f"created folder : {new_DIR}")
        return True
    else:
        print(f'Folder already exists=>{new_DIR}')
        return False
    
def copy_files_to_temp(oridir, tempdir, endwith='.pdf'):
    print("copy file to temp")

    _filelist = get_files_in_dir(ori_directory_fullpath, '.pdf')
    check_or_create_directory(temp_directory)
    print(_filelist)
    for file in _filelist:
        try:
            shutil.copy(os.path.join(oridir, file), os.path.join(tempdir, file))
        except Exception as e:
            print(f'file:{file} => {str(e)}')

copy_files_to_temp(ori_directory_fullpath, temp_directory)
filelist = get_files_in_dir(temp_directory, '.pdf')
# print(get_files_in_dir('.pdf'))



def read_pdf(filename):
    # # creating a pdf file object
    pdfFileObj = filename
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # printing number of pages in pdf file
    # print(pdfReader.numPages)
    tot_pages=len(pdfReader.pages)
    print(f'total pages={tot_pages}')
    reader_splited=[]
    for i in range(tot_pages):
        # creating a page object
        # pageObj = pdfReader.getPage(0)
        pageObj = pdfReader.pages[i]

        # extracting text from page
        # print(pageObj.extract_text())
        reader_splited+=pageObj.extract_text().split('\n')\

    # print(reader_splited)
    pdfFileObj=None
    return reader_splited

def get_data_from(data, str, j=1):
    i=0
    bolfound=False
    for i, x in enumerate(data):
        if str in x:
            # print(f'ada {str} di index {i}')
            bolfound=True
            break
    if bolfound:
        # print(data[i+j])
        return data[i+j]
    else:
        print(f"Cannot Found:{str}")
        return None

def get_pdfname_foldername_tosave(filename, str='Gondo Kusumo', j=1):
    filename_fullpath = os.path.join(temp_directory, filename)
    splited = read_pdf(filename_fullpath)
    str ='Penerima Jasa Kena Pajak'
    # print(get_data_from(splited, str))

    nama_wajib_pajak=get_data_from(splited, str)
    if nama_wajib_pajak:
        nama_wajib_pajak = nama_wajib_pajak.split(':')[1].strip()
    # print(nama_wajib_pajak)
    city_date= get_data_from(splited, 'pada Faktur Pajak ini.', j).strip()
    # inv_no = get_data_from(splited, str, j)
    inv_no = get_data_from(splited, 'pada Faktur Pajak ini.' , 3)
    inv_no =inv_no.replace('.', '_').replace(':', '_')
    # print(inv_no)
    # print(f'city={city_date}')
    city=city_date.split(',')[0].strip()
    date=city_date.split(',')[1].strip()
    datadict={filename: [inv_no, nama_wajib_pajak, city, date]}
    return datadict

def get_data_list(filelist):
    datalist=[]
    for filename in filelist:
        # print(filename)
        datalist.append(get_pdfname_foldername_tosave(filename))
    print(f'datalist={datalist}')
    return datalist

def get_value_for_filename(filename, datalist):
    for data in datalist:
        for key,val in data.items():
            # print(f'key={key}, val={ val}')
            if filename == key:
                return val

# keys = list(str(*my_dict) for my_dict in datalist)
# print (type(keys))



datalist=get_data_list(filelist)
folder = 'result'
success_count=0
fail_count=0
print("")
print("processing one file at a time:")
for filename in filelist:
    # print(f'filename={filename} => {get_value_for_filename(filename,get_data_list(filelist))}')
    values=get_value_for_filename(filename, datalist)
    # print(f'values in list={values}')

    new_filename = f'{values[0]}.pdf'
    new_cust_foldername = values[1].strip()
    new_city_foldername = values[2].split(' ')[-1].strip()
    new_year_foldername = values[3].split(' ')[-1].strip()
    print(new_filename, new_city_foldername, new_year_foldername, new_cust_foldername)
    if new_filename:
        old_name_fullpath= os.path.join(temp_directory, filename)
        new_filename_fullpath=os.path.join(temp_directory, new_filename)
        print(f'old_name_fullpath={old_name_fullpath}')
        print(f'new_filename_fullpath={new_filename_fullpath}')
        try:
            os.rename(old_name_fullpath, new_filename_fullpath) #rename to the original folder, not yet move or copy
            success_count+=1
        except Exception as e :
            print(str(e))
            fail_count+=1

        # copy/move to destination folder
        target_copy_folder_name=os.path.join(target_directory_fullpath, new_city_foldername, new_year_foldername, new_cust_foldername)
        # check_or_create_directory(folder, new_cust_foldername)
        check_or_create_directory(target_copy_folder_name)
        
        print(f'target folder fullpath={target_copy_folder_name}')
        target_copy_filename = os.path.join(target_copy_folder_name, new_filename)
        print(f'target filename fullpath={target_copy_filename}')
        shutil.copy(new_filename_fullpath, target_copy_filename)
    else:
        fail_count+=1
    print("")
#finish copy to temp folder and rename and copy to target folder, then delete the temp folder   
shutil.rmtree( temp_directory )
print("")
print("")
print("")
input(f"From {len(filelist)} PDF Files, SUCCESS={success_count}, Fail={fail_count}, Rename and Copy from '{ori_directory_fullpath}'  TO  '{target_directory_fullpath}'. Press the Enter key to Exit: ")
