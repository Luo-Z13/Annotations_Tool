import os
import cv2
from xml.dom.minidom import Document
import math

# # windows下无需
# import sys
#
# stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
# reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde

category_set =['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship', 'tennis-court',
               'basketball-court', 'storage-tank',  'soccer-ball-field', 'roundabout', 'harbor', 'swimming-pool', 'helicopter']


def custombasename(fullname):
    return os.path.basename(os.path.splitext(fullname)[0])


def limit_value(a, b):
    if a < 1:
        a = 1
    if a >= b:
        a = b - 1
    return a


def readlabeltxt(txtpath, height, width, hbb):
    print(txtpath)
    with open(txtpath, 'r') as f_in:  
        lines = f_in.readlines()
        splitlines = [x.strip().split(' ') for x in lines]  
        boxes = []
        for i, splitline in enumerate(splitlines):
            # if i in [0, 1]: 
            #     continue
            label = splitline[8]
            if label not in category_set:  
                continue
            x1 = int(float(splitline[0]))
            y1 = int(float(splitline[1]))
            x2 = int(float(splitline[2]))
            y2 = int(float(splitline[3]))
            x3 = int(float(splitline[4]))
            y3 = int(float(splitline[5]))
            x4 = int(float(splitline[6]))
            y4 = int(float(splitline[7]))
            # 如果是hbb
            if hbb:
                xx1 = min(x1, x2, x3, x4)
                xx2 = max(x1, x2, x3, x4)
                yy1 = min(y1, y2, y3, y4)
                yy2 = max(y1, y2, y3, y4)

                xx1 = limit_value(xx1, width)
                xx2 = limit_value(xx2, width)
                yy1 = limit_value(yy1, height)
                yy2 = limit_value(yy2, height)

                box = [xx1, yy1, xx2, yy2, label]
                boxes.append(box)
            else:  # 否则是obb
                x1 = limit_value(x1, width)
                y1 = limit_value(y1, height)
                x2 = limit_value(x2, width)
                y2 = limit_value(y2, height)
                x3 = limit_value(x3, width)
                y3 = limit_value(y3, height)
                x4 = limit_value(x4, width)
                y4 = limit_value(y4, height)

                box = [x1, y1, x2, y2, x3, y3, x4, y4, label]
                boxes.append(box)
    return boxes


# roLabelImg格式
def writeXml(tmp, imgname, w, h, d, bboxes, hbb):
    doc = Document()
    # owner
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)
    # owner
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder_txt = doc.createTextNode("images")
    folder.appendChild(folder_txt)

    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename_txt = doc.createTextNode(imgname)
    filename.appendChild(filename_txt)
    # ones#
    source = doc.createElement('source')
    annotation.appendChild(source)

    database = doc.createElement('database')
    source.appendChild(database)
    database_txt = doc.createTextNode("My Database")
    database.appendChild(database_txt)

    annotation_new = doc.createElement('size')
    source.appendChild(annotation_new)

    img_width = doc.createElement("width")
    annotation_new.appendChild(img_width)
    width_txt = doc.createTextNode(str(w))
    img_width.appendChild(width_txt)
    img_height = doc.createElement("height")
    annotation_new.appendChild(img_height)
    height_txt = doc.createTextNode(str(h))
    img_height.appendChild(height_txt)
    img_depth = doc.createElement("depth")
    annotation_new.appendChild(img_depth)
    depth_txt = doc.createTextNode(str(d))
    img_width.appendChild(depth_txt)

    segmented = doc.createElement('segmented')
    source.appendChild(segmented)
    segmented_txt = doc.createTextNode("0")
    segmented.appendChild(segmented_txt)


    for bbox in bboxes:
        # threes#
        object_new = doc.createElement("object")
        annotation.appendChild(object_new)

        type= doc.createElement('type')
        object_new.appendChild(type)
        type_txt = doc.createTextNode("robndbox")
        type.appendChild(type_txt)

        name = doc.createElement('name')
        object_new.appendChild(name)
        name_txt = doc.createTextNode(str(bbox[-1]))
        name.appendChild(name_txt)

        pose = doc.createElement('pose')
        object_new.appendChild(pose)
        pose_txt = doc.createTextNode("Unspecified")
        pose.appendChild(pose_txt)

        truncated = doc.createElement('truncated')
        object_new.appendChild(truncated)
        truncated_txt = doc.createTextNode("0")
        truncated.appendChild(truncated_txt)

        difficult = doc.createElement('difficult')
        object_new.appendChild(difficult)
        difficult_txt = doc.createTextNode("0")
        difficult.appendChild(difficult_txt)
        # threes-1#
        robndbox = doc.createElement('robndbox')
        object_new.appendChild(robndbox)

        if hbb:
            xmin = doc.createElement('xmin')
            robndbox.appendChild(xmin)
            xmin_txt = doc.createTextNode(str(bbox[0]))
            xmin.appendChild(xmin_txt)

            ymin = doc.createElement('ymin')
            robndbox.appendChild(ymin)
            ymin_txt = doc.createTextNode(str(bbox[1]))
            ymin.appendChild(ymin_txt)

            xmax = doc.createElement('xmax')
            robndbox.appendChild(xmax)
            xmax_txt = doc.createTextNode(str(bbox[2]))
            xmax.appendChild(xmax_txt)

            ymax = doc.createElement('ymax')
            robndbox.appendChild(ymax)
            ymax_txt = doc.createTextNode(str(bbox[3]))
            ymax.appendChild(ymax_txt)
        else:
            x0=bbox[0]
            y0=bbox[1]
            x1 = bbox[2]
            y1 = bbox[3]
            x2 = bbox[4]
            y2 = bbox[5]
            x3 = bbox[6]
            y3 = bbox[7]

            centerx=(x0+x1+x2+x3)/4
            centery = (y0 + y1 + y2 + y3) / 4
            w_len=math.sqrt(pow((x1-x2),2)+pow((y1-y2),2))
            h_len = math.sqrt(pow((x3 - x2), 2) + pow((y3 - y2), 2))

            deltax=x2-x1
            deltay=y2-y1
            theta=0

            if deltax>0 and deltay>0:
                theta=math.atan(deltay/deltax)
            elif deltax>0 and deltay<0:
                theta=math.atan(math.fabs(deltay)/deltax)+math.pi/2
            elif deltax==0:
                theta=math.pi/2
            elif deltay==0:
                theta=0

            cx = doc.createElement('cx')
            robndbox.appendChild(cx)
            cx_txt = doc.createTextNode(str(centerx))
            cx.appendChild(cx_txt)

            cy = doc.createElement('cy')
            robndbox.appendChild(cy)
            cy_txt = doc.createTextNode(str(centery))
            cy.appendChild(cy_txt)

            w = doc.createElement('w')
            robndbox.appendChild(w)
            w_txt = doc.createTextNode(str(w_len))
            w.appendChild(w_txt)

            h = doc.createElement('h')
            robndbox.appendChild(h)
            h_txt = doc.createTextNode(str(h_len))
            h.appendChild(h_txt)

            angle = doc.createElement('angle')
            robndbox.appendChild(angle)
            angle_txt = doc.createTextNode(str(theta))
            angle.appendChild(angle_txt)


    xmlname = os.path.splitext(imgname)[0]
    tempfile = os.path.join(tmp, xmlname + '.xml')
    with open(tempfile, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
    return


if __name__ == '__main__':
    data_path='data_path'
    out_path='labelTxt/'

    count=0

    with open(data_path, 'r', encoding='gbk') as f_in:  #
        merge_lines = f_in.readlines()

        for i, lines in enumerate(merge_lines):
        
            line=lines.strip().split(' ') 
            img_path = line[0]
            filename=str(img_path).split('/')[-1].split('.')[0]+'.txt'
            f = open(os.path.join(out_path, filename), 'w')

            boxes = []
            img_path = line[0]
            annos_merge = line[1:]
            for annos in annos_merge:
                anno = annos
                anno = anno.split(',')
                x1 = anno[0]
                y1 = anno[1]
                x2 = anno[2]
                y2 = anno[3]
                x3 = anno[4]
                y3 = anno[5]
                x4 = anno[6]
                y4 = anno[7]
                classname = anno[8]

                img_path = ' '
                f.write(str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' '
                        + str(x3) + ' ' + str(y3) + ' ' + str(x4) + ' ' + str(y4) + ' ' + classname +
                        ' ' + '0' + '\n')
                count+=1

            f.close()

    print("Instance num:", count)

