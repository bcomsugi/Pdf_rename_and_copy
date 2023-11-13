from pdfminer.high_level import extract_pages, extract_text     #pip install pdfminer-six
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal, LTPage
# import tabula
# import PyPDF2
import pandas as pd

filename = "example_001.pdf"
filename = "TCO-DNPG-2303-0951.pdf"
filename = "oriDNPG\TCO-DNPR-2305-00305.pdf"
filename = "60974-03.pdf"
items=[]
sjno=[]
qtylist=[]
uomlist=[]
prices=[]

tcolist=[]
polist=[]
RefNum = None
TxnDate = None
BillTo_1 = None
BillTo_2 = None
grandTotal = None

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
        print(data)
        return data
    else:
        print('salah')
    return None

for page_layout in extract_pages(filename):
    # print(type(page_layout), page_layout, page_layout.pageid)
    # if page_layout.pageid == 1:
    if True:
        print(f'page:{page_layout.pageid}')
        bbox_y_item = 10000
        bbox_y_uom = 10000
        bbox_y_price = 10000
        bbox_y_sjno = 10000
        bbox_y_qty = 10000
        bbox_y_tco = 10000
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for textline in element:
                    if isinstance(textline, LTTextLineHorizontal):
                        if 10 < int(textline.bbox[0]) < 18 and 160 < int(textline.bbox[1]) < 560 :
                            if bbox_y_item > textline.bbox[1]:
                                bbox_y_item = textline.bbox[1]
                                print( "item->", textline,  'Item')
                                items.append(textline.get_text().split('\n')[0].strip())
                            else:
                                print("Item Not in order")

                        elif 255 < int(textline.bbox[0]) < 280 and 160 < int(textline.bbox[1]) < 560 :
                            if bbox_y_sjno > textline.bbox[1]:
                                bbox_y_sjno = textline.bbox[1]
                                print( "SJ No->", textline,  'SJ No')
                                sjno.append(textline.get_text().split('\n')[0].strip())
                            else:
                                print("SJ no Not in order")

                        elif 335 < int(textline.bbox[0]) < 360 and 160 < int(textline.bbox[1]) < 560 :
                            if bbox_y_qty > textline.bbox[1]:
                                bbox_y_qty = textline.bbox[1]
                                print( "qty UOM->", textline,  'qty UOM')
                                # qtylist.append(float(textline.get_text().split('\n')[0].strip().split(' ')[0].strip()))
                                # uomlist.append(textline.get_text().split('\n')[0].strip().split(' ')[1].strip())
                                qtylist.append(float(textline.get_text().split('\n')[0].split(' ')[0].strip()))
                                uomlist.append(textline.get_text().split('\n')[0].split(' ')[1].strip())
                            else:
                                print("qty UOM Not in order")

                        elif 400 < int(textline.bbox[0]) < 460 and 118 < int(textline.bbox[1]) < 560 :
                            if bbox_y_price > textline.bbox[1]:
                                bbox_y_price = textline.bbox[1]
                                print( "price->", textline,  'price')
                                
                                prices.append(convertRPToFloat(textline.get_text().split('\n')[0].strip()))
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
                            print(convertRPToFloat(grandTotal),)
                            

                        # elif 363 < int(textline.bbox[0]) <368:
                        #     if textline.get_text().split('\n')[0].split(' ')[1].strip().startswith("TCO-DN"):
                        #         # RefNum.append(textline.get_text().split('\n')[0].split(' ')[1].strip())
                        #         RefNum = textline.get_text().split('\n')[0].split(' ')[1].strip() # from TCO-DNPG-2305-00305
                        #         RefNum = f'{RefNum.split("-")[-3][-1]}{RefNum.split("-")[-2]}{RefNum.split("-")[-1]}'   # into G230500305
                        #     elif textline.get_text().split('\n')[0].split(' ')[1].strip().startswith("20"):
                        #         TxnDate = textline.get_text().split('\n')[0].split(' ')[1].strip()

                        # if 43<int(textline.bbox[0])<47:
                        #     if bbox_y_item > textline.bbox[1]:
                        #         bbox_y_item = textline.bbox[1]
                        #         print( textline,  'ITEM')
                        #         if not textline.get_text().startswith("Sub") and not textline.get_text().startswith("Jenis") and not textline.get_text().startswith("Item") and not textline.get_text().startswith("Page") and not textline.get_text().startswith("Printed"):
                        #             # if textline.get_text().split('\n')[0].strip() == "TH-002AA":
                        #             #     items.append('TH')
                        #             if textline.get_text().split('\n')[0].strip() == "TPB-18.":
                        #                 items.append('TPB-18')
                        #             else:
                        #                 items.append(textline.get_text().split('\n')[0].strip())
                        #     else:
                        #         pass
                        #         print("Item Not in order")
                        # elif 275 < int(textline.bbox[0]) < 290 and not textline.get_text().startswith("Quantity"):
                        #     if bbox_y_qty > textline.bbox[1]:
                        #         bbox_y_qty = textline.bbox[1]
                        #         print( textline,  'QUANTITY')
                        #         qtylist.append(float(textline.get_text().split('\n')[0].strip().split(' ')[0].strip()))
                        #         uomlist.append(textline.get_text().split('\n')[0].strip().split(' ')[1].strip())
                        #     else:
                        #         pass
                        #         print("QTY Not in order")
                        # elif 375<int(textline.bbox[0])<379:
                        #     if bbox_y_tco > textline.bbox[1]:
                        #         bbox_y_tco = textline.bbox[1]
                        #         if 472<int(textline.bbox[2])<475:
                        #             print( textline,  'TCOSOL')
                        #             tcolist.append(textline.get_text().split(' ')[0].strip())
                        #         else:
                        #             print( textline,  'PONUM')
                        #             polist.append(textline.get_text().split('\n')[0].strip())
                        #     else:
                        #         pass
                        #         print("TCO or PONo Not in order")
                        # else:
                        #     pass
                        #     print( textline, textline.bbox)
                        # # elif int(textline.bbox[0])==377 and int(textline.bbox[2])==:
                        # #     print( textline, textline.bbox, 'TCOSOL')
                        # # elif int(textline.bbox[0])==282:
                        # #     print( textline, textline.bbox, 'QUANTITY')
    print(items, len(items))
    print(sjno, len(sjno))
    print(qtylist, len(qtylist))
    print(uomlist, len(uomlist))
    print(prices, len(prices))
    print(tcolist, len(tcolist))
    print(polist, len(polist))
print(f'items, {len(items)}')
print(f'qtylist, {len(qtylist)}')
print(f'tcolist, {len(tcolist)}')
print(f'polist, {len(polist)}')
# alllist=list(zip(items,items,qtylist, tcolist,tcolist , uomlist,polist))
alllist=list(zip(items,items,qtylist, uomlist, prices, uomlist, prices))

# print(alllist, len(alllist))
for idx, x in enumerate(alllist):
    print(idx, x)
# BillTo_1 = RefNum
print(RefNum, BillTo_1,  BillTo_2, TxnDate)
newdata = alllist
DeliveryNotedict={'RefNum':RefNum, 'TxnDate':TxnDate, 'BillTo_1': BillTo_1, 'BillTo_2': BillTo_2}

df=pd.DataFrame(newdata, columns=['Item No', 'Description', 'Quantity', 'No.SO/Ext.Doc.No.', 'LPN No.', 'UOM', 'Ext.Doc.No.'])#, columns=data[0]+"UOM")
# print(df)
# df=df.groupby(['No.SO/Ext.Doc.No.','Item No', 'UOM'])['Quantity'].sum().reset_index().sort_values(by=['Item No', 'No.SO/Ext.Doc.No.'])#.sort_values(by=['No.SO/Ext.Doc.No.'])
df=df.groupby(['Ext.Doc.No.', 'No.SO/Ext.Doc.No.','Item No', 'UOM'])['Quantity'].sum().reset_index().sort_values(by=['Ext.Doc.No.','No.SO/Ext.Doc.No.', 'Item No'])
df['NameFromTaco']=df['Item No']
print(df)
# df['FullName'] = inteminvdf.loc[df['Item No'],'FullName']

inteminvdf = pd.read_excel('ItemInventory140723.xlsx', usecols=['FullName', 'NameFromTaco'])
# print(inteminvdf)
# print (inteminvdf.index)

df=df.merge(inteminvdf, how='left')
print(df['FullName'].isnull().values.any())
if df['FullName'].isnull().sum() > 0:

    print("Cannot Find Item FullName")
    listitemNoFullName = df.loc[df['FullName'].isnull()].values.tolist()
    print(df.loc[df['FullName'].isnull()].values)
    print(listitemNoFullName)
    # return listitemNoFullName
else:
    print(df)
    df=df.groupby(['Ext.Doc.No.', 'No.SO/Ext.Doc.No.','Item No', 'UOM', 'FullName'])['Quantity'].sum().reset_index().sort_values(by=['Ext.Doc.No.','No.SO/Ext.Doc.No.', 'Item No'])
    print(df)
    lst = df.to_dict('records')
    # print(lst)
    DeliveryNotedict['lines']=lst
    print(DeliveryNotedict)
    # return deliveryNotedict