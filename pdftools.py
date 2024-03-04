from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal
import timeit
import os



start = timeit.default_timer()
def list_dir(dir:str = None, filetype:str=".pdf"):
    lstDir = []
    res = []
    print(dir)
    if dir == None:
        dir = os.getcwd()
        print(f"os.getcwd:{dir}")
    for (dir_path, dir_names, file_names) in os.walk(dir):
        # print(dir_path, dir_names, file_names)

        # res.extend(file_names)
    # for file in os.walk(dir):
        # print(file_names)
        for filename in file_names:
            if filename.endswith(filetype):
                # print(f'dipath:{dir_path}')
                # print(os.path.join(dir_path, filename))
                lstDir.append(os.path.join(dir_path, filename))
    # print(res)
    print("")
    return lstDir

# filename = "example_001.pdf"
# filename = r"c:\Users\bcoms\Downloads\63178-27.pdf" ### invoice ###
# filename = r"c:\Users\bcoms\Downloads\TCO-DNKR-2311-00510.pdf"
# filename = r"c:\Users\bcoms\Downloads\TCO-DNKR-2307-00361.pdf"
# filename="D:\Project\Python38\DNPG\okt\04\TCO-DNPG-2309-02185.pdf"


bbox_Item = None
bbox_Description = None
bbox_QuantityUOM = None
bbox_NoSO = None
bbox_Price = None
bbox = None
def get_column_bbox(filename=None, type:str=None):
    # print(filename)
    bbox=None
    bbox_Item, bbox_Description, bbox_Price, bbox_NoSO, bbox_QuantityUOM = None,None,None,None,None
    if filename:
        if type == None:
            for page_layout in extract_pages(filename,   page_numbers=[0]):
                print(f'page:{page_layout.pageid}')
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        # print(element.get_text())
                        # print(element)
                        if 40 < element.bbox[0] < 600 and 540 < element.bbox[1] < 560:
                            # print(element)
                            if 'Item' in element.get_text():
                                bbox_Item = element.bbox
                            if 'Description' in element.get_text():
                                bbox_Description = element.bbox
                            if 'Quantity' in element.get_text():
                                bbox_QuantityUOM = element.bbox
                            if 'SO' in element.get_text():
                                bbox_NoSO = element.bbox
                            if 'LPN' in element.get_text():
                                bbox_Price = element.bbox
            # else:
            #     print("eeror")
            bbox = {'bbox_Item': bbox_Item, 'bbox_Desc': bbox_Description, 'bbox_Qty': bbox_QuantityUOM, 'bbox_SO': bbox_NoSO, 'bbox_LPN': bbox_Price}

            return bbox
        else:   ###type inv
            for page_layout in extract_pages(filename,   page_numbers=[0]):
                print(f'page inv pdf:{page_layout.pageid}')
                ymin= 0
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        # print(element.get_text())
                        # print(element)
                        if 16 < element.bbox[0] < 600 and 54 < element.bbox[1] < 590:
                            # print(element)
                            if 'Item' in element.get_text():
                                # if ymin < element.bbox[1]:
                                #     ymin = element.bbox[1]
                                bbox_Item = element.bbox
                                if ymin < element.bbox[1]:
                                    ymin = element.bbox[1]
                                    bbox_Item = (element.bbox[0], ymin, element.bbox[2], element.bbox[3])
                            if 'Description' in element.get_text():
                                # if ymin < element.bbox[1]:
                                #     ymin = element.bbox[1]
                                bbox_Description = element.bbox
                                if ymin < element.bbox[1]:
                                    ymin = element.bbox[1]
                                print(ymin)
                            if 'Qty' in element.get_text():
                                # if ymin < element.bbox[1]:
                                #     ymin = element.bbox[1]
                                bbox_QuantityUOM = element.bbox
                                if ymin < element.bbox[1]:
                                    ymin = element.bbox[1]
                                    print(ymin)
                                bbox_QuantityUOM = (element.bbox[0], ymin, element.bbox[2], element.bbox[3])
                                print(ymin)
                            if 'SJ' in element.get_text():
                                # if ymin < element.bbox[1]:
                                #     ymin = element.bbox[1]
                                bbox_NoSO = element.bbox
                                if ymin < element.bbox[1]:
                                    ymin = element.bbox[1]
                                bbox_NoSO = (element.bbox[0], ymin, element.bbox[2], element.bbox[3])
                            if 'Price' in element.get_text():
                                # if ymin < element.bbox[1]:
                                #     ymin = element.bbox[1]
                                bbox_Price = element.bbox
                                if ymin < element.bbox[1]:
                                    ymin = element.bbox[1]
                                print(ymin)
                                bbox_Price = (element.bbox[0], ymin, element.bbox[2], element.bbox[3])
                            if 'Total' in element.get_text() and not ('Grand' in element.get_text()):
                                # if ymin < element.bbox[1]:
                                #     ymin = element.bbox[1]
                                bbox_Total = element.bbox
                                if ymin < element.bbox[1]:
                                    ymin = element.bbox[1]
                                bbox_Total = (element.bbox[0], ymin, element.bbox[2], element.bbox[3])
                print(ymin)
            # else:
            #     print("eeror")
            bbox = {'bbox_Item': bbox_Item, 'bbox_Desc': bbox_Description, 'bbox_Qty': bbox_QuantityUOM, 'bbox_SO': bbox_NoSO, 'bbox_Price': bbox_Price, 'bbox_Total': bbox_Total}

            return bbox
    else:
        return None
#bbox = get_column_bbox(filename)
def get_area_table(bbox):
    xmin = 10000
    xmax = 0
    ymin = 10000
    ymax = 0
    # print(bbox['bbox_Item'][0])
    for item, value in bbox.items():
        # print(item, value)
        if xmin > value[0]:
            xmin = value[0]
        if ymin > value[1]:
            ymin = value[1]
        if xmax < value[2]:
            xmax = value[2]
        if ymax < value[3]:
            ymax = value[3]
    # area_bbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
    # print(f'Area:{area_bbox}')
    area_bbox = (xmin, ymin, xmax, ymax)
    return area_bbox
# bbox = get_column_bbox(filename)


if '__main__' ==__name__:
    pass
    # filename = r"c:\Users\bcoms\Downloads\TCO-DNKR-2311-00510.pdf"
    filename = r"c:\Users\bcoms\Downloads\63178-27.pdf" ### invoice ###

    bbox = get_column_bbox(filename, type='inv')
    print(bbox)
    print(get_area_table(bbox))
    # print(list_dir(r"D:\Project\Python38\DNPG\okt"))
    # get_column_bbox(r"D:\Project\Python38\DNPG\okt\04\TCO-DNPG-2309-02185.pdf")
    # for idx, _ in enumerate(list_dir("D:\Project\Python38\DNPG\okt")):
    #     print(get_column_bbox(_))
# print(bbox)
print(f'Timeit {__name__}= {timeit.default_timer() - start}')