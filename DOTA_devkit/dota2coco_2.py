import json
import dota_utils as util
import os
from PIL import Image

info = {"description": "DOTA dataset from WHU", "url": "http://caption.whu.edu.cn", "year": 2018, "version": "1.0"}
licenses = {"url": "http://creativecommons.org/licenses/by-nc/2.0/", "id": 1,
            "name": "Attribution-NonCommercial License"}
categories = []
for i, catName in enumerate(util.wordname_15, start=1):
    categories.append({"id": i, "name": "%s" % catName, "supercategory": "%s" % catName})

images = []
annotations = []
aug = "/home/lxy/dota/data/aug"
augmented = "/home/lxy/dota/data/augmented"
train_small = "/home/lxy/dota/data/train_small"
trainsplit_HBB = "/home/lxy/dota/data/trainsplit_HBB"
val_small = "/home/lxy/dota/data/val_small"
valsplit_HBB = "/home/lxy/dota/data/valsplit_HBB"
dataset_path = [augmented, train_small, trainsplit_HBB, val_small, valsplit_HBB]
imgid = 0
annid = 0
for path in dataset_path:
    img_path = os.path.join(path, "images")
    label_path = os.path.join(path, "labelTxt")
    for file in os.listdir(label_path):
        img_name = file.replace("txt", "png")
        im = Image.open(os.path.join(img_path, img_name))
        w, h = im.size
        imgid += 1
        images.append({"license": 1, "file_name": "%s" % img_name, \
                       "height": h, "width": w, "id": imgid})

        f = open(os.path.join(label_path, file))
        for line in f.readlines():
            line = "".join(line).strip("\n").split(" ")
            # a bbox has 4 points, a category name and a difficulty
            if len(line) != 10:
                print(path, file)
            else:
                annid += 1
                catid = util.wordname_15.index(line[-2]) + 1
                w_bbox = int(line[4][:-2]) - int(line[0][:-2])
                h_bbox = int(line[5][:-2]) - int(line[1][:-2])
                bbox = [line[0], line[1], str(w_bbox) + '.0', str(h_bbox) + '.0']
                annotations.append({"id": annid, "image_id": imgid, "category_id": catid, \
                                    "segmentation": [line[0:8]], "area": float(w_bbox * h_bbox), \
                                    "bbox": bbox, "iscrowd": 0})

        f.close()

my_json = {"info": info, "licenses": licenses, "images": images, "annotations": annotations, "categories": categories}

with open("/home/lxy/dota/data/coco/annotations/train.json", "w+") as f:
    json.dump(my_json, f)
    print("writing json file done!")