from pdfminer.high_level import extract_pages, extract_text     #pip install pdfminer-six
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal, LTPage
# import tabula
# import PyPDF2
import pandas as pd

filename = "example_001.pdf"
filename = "TCO-DNPG-2303-0951.pdf"
filename = "oriDNPG\TCO-DNPR-2305-00305.pdf"
items=[]
qtylist=[]
uomlist=[]
tcolist=[]
polist=[]
DNRefNum = None
TxnDate = None
Memo = None

for page_layout in extract_pages(filename):
    # print(type(page_layout), page_layout, page_layout.pageid)
    # if page_layout.pageid == 1:
    if True:
        print(f'page:{page_layout.pageid}')
        bbox_y_item = 10000
        bbox_y_qty = 10000
        bbox_y_tco = 10000
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for textline in element:
                    if isinstance(textline, LTTextLineHorizontal):
                        if 363 < int(textline.bbox[0]) <368:
                            if textline.get_text().split('\n')[0].split(' ')[1].strip().startswith("TCO-DN"):
                                # DNRefNum.append(textline.get_text().split('\n')[0].split(' ')[1].strip())
                                DNRefNum = textline.get_text().split('\n')[0].split(' ')[1].strip() # from TCO-DNPG-2305-00305
                                DNRefNum = f'{DNRefNum.split("-")[-3][-1]}{DNRefNum.split("-")[-2]}{DNRefNum.split("-")[-1]}'   # into G230500305
                            elif textline.get_text().split('\n')[0].split(' ')[1].strip().startswith("20"):
                                TxnDate = textline.get_text().split('\n')[0].split(' ')[1].strip()

                        if 43<int(textline.bbox[0])<47:
                            if bbox_y_item > textline.bbox[1]:
                                bbox_y_item = textline.bbox[1]
                                print( textline,  'ITEM')
                                if not textline.get_text().startswith("Sub") and not textline.get_text().startswith("Jenis") and not textline.get_text().startswith("Item") and not textline.get_text().startswith("Page") and not textline.get_text().startswith("Printed"):
                                    # if textline.get_text().split('\n')[0].strip() == "TH-002AA":
                                    #     items.append('TH')
                                    if textline.get_text().split('\n')[0].strip() == "TPB-18.":
                                        items.append('TPB-18')
                                    else:
                                        items.append(textline.get_text().split('\n')[0].strip())
                            else:
                                pass
                                print("Item Not in order")
                        elif 275 < int(textline.bbox[0]) < 290 and not textline.get_text().startswith("Quantity"):
                            if bbox_y_qty > textline.bbox[1]:
                                bbox_y_qty = textline.bbox[1]
                                print( textline,  'QUANTITY')
                                qtylist.append(float(textline.get_text().split('\n')[0].strip().split(' ')[0].strip()))
                                uomlist.append(textline.get_text().split('\n')[0].strip().split(' ')[1].strip())
                            else:
                                pass
                                print("QTY Not in order")
                        elif 375<int(textline.bbox[0])<379:
                            if bbox_y_tco > textline.bbox[1]:
                                bbox_y_tco = textline.bbox[1]
                                if 472<int(textline.bbox[2])<475:
                                    print( textline,  'TCOSOL')
                                    tcolist.append(textline.get_text().split(' ')[0].strip())
                                else:
                                    print( textline,  'PONUM')
                                    polist.append(textline.get_text().split('\n')[0].strip())
                            else:
                                pass
                                print("TCO or PONo Not in order")
                        else:
                            pass
                            print( textline, textline.bbox)
                        # elif int(textline.bbox[0])==377 and int(textline.bbox[2])==:
                        #     print( textline, textline.bbox, 'TCOSOL')
                        # elif int(textline.bbox[0])==282:
                        #     print( textline, textline.bbox, 'QUANTITY')
    print(items, len(items))
    print(qtylist, len(qtylist))
    print(tcolist, len(tcolist))
    print(polist, len(polist))
print(f'items, {len(items)}')
print(f'qtylist, {len(qtylist)}')
print(f'tcolist, {len(tcolist)}')
print(f'polist, {len(polist)}')
alllist=list(zip(items,items,qtylist, tcolist,tcolist , uomlist,polist))
# print(alllist, len(alllist))
for idx, x in enumerate(alllist):
    print(idx, x)
Memo = DNRefNum
print(DNRefNum, Memo, TxnDate)                        
newdata = alllist
DeliveryNotedict={'DNRefNum':DNRefNum, 'TxnDate':TxnDate, 'Memo': Memo}

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