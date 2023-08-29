import os
import os.path
import numpy as np
import xml.etree.ElementTree as xmlET
from PIL import Image, ImageDraw
from tqdm import tqdm


classes=('sicktree1','sicktree2','notree')  # 如果不加后面的',',输出的标签只有一个字符b
# 这里我的图片和xml文件放在同一文件夹了，所以后面用了一个if语句判断是否为标签
file_path_img = r'D:\VOC2012\JPEGImages'
file_path_xml = r'D:\VOC2012\Annotations'
save_file_path = r'D:\VOC2012\visual_boxes'

pathDir = os.listdir(file_path_xml)
print(r'begin\n')
#for idx in range(10):  # 图片过多可以选择只看几张，如果图片跟标签放一起，剔除非标签文件后只输出5张标注图片
for idx in tqdm(range(len(pathDir))):
    filename = pathDir[idx]
    print(filename+r'\n')
    if filename[-3:]=='xml':    # 防止图片跟标签放一起，读取的时候出错，将xml单独放在一个文件夹时可以去掉判断
        tree = xmlET.parse(os.path.join(file_path_xml, filename))
        objs = tree.findall('object')
        num_objs = len(objs)
        boxes = np.zeros((num_objs, 5), dtype=np.uint16)

        for ix, obj in enumerate(objs):
            bbox = obj.find('bndbox')
            # Make pixel indexes 0-based
            x1 = float(bbox.find('xmin').text) - 1
            y1 = float(bbox.find('ymin').text) - 1
            x2 = float(bbox.find('xmax').text) - 1
            y2 = float(bbox.find('ymax').text) - 1

            cla = obj.find('name').text
            label = classes.index(cla)

            boxes[ix, 0:4] = [x1, y1, x2, y2]
            boxes[ix, 4] = label

        image_name = os.path.splitext(filename)[0]
        img = Image.open(os.path.join(file_path_img, image_name + '.jpg'))

        draw = ImageDraw.Draw(img)
        for ix in range(len(boxes)):
            xmin = int(boxes[ix, 0])
            ymin = int(boxes[ix, 1])
            xmax = int(boxes[ix, 2])
            ymax = int(boxes[ix, 3])
            if classes[boxes[ix, 4]] == 'sicktree1' or classes[boxes[ix, 4]] == 'sicktree2':
                print('image_name:' + image_name + 'clsname:' + classes[boxes[ix, 4]] + r'\n')
                clsname = r'sicktree'
                draw.rectangle([xmin, ymin, xmax, ymax], outline=(0, 255, 0))
                draw.text([xmin, ymin - 10], clsname, (0, 255, 0))
            if classes[boxes[ix, 4]] =='notree':
                print('image_name:' + image_name + 'clsname:' + classes[boxes[ix, 4]] + r'\n')
                clsname = r'notree'
                #continue
                draw.rectangle([xmin, ymin, xmax, ymax], outline=(0, 0, 255))
                draw.text([xmin, ymin - 10], clsname, (0, 0, 255))
            #draw.rectangle([xmin, ymin, xmax, ymax], outline=(0, 255, 0))
            #draw.text([xmin, ymin-10], clsname, (0, 255, 0))

        img.save(os.path.join(save_file_path, image_name + '.png'))
