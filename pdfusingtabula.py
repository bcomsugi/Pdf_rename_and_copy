import tabula
import timeit
import pandas as pd
from pdftools import get_column_bbox, get_area_table, list_dir


def convert_pdf(filename:str):
    start = timeit.default_timer()
    print(f'Filename:{filename}')
    # filename = "example_001.pdf"
    # filename = r"c:\Users\bcoms\Downloads\63178-27.pdf" ### invoice ###
    # filename = "TCO-DNPG-2303-0951.pdf"
    # filename = r"c:\Users\bcoms\Downloads\TCO-DNKR-2311-00510.pdf"
    # filename = r"c:\Users\bcoms\Downloads\TCO-DNKR-2307-00361.pdf"
    # filename = "oriDNPG\TCO-DNPR-2305-00305.pdf"
    # Read pdf into a list of DataFrame
    # dfs_source = tabula.read_pdf(filename, pages='all', multiple_tables=True, lattice=True)
    # dfs_source = tabula.read_pdf(filename, pages='all', multiple_tables=True, lattice=False, area=[230, 42, 600, 580])
    page_height = 792
    page_width = 612
    column_bbox=get_column_bbox(filename)
    print(column_bbox)
    header_area = get_area_table(column_bbox)
    print(header_area)
    area = (page_height-header_area[3], header_area[0], page_height-header_area[3]+370, page_width )
    print(f'area:{area}')
    column_devider=[column_bbox['bbox_Desc'][0]-1, column_bbox['bbox_Qty'][0]-1, column_bbox['bbox_Qty'][0]+40-1, column_bbox['bbox_SO'][0]-1, column_bbox['bbox_LPN'][0]-1]
    print(f'column divider:{column_devider}')
    df_header = tabula.read_pdf(filename, pages=1, lattice=False, area = [ 0, 280, 220, 580]) ## GET Header Info

    dfs_source = tabula.read_pdf(filename, pages='all', multiple_tables=True, lattice=False,columns=column_devider, area=area, ) # columns=[140.2, 283.2, 325.2, 380.2, 495.2] for newer DN. maybe start from Oct 2023 # area=(y, x, y+height, x+width) 

    # dfs_source = tabula.read_pdf(filename, pages='all', multiple_tables=True, lattice=False,columns=[133, 274.2, 317.2, 373.2, 486.2], area=(230, 42, 600, 580), ) # columns=[133, 274.2, 317.2, 373.2, 486.2] for the older DN, before Oct maybe
    # print(dfs_source, type(dfs_source), len(dfs_source))
    # exit()
    def get_sublist(itemdesc : str):
        if isinstance(itemdesc, str):
            # print(itemdesc, type(itemdesc))
            
            item_code = itemdesc.split(' ')[0]
            if '400_Sales' in item_code:
                _ = itemdesc.split(' ')[1]
                item_code = item_code + " " + _
            # print( item_code)
            return item_code
        else:
            print(f" none:{itemdesc}")
        return None
    grand_total = 0
    dfs=[]

    for idx_df, df in enumerate(dfs_source):
        df = df.loc[~(df['Item No'].str.contains('Jenis', na=False)) & ~(df['Item No'].str.contains('Total', na=False)) ]
        dfs.append(df)
        # print(f' idx:{idx_df}')
        # print(df)
    ### di bawah ini ga perlu lagi, krena sdh pakai latice
    for idx_df, df in enumerate(dfs_source):
        # print(df)
        if 'Item Description' in df:
            df['Item No'] = df.apply(lambda x: get_sublist(x['Item Description']), axis=1)
            # print(df['Item No'].notnull())
            # print(f"get None: {df[df['Item No'].isnull()].index.to_list()}")
            


            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            
            df = df.where(df.notnull(), None)
            # print(df)
            
            if 'Price Total' in df:
                df[['Price', 'Total']] = df['Price Total'].str.split(" ", expand=True)
            if 'Qty Unit' in df:
                df[['Qty', 'Unit']] = df['Qty Unit'].str.split(" ", expand=True)
            
            # print(df)
            df.dropna(thresh=3,  inplace=True)
            df.reset_index(drop= True, inplace=True)
            # print(df)
            index = None
            try:
                index = df[df['Item No'].isnull()].index.to_list()[0]
                # print(f"None index:{index}")
            except:
                print('cannot get index')
            if index:
                # print(f'len df:{len(df)}')
                # print(df.iloc[index])
                if 'Price Total' in df and grand_total==0:
                    grand_total = df['Price Total'].iloc[index]
                    print(f'grand Total = {grand_total}')
                elif df['Total'].iloc[index]!=None and grand_total==0:
                    grand_total = df['Total'].iloc[index]
                    print(f'grand Total = {grand_total}')
                # print(df.iloc)
                df = df.iloc[:index]
            df['Grand_Total']=grand_total
            # print(df)#, df.info())
            df_edited = df[['Item No', 'SJ No', 'Qty', 'Unit', 'Price', 'Total', 'Grand_Total']]
            # print(df_edited)
            dfs.append(df_edited)
        elif 'Item' in df:
            index = None
            # print(df)
            try:
                index = df[df['Description'].isnull()].index.to_list()[0]
                # print(f"None index:{index}")
            except:
                print('cannot get index')
            print(df)
            
            df['Description'] = df['Description'].where(df['Description'].notnull(), "")
            # grand_total_temp = df.iloc[df['Description'].str.contains('Grand Total').values.tolist(), df.columns.str.contains('Description')].values[0][0]
            grand_total_temp = df.iloc[df['Description'].str.contains('Grand Total').values.tolist()]['Description'].values[0]
            print(grand_total_temp, type(grand_total_temp))
            if 'rp' in grand_total_temp.strip().lower():
                grand_total = grand_total_temp.split("Rp")[1]
            
            if index:
                df = df.iloc[:index]
            df['Grand_Total']=grand_total
            # print(df)

            df[['Price', 'Total']] = (df[['Price', 'Total']].replace('[.]','', regex=True).replace('[,]','.', regex=True).astype('float64'))
            # print(df)
            # print(df.info())
            dfs.append(df)
        elif 'Bill To' in df:
            print(df)
        elif "Invoice #" in df:
            print(df)
        
    # print(dfs)

    df = pd.concat(dfs).reset_index()

    # print(df)
    df = df.groupby(df.index // 2).agg(lambda x: ' '.join(x.ffill(downcast='infer').astype(str).unique())).drop('index', axis=1)
    df['Quantity'] = df['Quantity'].astype('float')
    # print(df)
    # print(df)
    # print(df.info())
    df[['No.SO', 'Ext.Doc.No']] = df['No.SO/Ext.Doc.No.'].str.split(" / ", expand=True)

    df[['LPN No', 'Packaging']] = df['LPN No.'].str.split(" - ", expand=True)

    # print(df, df.info())

    # print(df_header[0], type(df_header[0]))
    # print(df_header[0].values)
    # df=df.groupby(['Ext.Doc.No', 'No.SO','Item No', 'UOM', 'FullName'])['Quantity'].sum().reset_index().sort_values(by=['Ext.Doc.No.','No.SO', 'Item No'])



    ### get_Header ###
    Branch = None
    for _ in df_header[0].values.tolist():
        # print(_, type(_))
        if 'TCO-DN' in _[0]:
            DNRefNum = _[0].split(":")[1].strip()
            DNRefNum = f'{DNRefNum.split("-")[-3][-1]}{DNRefNum.split("-")[-2]}{DNRefNum.split("-")[-1]}'   # into G230500305
            print(f'DN:{DNRefNum}')
        elif 'Date' in _[0]:
            TxnDate = _[0].split(":")[1].strip()
            print(f'TxnDate:{TxnDate}')
        elif 'ANTARTIKA' in _[0]:
            Branch = 'SBY'
        elif 'NAS ' in _[0]:
            Branch = 'BGR'

    DeliveryNotedict={'DNRefNum':DNRefNum, 'TxnDate':TxnDate, 'Memo': DNRefNum, 'Branch': Branch}
    # DeliveryNotedict['lines'] = df.to_dict('records')
    df=df.groupby(['Ext.Doc.No', 'No.SO','Item No', 'UOM'])['Quantity'].sum().reset_index().sort_values(by=['Ext.Doc.No','No.SO', 'Item No'])

    df['NameFromTaco'] = df['Item No']
    inteminvdf = pd.read_excel('ItemInventory20231416.xlsx', usecols=['FullName', 'NameFromTaco'] )
    # print(inteminvdf)
    # print (inteminvdf.index)

    df=df.merge(inteminvdf, how='left')
    # print(df['FullName'].isnull().values.any())
    print(df)
    if df['FullName'].isnull().sum() > 0:

        print("Cannot Find Item FullName")
        listitemNoFullName = df.loc[df['FullName'].isnull()].values.tolist()
        print(df.loc[df['FullName'].isnull()].values)
        print(listitemNoFullName)
        # return listitemNoFullName
    else:
        # print(df)
        df=df.groupby(['Ext.Doc.No', 'No.SO','Item No', 'UOM', 'FullName'])['Quantity'].sum().reset_index().sort_values(by=['Ext.Doc.No','No.SO', 'Item No'])
        print(df)
        lst = df.to_dict('records')
        # print(lst)
        DeliveryNotedict['lines']=lst
        print(DeliveryNotedict, len(DeliveryNotedict['lines']))
        # return deliveryNotedict



    # print(DeliveryNotedict)
    # print(df_header, type(df_header))
    ### end get_header ###

    # print(df_dict)
    print(f'Timeit = {timeit.default_timer() - start}')
    return DeliveryNotedict



if "__main__" == __name__:
    print(list_dir())
    starttime = timeit.default_timer()
    lstConvert = []
    for idx, _ in enumerate(list_dir("D:\Project\Python38\DNPG\okt")[:1]):
        lstConvert.append(convert_pdf(_))
    for _ in lstConvert:
        print(_)
    
    print(f'Timeit all = {timeit.default_timer() - starttime}, {idx+1} files')
    