from pdfminer.high_level import extract_pages, extract_text     #pip install pdfminer-six
from pdfminer.layout import LAParams, LTTextContainer, LTTextLineHorizontal, LTPage, LTTextBoxHorizontal, LTRect, LTTextBox, LTTextBoxVertical
# import tabula
# import PyPDF2
import pandas as pd

filename = "example_001.pdf"
filename = "TCO-DNPG-2303-0951.pdf"
filename = "oriDNPG\TCO-DNPR-2305-00305.pdf"
filename = "60974-03.pdf"
filename = r"c:\Users\bcoms\Downloads\63178-27.pdf"
items=[]
descriptions=[]
sjno=[]
qtylist=[]
uomlist=[]
prices=[]
itemLineNumber=[]
sjnoLineNumber=[]
qtyLineNumber=[]
uomLineNumber=[]
priceLineNumber=[]
RefNum = None
TxnDate = None
BillTo_1 = None
BillTo_2 = None
grandTotal = None
DIVIDER = 14.2


def convertRPToFloat(data:str):
    koma = data.find(',')
    # print(koma)
    if koma == len(data)-3:
        # print('3')
        decimal = data.split(',')[1]
        data = data.split(',')[0]
        data = data.replace(".", "")
        data = f'{data}.{decimal}'
        data = format(float(data), ".2f") #float(data)
        # print(data)
        return data
    else:
        print('salah')
    return None
firstLineNumber = None



for page_layout in extract_pages(filename):
    # print(type(page_layout), page_layout, page_layout.pageid)
    # if page_layout.pageid == 1:
    
    if True:
        print(f'page:{page_layout.pageid}')
        page = page_layout.pageid
        bbox_y_item = 10000
        bbox_y_uom = 10000
        bbox_y_price = 10000
        bbox_y_sjno = 10000
        bbox_y_qty = 10000
        bbox_y_tco = 10000
        bbox_y_description = 10000
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for textline in element:
                    lineNumber = 0
                    if isinstance(textline, LTTextLineHorizontal):
                        if 10 < int(textline.bbox[0]) < 18 and 160 < int(textline.bbox[1]) < 560 :
                            if bbox_y_item > textline.bbox[1]:
                                bbox_y_item = textline.bbox[1]
                                print( "item->", textline,  'Item')
                                # items.append(textline.get_text().split('\n')[0].strip())
                                # lineNumber = 0
                                if firstLineNumber:
                                    lineNumber = firstLineNumber * page - int(textline.bbox[1]/14.2)
                                    itemLineNumber.append(lineNumber)
                                else:
                                    firstLineNumber = int(textline.bbox[1]/14.2)
                                    lineNumber = firstLineNumber-int(textline.bbox[1]/14.2)
                                    itemLineNumber.append(lineNumber)
                                items.append((lineNumber, textline.get_text().split('\n')[0].strip()))
                            else:
                                print("Item Not in order")

                        if 125 < int(textline.bbox[0]) < 140 and 160 < int(textline.bbox[1]) < 560 :
                            if bbox_y_description > textline.bbox[1]:
                                bbox_y_description = textline.bbox[1]
                                print( "desc->", textline,  'desc')
                                # lineNumber = 0
                                if firstLineNumber:
                                    lineNumber = firstLineNumber * page -int(textline.bbox[1]/14.2)
                                    # itemLineNumber.append(lineNumber)
                                else:
                                    firstLineNumber = int(textline.bbox[1]/14.2)
                                    lineNumber = firstLineNumber-int(textline.bbox[1]/14.2)
                                    # itemLineNumber.append(lineNumber)
                                descriptions.append((lineNumber, textline.get_text().split('\n')[0].strip()))
                            else:
                                print("Item Not in order")

                        elif 255 < int(textline.bbox[0]) < 280 and 160 < int(textline.bbox[1]) < 560 :
                            if bbox_y_sjno > textline.bbox[1]:
                                bbox_y_sjno = textline.bbox[1]
                                print( "SJ No->", textline,  'SJ No')
                                # lineNumber = 0
                                if firstLineNumber:
                                    lineNumber = firstLineNumber * page -int(textline.bbox[1]/14.2)
                                    # itemLineNumber.append(lineNumber)
                                else:
                                    firstLineNumber = int(textline.bbox[1]/14.2)
                                    lineNumber = firstLineNumber-int(textline.bbox[1]/14.2)
                                    # itemLineNumber.append(lineNumber)
                                sjno.append((lineNumber, textline.get_text().split('\n')[0].strip()))
                            else:
                                print("SJ no Not in order")

                        elif 335 < int(textline.bbox[0]) < 360 and 160 < int(textline.bbox[1]) < 560 :
                            if bbox_y_qty > textline.bbox[1]:
                                bbox_y_qty = textline.bbox[1]
                                print( "qty UOM->", textline,  'qty UOM')
                                if firstLineNumber:
                                    lineNumber = firstLineNumber * page -int(textline.bbox[1]/14.2)
                                else:
                                    firstLineNumber = int(textline.bbox[1]/14.2)
                                    lineNumber = firstLineNumber-int(textline.bbox[1]/14.2)
                                qtylist.append((lineNumber, float(textline.get_text().split('\n')[0].split(' ')[0].strip())))
                                uomlist.append((lineNumber, textline.get_text().split('\n')[0].split(' ')[1].strip()))
                            else:
                                print("qty UOM Not in order")

                        elif 400 < int(textline.bbox[0]) < 460 and 118 < int(textline.bbox[1]) < 560 :
                            if bbox_y_price > textline.bbox[1]:
                                bbox_y_price = textline.bbox[1]
                                print( "price->", textline,  'price')
                                if firstLineNumber:
                                    lineNumber = firstLineNumber * page -int(textline.bbox[1]/14.2)
                                else:
                                    firstLineNumber = int(textline.bbox[1]/14.2)
                                    lineNumber = firstLineNumber-int(textline.bbox[1]/14.2)
                                prices.append((lineNumber, convertRPToFloat(textline.get_text().split('\n')[0].strip())))
                            else:
                                pass
                                print("price Not in order")

                        elif 10 < int(textline.bbox[0]) < 18 and  668 < int(textline.bbox[1]) < 675 :
                            print( "BillTo_1 ->", textline,  'BillTo_1')
                            BillTo_1 = textline.get_text().split('\n')[0].strip()

                        elif 10 < int(textline.bbox[0]) < 18 and  652 < int(textline.bbox[1]) < 658 :
                            print( "BillTo_2 ->", textline,  'BillTo_2')
                            BillTo_2 = textline.get_text().split('\n')[0].strip()
                        
                        elif 400 < int(textline.bbox[0]) < 450 and  720 < int(textline.bbox[1]) < 740 :
                            print( "TxnDate ->", textline,  'TxnDate')
                            TxnDate = textline.get_text().split('\n')[0].strip()

                        elif 510 < int(textline.bbox[0]) < 550 and  720 < int(textline.bbox[1]) < 740 :
                            print( "Invoice# ->", textline,  'Invoice')
                            RefNum = textline.get_text().split('\n')[0].strip()
                            
                        elif 425 < int(textline.bbox[0]) < 565 and  130 < int(textline.bbox[1]) < 145 :
                            print( "grandTotal ->", textline,  'grandTotal')
                            grandTotal = textline.get_text().split('\n')[0].split('Rp')[1].strip()
                            grandTotal = convertRPToFloat(grandTotal)
                            print(grandTotal, type(grandTotal))

                        print(textline)    
    print(f'firstlinenumbber:{firstLineNumber * page}')
    print(items, len(items))
    print(descriptions, len(descriptions))
    print(sjno, len(sjno))
    print(qtylist, len(qtylist))
    print(uomlist, len(uomlist))
    print(prices, len(prices))
    print(itemLineNumber, len(itemLineNumber))
print(f'items, {len(items)}')
print(f'qtylist, {len(qtylist)}')
# alllist=list(zip(items,descriptions, sjno, qtylist, uomlist, prices))
templist = []
def fillList(data, templist):
    result = None
    for _ in data:
        if _[0] == idx:
            templist.append(_[1])
            result = True
            break
    else:
        templist.append(None)
    return templist, result
alllist = []

for idx in range(26*page):
    result = [None, None, None, None, None, None]

    templist=[idx]
    templist, result[0] = fillList(items, templist)
    # templist, result[1] = fillList(descriptions, templist)
    templist, result[2] = fillList(sjno, templist)
    templist, result[3] = fillList(qtylist, templist)
    templist, result[4] = fillList(uomlist, templist)
    templist, result[5] = fillList(prices, templist)
    print(result)
    if not all(v is None for v in result):
        alllist.append(templist)


print(alllist)


for idx, x in enumerate(alllist):
    print(idx, x)
print(RefNum, BillTo_1,  BillTo_2, TxnDate)
newdata = alllist
DeliveryNotedict={'RefNum':RefNum, 'TxnDate':TxnDate, 'BillTo_1': BillTo_1, 'BillTo_2': BillTo_2, 'GrandTotal': grandTotal}
df = pd.DataFrame(newdata, columns=['lineno', 'Item No', 'SJNo', 'Quantity', 'UOM', 'Price'])
# df=pd.DataFrame(newdata, columns=['Item No', 'Description', 'SJNo', 'Quantity', 'UOM', 'Price'])#, columns=data[0]+"UOM")
print(df)
df['NameFromTaco']=df['Item No']
# print(df)
# print("afterdf")
inteminvdf = pd.read_excel('ItemInventory140723.xlsx', usecols=['FullName', 'NameFromTaco'])

df=df.merge(inteminvdf, how='left')
df.loc[(df['Item No']=='400_Sales Discount'), "FullName"] = df['Item No']
print(f"null values are: {df['FullName'].isnull().values.any()}")
if df['FullName'].isnull().sum() > 0:

    print("Cannot Find Item FullName")
    print(df.loc[(df['Item No']=='400_Sales Discount')])
    listitemNoFullName = df.loc[df['FullName'].isnull()].values.tolist()
    # print(df.loc[df['FullName'].isnull()].values)
    # print(df.loc[df['FullName'].isnull(), df['UOM']==None].values)
    df.loc[df['UOM'].isna() & df['FullName'].isnull(),'FullName']=df['Item No']
    # print(dftemp)
    print(df)
    # dftemp['FullName']=dftemp['SJNo']
    # print(dftemp)
    # print(df.loc[df['UOM'].isna() & df['FullName'].isnull()])
    print(listitemNoFullName)
    # return listitemNoFullName
else:
    print(df)
    # df = df.astype({'Price': 'float'})
    print(df.info())
    # print(df)
    lst = df.to_dict('records')
    # print(lst)
    DeliveryNotedict['lines']=lst
    print(DeliveryNotedict)
    # return deliveryNotedict
# # print(df)
# df = df.sort_values(['SJNo', 'lineno'])
# print(df)
# lst = df.to_dict('records')
# # print(lst)
# DeliveryNotedict['lines']=lst
# print(DeliveryNotedict)
# print("end")
# for _ in DeliveryNotedict['lines']:
#     if isinstance(_['FullName'], float):
#         print(_['FullName'])
#     print(_['lineno'], _['FullName'], type(_['FullName']))

laparams = LAParams(word_margin=0.1)
for page_layout in extract_pages(filename, laparams=laparams):
    ltrect=[]
    lttextboxhorizontals_element = []
    lttextboxhors = []
    lttextboxs = []
    lttextboxvers = []
    if True:
        print(f'page:{page_layout.pageid}')
        print(page_layout)


        for element in page_layout:
            # print(element, type(element))
            if isinstance(element, LTTextBoxVertical):
                lttextboxvers.append(element)
            if isinstance(element, LTRect):
                # print(element)
                ltrect.append(element)
            # if isinstance(element, LTTextContainer):
            if isinstance(element, LTTextBox):
                lttextboxs.append(element)
            if isinstance(element, LTTextBoxHorizontal):
                lttextboxhors.append(element)

                for el in element:
                    # print(el)
                    lttextboxhorizontals_element.append(el)
        print(lttextboxhorizontals_element, len(lttextboxhorizontals_element))
        print(ltrect, len(ltrect))
        print(lttextboxhors, len(lttextboxhors))
        print(lttextboxs, len(lttextboxs))
        print(lttextboxvers, len(lttextboxvers))