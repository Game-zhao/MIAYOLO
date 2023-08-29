import os
import cv2
import imghdr
import shutil
import xml.etree.ElementTree as ET

imgType_list = {'jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif'}

def get_template():
    obj_string = '<object><name>sicktree</name>' + \
                 '<pose>Unspecified</pose><truncated>0</truncated>' + \
                 '<difficult>0</difficult><bndbox><xmin>834</xmin>' + \
                 '<ymin>763</ymin><xmax>868</xmax><ymax>795</ymax></bndbox></object>'

    root_string = '<annotation><folder>yilingtest</folder>' + \
                  '<filename>p_yl_0001.jpg</filename><path>D:\\&#27979;&#35797;&#22270;' + \
                  '\\yilingtest\\p_yl_0001.jpg</path><source><database>Unknown</database>' + \
                  '</source><size><width>1000</width><height>1000</height><depth>3</depth></size>' + \
                  '<segmented>0</segmented></annotation>'
    return obj_string, root_string


def create_xml(filename, width, height, depth, objs):
    """
    objs: [{'name': 'sicktree', 'xmin': 0, 'ymin': 0, 'xmax': 50, 'ymax': 50,},
           {'name': 'notree', 'xmin': 10, 'ymin': 20, 'xmax': 70, 'ymax': 90,},
            ...]
    """
    obj_template, root_template = get_template()
    xml_create = ET.fromstring(root_template)
    xml_create.find('filename').text = filename
    xml_create.find('size/width').text = str(width)
    xml_create.find('size/height').text = str(height)
    xml_create.find('size/depth').text = str(depth)
    for obj in objs:
        create_obj = ET.fromstring(obj_template)
        create_obj.find('name').text = obj['name']
        create_obj.find('bndbox/xmin').text = str(obj['xmin'])
        create_obj.find('bndbox/ymin').text = str(obj['ymin'])
        create_obj.find('bndbox/xmax').text = str(obj['xmax'])
        create_obj.find('bndbox/ymax').text = str(obj['ymax'])
        xml_create.append(create_obj)
    ET.indent(xml_create)
    return ET.tostring(xml_create)


def xywh2xyxy(x, y, w, h, width, height):
    xmin = x * width - w * width / 2
    xmin = round(xmin)

    xmax = x * width + w * width / 2
    xmax = round(xmax)

    ymin = y * height - h * height / 2
    ymin = round(ymin)

    ymax = y * height + h * height / 2
    ymax = round(ymax)

    return xmin, ymin, xmax, ymax


def xyxy2xywh(xmin, ymin, xmax, ymax, width, height):
    x = (xmin + xmax) / 2 / width
    y = (ymin + ymax) / 2 / height
    w = (xmax - xmin) / width
    h = (ymax - ymin) / height
    return x, y, w, h


if __name__ == "__main__":
    classes = ['sicktree']
    imgpath_dir = r"/data/mnt_share/jpg/2022.10.4/jpg_cut/20220928-旋翼-龙泉-jpg(全已拼好)-1kx1k"
    txt_dir = r"/home/zhaogan/yolov5-6.1/runs/detect/20220928-旋翼-龙泉-jpg(全已拼好)-1kx1k"
    save_dir = r"/data/mnt_share/jpg/2022.10.4/jpg_conf/20220928-旋翼-龙泉"

    imgpath_list = os.listdir(imgpath_dir)

    for img_list in imgpath_list:
        if imghdr.what(os.path.join(imgpath_dir, img_list)) in imgType_list:
            img_path = os.path.join(imgpath_dir, img_list)
            img = cv2.imread(img_path)
            height, width, channel = img.shape
            #print(img_name)
            pre, app = img_list.split(".")
            txt_name = pre + ".txt"
            txt_path = os.path.join(txt_dir, r'labels', txt_name)
            print(txt_path)
            print('*******************************************************')
            if os.path.exists(txt_path):
                print('txtexists')
                objs_list = []
                with open(txt_path, 'r') as f:
                    #print(f)
                    for line in f.readlines():
                        obj_dict = {}
                        info = line.split(" ")
                        #print(line)
                        #print(info)
                        if len(info) == 5:
                            #print('conf is not exist')
                            class_index, x, y, w, h = info
                        elif len(info) == 6:
                            print('conf is exist')
                            class_index, x, y, w, h, conf = info
                        obj_dict['name'] = classes[int(class_index)] + '-{:.2f}'.format(float(conf))
                        xmin, ymin, xmax, ymax = xywh2xyxy(float(x), float(y), float(w), float(h), width, height)
                        obj_dict['xmin'] = xmin
                        obj_dict['ymin'] = ymin
                        obj_dict['xmax'] = xmax
                        obj_dict['ymax'] = ymax
                        #obj_dict['conf'] = conf
                        objs_list.append(obj_dict)
                filename = pre + ".xml"
                xml_string = create_xml(filename, width, height, channel, objs_list)
                if not os.path.exists(save_dir):
                    os.mkdir(save_dir)
                filepath = os.path.join(save_dir, r'annotation')
                if not os.path.exists(filepath):
                    os.mkdir(filepath)
                filepath = os.path.join(save_dir, r'annotation', filename)
                if not os.path.exists(filepath):
                    with open(filepath, "wb") as f:
                        f.write(xml_string)
                        print(txt_path, '========>', filepath)
                # imgnewpath = os.path.join(save_dir, r'images')
                # if not os.path.exists(imgnewpath):
                #     os.mkdir(imgnewpath)
                # imgnewpath = os.path.join(save_dir, r'images', img_list)
                # if not os.path.exists(imgnewpath):
                #     shutil.copy(img_path, imgnewpath)
                #     print(img_path, '========>', imgnewpath)