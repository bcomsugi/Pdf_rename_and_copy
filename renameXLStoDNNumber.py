import xlrd
import shutil
filename="example_001.xls"
# wb = openpyxl.load_workbook(filename, data_only=True)
wb = xlrd.open_workbook(filename)

print(wb)
print(wb.sheets)
# for sheet in wb.worksheets:
#     print(sheet)

for sheet in wb.sheets():
    print(sheet.name, sheet.nrows, sheet.ncols)
    for row in range(0, sheet.nrows):
        header = sheet.row_values(row, start_colx=0, end_colx=None)
        print(header)

DNRefNum = wb.sheets()[0].cell(1, 3).value.strip().split("-")[1][-1] + "".join(wb.sheets()[0].cell(1, 3).value.strip().split("-")[-2:])#[1][3].strip().split("-")[1][-1] + "".join(rawdata[1][3].strip().split("-")[-2:])
DNRefNum = wb.sheets()[0].cell(1, 3).value.strip().split(" ")[-1]

print(DNRefNum)
if DNRefNum.startswith("TCO-DN"):
    shutil.copy(filename, f'{DNRefNum}.xls')
    print(f'copy and rename example_001.xls to {DNRefNum}.xls success')
else:
    print ("this example_001.xls is not DeliveryNote file")