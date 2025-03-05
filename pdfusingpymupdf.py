import fitz # imports the pymupdf library
import pandas as pd
import pprint


def getItemFullName(df, DeliveryNotedict, debug:bool=False):
    inteminvdf = pd.read_excel('ItemInventory20231416.xlsx', usecols=['FullName', 'Name'] )
    # print(inteminvdf)
    # print (inteminvdf.index)

    df=df.merge(inteminvdf, how='left', left_on='Item', right_on='Name').reset_index()
    df.loc[(df['Item']=='400_Sales Discount') & (df['FullName'].isnull()), "FullName"] = df['Item']
    df.loc[(df['Item']=='Sales Promo Discount') & (df['FullName'].isnull()), "FullName"] = df['Item']
    df.loc[(df['Item']=='Sales Promo Discou...') & (df['FullName'].isnull()), "FullName"] = "Sales Promo Discount"
    df.loc[(df['Item']=='PETI') & (df['FullName'].isnull()), "FullName"] = df['Item']
    df.loc[(df['Item']=='Sales Ekspedisi') & (df['FullName'].isnull()), "FullName"] = df['Item']

    # print(df['FullName'].isnull().values.any())
    if debug:print(df)
    if df['FullName'].isnull().sum() > 0:
        print("Cannot Find Item FullName")
        listitemNoFullName = df.loc[df['FullName'].isnull()].values.tolist()
        print(df.loc[df['FullName'].isnull()].values)
        print(listitemNoFullName)
        # print(f'Timeit = {timeit.default_timer() - start}')
        return listitemNoFullName
    else:
        # print(df)
        # df=df.groupby(['Ext.Doc.No', 'No.SO','Item No', 'UOM', 'FullName'])['Quantity'].sum().reset_index().sort_values(by=['Ext.Doc.No','No.SO', 'Item No'])
        # if debug:print(df)
        lst = df.to_dict('records')
        # print(lst)
        DeliveryNotedict['lines']=lst
        if debug:print("deliveryNotedict", pprint.pprint(DeliveryNotedict), len(DeliveryNotedict['lines']))
        # print(f'Timeit = {timeit.default_timer() - start}')
        return DeliveryNotedict


def getHeader(df_header, text, debug:bool=False):
    ### get_Header  INVOICE DBW ###
    Branch = None
    BillTo = None
    
    ##get billto
    texts = text.split("\n")
    # print("texts:",texts)
    isBillToOn = False
    for _ in texts:
        if isBillToOn:
            BillTo = _
            isBillToOn=False
            break
        if "Bill To" in _:isBillToOn=True


    for header in df_header:
        if debug:print(header, type(header))
        if 'Date' in header:
            for _ in header.values.tolist():
                if debug:print(_, type(_))
                TxnDate = _[0]
                DNRefNum = _[1]
                # if 'TCO-DN' in _[0]:
                #     DNRefNum = _[0].split(":")[1].strip()
                #     DNRefNum = f'{DNRefNum.split("-")[-3][-1]}{DNRefNum.split("-")[-2]}{DNRefNum.split("-")[-1]}'   # into G230500305
                #     print(f'DN:{DNRefNum}')
                # elif 'Date' in _[0]:
                #     TxnDate = _[0].split(":")[1].strip()
                #     print(f'TxnDate:{TxnDate}')
                # elif 'ANTARTIKA' in _[0]:
                #     Branch = 'SBY'
                # elif 'NAS ' in _[0]:
                #     Branch = 'BGR'
        # elif 'Bill To' in header:
        #     for _ in header.values.tolist():
        #         if debug:print(_, type(_))
        #         BillTo = _[0]
        #         # DNRefNum = _[1]
    DeliveryNotedict={'DNRefNum':DNRefNum, 'TxnDate':TxnDate, 'Memo': DNRefNum, 'BillTo': BillTo, 'Branch': Branch}
    if debug:print("DeliveryNotedict Header:", DeliveryNotedict)
    return DeliveryNotedict

def isYearCorrect(page, year):
    text = page.get_text()
    if "/"+year in text: return True
    elif "-"+year in text: return True
    else:return False

def convertPDF(filename:str, year:str="2024" ,debug:bool=False):
    doc = fitz.open(filename) # open a document
    if not isYearCorrect(doc[0], year): return None
    lines = []
    grandTotal = None
    for page in doc: # iterate the document pages
        text = page.get_text() # get plain text encoded as UTF-8
        # print("PAGE:",page.number, type(page.number))

        tabs = page.find_tables()
        print(f"{len(tabs.tables)} table(s) on {page}")
        if len(tabs.tables) < 3:continue
        if len(tabs.tables) == 4: tab = tabs[-2]
        elif len(tabs.tables) == 3: tab = tabs[-1]
        else: continue
        noneCol = None
        # print(tab.extract()[0])
        for _idx, _ in enumerate(tab.extract()[0]):
            # print("__", _)
            if  _ ==None:
                noneCol=_idx
                # print("noneCol is here at idx:", noneCol)
                tempTab = tab.extract()[0]
                tempTab.pop(_idx)
                # print(tab.extract()[0], tempTab)
        print("nonecol:",noneCol)
        for _idx, line in enumerate(tab.extract()):  # print cell text for each row
            
            # print(line, len(line), page.number, _idx)
            if line[0] != None and line[0].strip() != "":
                # print(line, len(line), page.number, _idx)
                if page.number > 0 and _idx == 0:continue
                tempLine = []
                for _i, _ in enumerate(line): #eplacing \n with "" or " "
                    if _!= None and _i==0: _ = _.replace("\n", "")
                    if _!= None and _i>0: _ = _.replace("\n", " ")
                    if _i>4 and "," in _: 
                        if "." in _: _ = _.replace(".","").replace(",", ".")
                        else: _ = _.replace(",", ".")
                    tempLine.append(_)
                if noneCol: tempLine.pop(noneCol)
                # print(line, tempLine)
                lines.append(tempLine)
            else:
                for _i, _ in enumerate(line):
                    if _ != None and "Grand Total" in _:
                        # print(_)
                        if "Rp" in _ :grandTotal = line[_i].split("Rp")[1]
                        # print(grandTotal)
        if grandTotal==None:
            tab = tabs[-1]
            # print(tab.extract())
            for line in tab.extract():
                for _i, _ in enumerate(line):
                    if _ != None and "Grand Total" in _:
                        # print(_)
                        if "Rp" in _ :grandTotal = line[_i].split("Rp")[1]


    # print("lines=",lines, len(lines))
    print("len Lines:", len(lines))
    


    ## cleaning grandTotal from string to float
    if  "," in grandTotal: 
        if "." in grandTotal: grandTotal = grandTotal.replace(".","").replace(",", ".")
        else: grandTotal = grandTotal.replace(",", ".")
    grandTotal = float(grandTotal)
    # print("grandTotal:", grandTotal, type(grandTotal))

    df = pd.DataFrame(lines[1:], columns=lines[0] )
    # print(df)
    df["xQty"]=df["Qty"].replace("", "1")   ##fill the empty Qty, because sales disc have no qty(and also no Unit)
    df["xQty"]= df["xQty"].astype("int")
    df["Price"]= df["Price"].astype("float")
    df["Total"]= df["Total"].astype("float")
    # print(df)
    # print(df.info())

    df["xTotal"] = df["xQty"]*df["Price"]
    df.sort_values(by=["SJ No"], inplace=True)
    # df = tab.to_pandas()
    # print(df)
    notSameTotal = df[df["xTotal"]!=df["Total"]]
    print("not same:", notSameTotal, "len notSameTotal:",len(notSameTotal))
    sumTotal = float(df["Total"].sum())
    print("sumTotal:", sumTotal, type(sumTotal), "grandTotal:", grandTotal)
    isGrandTotalOk = False
    if len(notSameTotal)==0 and (sumTotal == grandTotal): ##check if qty*price==Total and sum(Total)==grandTotal
        print("isGrandTotalOk is True")
        isGrandTotalOk = True
    else:
        print("sumTotal <> grandtotal")

    if isGrandTotalOk:
        headers = [x.to_pandas() for x in doc[0].find_tables()]
        print("HEADERS")
        DeliveryNotedict = getHeader(headers, text, debug=False)
        DeliveryNotedict = getItemFullName(df, DeliveryNotedict, debug=False)
        pprint.pprint(DeliveryNotedict)
        return DeliveryNotedict
    else: return None



if "__main__" == __name__:
    from pdftools import list_dir
    lstConvert = []
    noneCounter = 0

    # for idx, _ in enumerate(list_dir(r"P:\ACCOUNTING\A. INVOICE DISTRINDO BAKTI WUTAMA")):
    #     print(idx, "filename:", _)
    #     lstConvert.append(convertPDF(_, "2023"))
    # for _idx, _ in enumerate(lstConvert):

    #     if _==None:noneCounter+=1
    #     print(_idx, _)
    #     print("")
    # print(len(lstConvert))


    # filename = r"C:/Users/bcoms/Downloads/63178-27.pdf"
    # # filename = r"P:/ACCOUNTING/A. INVOICE DISTRINDO BAKTI WUTAMA/AGUNG - JOMBANG/56154-06 AGUNG JOMBANG MANUAL.pdf"
    # filename = r"P:\ACCOUNTING\A. INVOICE DISTRINDO BAKTI WUTAMA\67489-17.pdf"
    # filename = r"P:\ACCOUNTING\A. INVOICE DISTRINDO BAKTI WUTAMA\ATRIA\CV ATRIA MITRA MULIA\68079-01 FIX POTONGAN TACO.pdf"
    # filename = r"P:/ACCOUNTING/A. INVOICE DISTRINDO BAKTI WUTAMA/ANEKA MATERIAL BALONGSARI/68083-01 Potongan Taco HPL Solid Colour Januari 2024.pdf"
    filename = r"P:\ACCOUNTING\A. INVOICE DISTRINDO BAKTI WUTAMA\HS\25730-18 REVISI.pdf"
    convertPDF(filename, "2020")