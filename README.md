# Annotations_Tool
A personal tool for transforming annotations among rolabelImg and DOTA and so on

### New(2022.10.21) : Add `DOTA_devkit` contains DOTA2COCO(object detection) style~

Classic style of rolabelImg:
https://github.com/cgvict/roLabelImg
## sososo useful :smile: ——THC
![image](https://user-images.githubusercontent.com/72430633/187375382-3d6e1911-1c41-44e3-a5b3-a7d4bd12ac08.png)


Where angle θ:[0,pi/2), which is the angle 

and DOTA style:
see https://captain-whu.github.io/DOTA/dataset.html

x1, y1, x2, y2, x3, y3, x4, y4, category, difficult

Note that the points are arranged in a clockwise order.

So my method is:

1)Calculate xmin,ymin,xmax,ymax, and you will find they correspond to 4 points of OBB like (x1,ymin) (xmax,y2) (x3,ymax) (x4,ymin) in a clockwise order(when θ<pi/2);

2)Choose a first-point as (x1,y1) and alculate 4 points;For me ,I choose top-left point(x1,ymin) when θ<pi/2 and (xmax,y1) when θ>=pi/2;

3)Store the xml to txt.


More about OBB:
https://zhuanlan.zhihu.com/p/459018810



