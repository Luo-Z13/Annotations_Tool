import os
import xml.etree.ElementTree as ET
import math


def robndbox2_4points(cx, cy, w, h, angle):
    # 对旋转框的标注进行格式转换
    # 转换为旋转框的4个角点，顺时针0123

    ####下面以矩形的左上角点为起始点顺时针计算
    Pi=math.pi
    if angle<Pi/2:
        theta=angle
        # 注释部分为θ<pi/2的形状的情况：
        # y1=ymin
        # x1=xmax-w*math.cos(theta)
        x1 = cx - math.cos(theta) * (w / 2) + math.sin(theta) * (h / 2)
        y1 = cy - math.sin(theta) * (w / 2) - math.cos(theta) * (h / 2)

        # x2=xmax
        # y2=ymin+wsin(theta)
        x2 = cx + math.cos(theta) * (w / 2) + math.sin(theta) * (h / 2)
        y2 = cy + math.sin(theta) * (w / 2) - math.cos(theta) * (h / 2)

        # y3=ymax
        # x3=xmin+wcos(theta)
        x3 = cx + math.cos(theta) * (w / 2) - math.sin(theta) * (h / 2)
        y3 = cy + math.sin(theta) * (w / 2) + math.cos(theta) * (h / 2)

        # x4=xmin
        # y4=ymax-wsin(theta)
        x4 = cx - math.cos(theta) * (w / 2) - math.sin(theta) * (h / 2)
        y4 = cy - math.sin(theta) * (w / 2) + math.cos(theta) * (h / 2)

    else:
        theta=angle-Pi/2  #转换为h边与x轴的夹角，此时即w,h定义互换
        # 注释部分为θ>=pi/2的形状的情况：
        # x1=xmax
        # y1=ymin+hsin(theta)
        x1 = cx + math.cos(theta) * (h / 2) + math.sin(theta) * (w / 2)
        y1 = cy + math.sin(theta) * (h / 2) - math.cos(theta) * (w / 2)

        # y2=ymax
        # x2=xmin+hcos(theta)
        x2 = cx + math.cos(theta) * (h / 2) - math.sin(theta) * (w / 2)
        y2 = cy + math.sin(theta) * (h / 2) + math.cos(theta) * (w / 2)

        # x3=xmin
        # y3=ymin+wcos(theta)
        x3 = cx - math.cos(theta) * (h / 2) - math.sin(theta) * (w / 2)
        y3 = cy - math.sin(theta) * (h / 2) + math.cos(theta) * (w / 2)
        # y4=ymin
        # x4=xmax-h*math.cos(theta)
        x4 = cx - math.cos(theta) * (h / 2) + math.sin(theta) * (w / 2)
        y4 = cy - math.sin(theta) * (h / 2) - math.cos(theta) * (w / 2)


    x1 = math.modf(round(x1))[1]  # 取整后保留一位小数
    y1 = math.modf(round(y1))[1]
    x2 = math.modf(round(x2))[1]
    y2 = math.modf(round(y2))[1]
    x3 = math.modf(round(x3))[1]
    y3 = math.modf(round(y3))[1]
    x4 = math.modf(round(x4))[1]
    y4 = math.modf(round(y4))[1]

    return x1, y1, x2, y2, x3, y3, x4, y4


################################

##将rolabelImg格式的旋转标注(x,y,w,h,θ)转换为4点坐标表示形式
def robndbox_to_bndbox_4pts(path, out_path):
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    count = 0  #文件计数
    misses = 0

    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            count+=1
            in_file = open(os.path.join(path, file), encoding='utf-8')
            tree = ET.parse(in_file)
            root = tree.getroot()

            # tree.write(os.path.join(out_path, file), encoding="utf-8")
            filename = file.split('.')[0] + '.txt'
            f = open(os.path.join(out_path, filename), 'w')

            find = 0
            for obj in root.iter('object'):
                name=obj.find('name')
                class_name=name.text

                ##transform
                xmlbox = obj.find('robndbox')
                cx = float(xmlbox.find('cx').text)
                cy = float(xmlbox.find('cy').text)
                w = float(xmlbox.find('w').text)
                h = float(xmlbox.find('h').text)
                angle = float(xmlbox.find('angle').text)
                # obj.remove(xmlbox)  # 移除旋转框节点
                # 格式转换
                x1, y1, x2, y2, x3, y3, x4, y4 = robndbox2_4points(cx, cy, w, h, angle)
                find=find+1

                # 写新文件
                f.write(str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' '
                        + str(x3) + ' ' + str(y3) + ' ' + str(x4) + ' ' + str(y4) + ' ' + class_name + ' ' + str(
                    0) + '\n')

            f.close()
            if find == 0:
                print('miss ' + file.split('.')[0])
                misses += 1


    print("Transform xml files from rolabelImg to dota style!")
    print("转换", count - misses, "个文件!!")



if __name__ == '__main__':
    raw_path = "annotations"
    out_path = "annotations_DOTA_txt"
    #####下面将rolabeiImg格式(cx,cy,w,h,θ)转化为DOTA数据集的txt格式
    ####在rolabelImg的标注格式中,角度angle范围是[0,pi)
    robndbox_to_bndbox_4pts(raw_path,out_path)
    print('down!')


