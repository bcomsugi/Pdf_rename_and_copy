import PyPDF2
import pandas as pd


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
    tot_pages=6
    for i in range(tot_pages):
        # creating a page object
        # pageObj = pdfReader.getPage(page)
        pageObj = pdfReader.pages[i]

        # extracting text from page
        print(pageObj.extract_text())
        # reader_splited+=pageObj.extract_text().split('\n')\

    # print(reader_splited)
    pdfFileObj=None
    return reader_splited

rst = read_pdf('example_001.pdf')

# print(rst)

import tabula

# Read pdf into list of DataFrame
dfx = tabula.read_pdf("example_001.pdf", pages='all')
dfs=[]
for tempdf in dfx:
    tempdf=tempdf.rename(columns= {'Item No Description': 'Item No'})
    dfs.append(tempdf)
print (dfs[1].head(20))
df=pd.concat(dfs, ignore_index=True).reset_index(drop=True)
df=df.dropna(subset=['No.SO/Ext.Doc.No.',]).reset_index(drop=True)
df=df.astype(str)

# print(df.head(26))
# print(dfs)
page=3

print(dfs[page])
# for x in dfs:
#     print(x[1])
# result = [x for x in dfs[page]['Item No Description']]
# print(result)

# dfs[page]['No.SO/Ext.Doc.No.']=dfs[page]['No.SO/Ext.Doc.No.'].astype(str)
dfs[page]=dfs[page].astype(str)
# print(dfs[page].dtypes)
# dfs[page]['QuantityUOM']=dfs[page]['QuantityUOM'].astype(str)
lineitem={}
dnlist={}
# for i in range(len(dfs[page])):
#     # if i%2==0:
#     if dfs[page].loc[i, "QuantityUOM"]=='nan':
#         # print(i, dfs[page].loc[i, "No.SO/Ext.Doc.No."])
#         ponumber=dfs[page].loc[i, "No.SO/Ext.Doc.No."]
#         # print(i, ponumber)
#         lineitem['ponumber']=ponumber
        
#     else:
      
#         if 'Item No' in dfs[page]:
#             itemcode=dfs[page].loc[i, "Item No"].split(" ")[0].strip()
#         else:
#             itemcode=dfs[page].loc[i, "Item No Description"].split(" ")[0].strip()
            
#         qty=int(dfs[page].loc[i, "QuantityUOM"].split(" ")[0].split(".")[0].strip())
#         uom=dfs[page].loc[i, "QuantityUOM"].split(" ")[1].strip()
#         sol=dfs[page].loc[i, "No.SO/Ext.Doc.No."].split(" ")[0]
#         lineitem['itemcode']=itemcode
#         lineitem['qty']=qty
#         lineitem['uom']=uom
#         lineitem['sol']=sol

#         # print(i, itemcode, qty, uom, sol)
#     print(i, lineitem)
#     if i%2==0 and i>1 :
#         # print(i, lineitem)
#         # if ponumber in 
#         pass


for i in range(len(df)):
    # if i%2==0:
    if df.loc[i, "QuantityUOM"]=='nan':
        # print(i, df.loc[i, "No.SO/Ext.Doc.No."])
        ponumber=df.loc[i, "No.SO/Ext.Doc.No."]
        # print(i, ponumber)
        lineitem['ponumber']=ponumber
        
    else:
      
        if 'Item No Description' in df:
            itemcode=df.loc[i, "Item No Description"].split(" ")[0].strip()
        else:
            itemcode=df.loc[i, "Item No"].split(" ")[0].strip()
            
        qty=int(df.loc[i, "QuantityUOM"].split(" ")[0].split(".")[0].strip())
        uom=df.loc[i, "QuantityUOM"].split(" ")[1].strip()
        sol=df.loc[i, "No.SO/Ext.Doc.No."].split(" ")[0]
        lineitem['itemcode']=itemcode
        lineitem['qty']=qty
        lineitem['uom']=uom
        lineitem['sol']=sol

        # print(i, itemcode, qty, uom, sol)
    # print(i, lineitem)
    if i%2==0 and i>1 :
        # print(i, lineitem)
        # if ponumber in 
        pass



# result = [(row[page], row[1]) for row in dfs[['Item No Description','QuantityUOM']].to_numpy()]
# Read remote pdf into list of DataFrame
# dfs2 = tabula.read_pdf("https://github.com/tabulapdf/tabula-java/raw/master/src/test/resources/technology/tabula/arabic.pdf")

# convert PDF into CSV file
# tabula.convert_into("test.pdf", "output.csv", output_format="csv", pages='all')

# convert all PDFs in a directory
# tabula.convert_into_by_batch("input_directory", output_format='csv', pages='all')

print(int('glossy15'))