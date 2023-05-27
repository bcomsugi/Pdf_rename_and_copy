# importing required modules
import PyPDF2
from files_in_directory import get_files_in_dir
import os
import shutil
from configparser import ConfigParser

if os.path.exists(os.path.join(os.getcwd(),'config.ini')):
    # print("config.ini okay")
    pass
else:
    print("")
    print("please create file config.ini :")
    print("[conf]")
    print("fullpath_ori_directory = ")
    print("fullpath_target_directory = ")
    # print("year_backup_folder = ")
    print("")
    print("")
    input("Press anykey to Exit:")
    quit()
config = ConfigParser()
config.read('config.ini')


data_dir='data ori'
# ori_directory_fullpath = os.path.join(os.getcwd(), data_dir)
ori_directory_fullpath = config['conf']['fullpath_ori_directory']
parent_ori_directory = os.path.dirname(ori_directory_fullpath)
# city_source = parent_ori_directory.split("\\")[-1].strip()
# print(city_source)
month_folder_list = {'Januari':'1. Jan Feb Mar',
                    'Februari':'1. Jan Feb Mar',
                    'Maret':'1. Jan Feb Mar',
                    'April':'2. Apr Mei Jun',
                    'Mei':'2. Apr Mei Jun',
                    'Juni':'2. Apr Mei Jun',
                    'Juli':'3. Jul Agu Sep',
                    'Agustus':'3. Jul Agu Sep',
                    'September':'3. Jul Agu Sep',
                    'Oktober':'4. Okt Nov Des',
                    'November':'4. Okt Nov Des',
                    'Desember':'4. Okt Nov Des', 
                    }
# if 'year_backup_folder' in config['conf']:
#     year_backup_folder = config.get('conf', 'year_backup_folder')
# else:
#     year_backup_folder=2051
# if not year_backup_folder:
#     year_backup_folder = '2050'
# # print(f'year_backup_folder={year_backup_folder}')
# target_directory_fullpath = os.path.join(os.getcwd(),'targetdir')
target_directory_fullpath = config['conf']['fullpath_target_directory']
print(f'Source Dir={ori_directory_fullpath}')
print(f'Target Dir={target_directory_fullpath}')
if not (os.path.isdir(ori_directory_fullpath) and target_directory_fullpath):
    print("")
    print("Please fill the config.ini with the correct directory")
    print("[conf]")
    print("fullpath_ori_directory = ")
    print("fullpath_target_directory = ")
    # print("year_backup_folder = ")
    print("")
    print("")
    input("Press Enter to Exit:")
    quit()
    
temp_directory = os.path.join(os.getcwd(), 'temp')
# shutil.copytree(ori_directory_fullpath, temp_directory)

def check_or_create_directory(new_DIR, debug=False):
    # print(target_dir)
    CHECK_FOLDER = os.path.isdir(new_DIR)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(new_DIR)
        if debug:
            print(f"   created folder : {new_DIR}")
        return True
    else:
        if debug:
            print(f'   Folder already exists=>{new_DIR}')
        return False
    
def copy_files_to_temp(oridir, tempdir, endwith='.pdf'):
    print("Copy file to temp Dir")

    _filelist = get_files_in_dir(ori_directory_fullpath, '.pdf')
    check_or_create_directory(temp_directory)
    print(_filelist)
    for file in _filelist:
        try:
            shutil.copy(os.path.join(oridir, file), os.path.join(tempdir, file))
        except Exception as e:
            print(f'file:{file} => {str(e)}')



def read_pdf(filename):
    # # creating a pdf file object
    pdfFileObj = filename
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # printing number of pages in pdf file
    # print(pdfReader.numPages)
    tot_pages=len(pdfReader.pages)
    # print(f'total pages={tot_pages}')
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
        nama_wajib_pajak = nama_wajib_pajak.split('NIK /')[0].strip()
    # print(nama_wajib_pajak)
    city_date= get_data_from(splited, 'pada Faktur Pajak ini.', j).strip()
    # inv_no = get_data_from(splited, str, j)
    inv_no = get_data_from(splited, 'pada Faktur Pajak ini.' , 3)
    inv_no =inv_no.replace('.', '_').replace(':', '_')
    # print(inv_no)
    # print(f'city={city_date}')
    city=city_date.split(',')[0].strip()
    date=city_date.split(',')[1].strip()
    # month=city_date.split(',')
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

def move_files_in_dir(sourcedir, targetdir, datalist, success_list):
    print(f'Moving ORI Files To BACKUP from {sourcedir} TO {targetdir}')
    for success_file in success_list:
        print(success_file)
        file = success_file[1].strip()
        month_backup_folder=success_file[5].strip()
        year_backup_folder=success_file[4].strip()

        targetdir=targetdir.replace('[year]',year_backup_folder)
        targetdir=targetdir.replace('[month]',month_backup_folder)
        check_or_create_directory(targetdir)
        print(f'targetdir={targetdir}', type(targetdir))
        shutil.copy(os.path.join(sourcedir, file), os.path.join(targetdir, file))
        os.remove(os.path.join(sourcedir, file))

    # for data in datalist:
    #     # print(data)
    #     for file, val in data.items():
    #         # print(f'file={file}, val={val}')
    #         month_backup_folder=val[3].split(' ')[-2].strip()
    #         year_backup_folder=val[3].split(' ')[-1].strip()
    #         targetdir=targetdir.replace('[year]',year_backup_folder)
    #         targetdir=targetdir.replace('[month]',month_backup_folder)
    #         check_or_create_directory(targetdir)
    #         # print(f'targetdir={targetdir}', type(targetdir))
    #         shutil.copy(os.path.join(sourcedir, file), os.path.join(targetdir, file))
    #         os.remove(os.path.join(sourcedir, file))

# keys = list(str(*my_dict) for my_dict in datalist)
# print (type(keys))

copy_files_to_temp(ori_directory_fullpath, temp_directory)
filelist = get_files_in_dir(temp_directory, '.pdf')

print("READING FILES and Get Datalist:")
datalist=get_data_list(filelist)
folder = 'result'
success_count=0
fail_count=0
fail_filelist=[]
success_filelist=[]
print("")
print("PROCESSING one file at a time:")
print("")

for idx, filename in enumerate(filelist):
    # print(f'filename={filename} => {get_value_for_filename(filename,get_data_list(filelist))}')
    values=get_value_for_filename(filename, datalist)
    # print(f'values in list={values}')

    new_filename = f'{values[0]}.pdf'
    new_cust_foldername = values[1].strip()
    new_city_foldername = values[2].split(' ')[-1].strip()
    month_foldername = values[3].strip().split(' ')[-2].strip()
    new_year_foldername = values[3].split(' ')[-1].strip()
    converted_month_foldername=month_foldername
    if month_foldername in month_folder_list:
        converted_month_foldername = month_folder_list[month_foldername]
        print(f'{idx+1}==>[{new_filename}], [{new_city_foldername}], [{new_year_foldername}], [{converted_month_foldername}], [{new_cust_foldername}], [{filename}]')
    else:
        fail_count+=1
        print(f'{idx+1}==>[{new_filename}], [{new_city_foldername}], [{new_year_foldername}], [{converted_month_foldername}], [{new_cust_foldername}], [{filename}]')
        print(f"ERROR: {idx+1}==>[{filename}] month not found, Tell IT dept to investigate")
        fail_filelist.append((new_filename, filename, new_cust_foldername, new_city_foldername, new_year_foldername))

        continue
    if new_filename:
        old_name_fullpath= os.path.join(temp_directory, filename)
        new_filename_fullpath=os.path.join(temp_directory, new_filename)
        # print(f'old_name_fullpath={old_name_fullpath}')
        # print(f'new_filename_fullpath={new_filename_fullpath}')
        try:
            os.rename(old_name_fullpath, new_filename_fullpath) #rename to the original folder, not yet move or copy
            success_count+=1
        except Exception as e :
            print(str(e))
            fail_count+=1
            fail_filelist.append((new_filename, filename, new_cust_foldername, new_city_foldername, new_year_foldername))
            continue

        # # copy/move to destination folder
        target_copy_folder_name=os.path.join(target_directory_fullpath, new_year_foldername, converted_month_foldername, new_cust_foldername)
        check_or_create_directory(target_copy_folder_name, debug=True)
        # print(f'target folder fullpath={target_copy_folder_name}')
        target_copy_filename = os.path.join(target_copy_folder_name, new_filename)
        # print(f'target filename fullpath={target_copy_filename}')
        shutil.copy(new_filename_fullpath, target_copy_filename)
    else:
        fail_count+=1
        fail_filelist.append((new_filename, filename, new_cust_foldername, new_city_foldername, new_year_foldername))
        continue
    # print("")
    success_filelist.append((new_filename, filename, new_cust_foldername, new_city_foldername, new_year_foldername, month_foldername))

#finish copy to temp folder and rename and copy to target folder, then delete the temp folder   
shutil.rmtree( temp_directory )
# print(backup_dir_fullpath)
print("")
# backup_dir_fullpath=os.path.join(os.path.dirname(ori_directory_fullpath), f"backup\\{year_backup_folder}\\data ori")
backup_dir_fullpath = os.path.join(os.path.dirname(ori_directory_fullpath), f"backup\\[year]\\[month]\\data ori")
move_files_in_dir(ori_directory_fullpath, backup_dir_fullpath, datalist, success_filelist)

print("")
# print("")
print("Success Files:")
for idx, x in enumerate(success_filelist):
    print (idx+1, x)
print("")
if len(fail_filelist)>0:
    print("FAILED Filelist:")
    for x in fail_filelist:
        print(x)
print("")
input(f"From {len(filelist)} PDF Files, SUCCESS={success_count}, Fail={fail_count}, Rename and Copy from '{ori_directory_fullpath}'  TO  '{target_directory_fullpath}'. Press the Enter key to Exit: ")
