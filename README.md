# Annotations_Tool
A personal tool for transforming annotations among rolabelImg and DOTA and so on

Classic style of rolabelImg:
https://github.com/cgvict/roLabelImg

<annotation verified="no">
  <folder>JPEGImages</folder>
  <filename>17</filename>
  <path>*****</path>
  <source>
    <database>Unknown</database>
  </source>
  <size>
    <width>4800</width>
    <height>2843</height>
    <depth>3</depth>
  </size>
  <segmented>0</segmented>
  <object>
    <type>robndbox</type>
    <name>***</name>
    <pose>Unspecified</pose>
    <truncated>0</truncated>
    <difficult>0</difficult>
    <robndbox>
      <cx>2747.5</cx>
      <cy>588.2051</cy>
      <w>111.6403</w>
      <h>1322.4623</h>
      <angle>0.59</angle>
    </robndbox>
  </object>
</annotation>


Where angle θ:[0,pi/2), which is the angle 

and DOTA style:
see https://captain-whu.github.io/DOTA/dataset.html
x1, y1, x2, y2, x3, y3, x4, y4, category, difficult
Note that the points are arranged in a clockwise order.

So my method is:
1)Calculate xmin,ymin,xmax,ymax, and you will find they correspond to 4 points of OBB like (x1,ymin) (xmax,y2) (x3,ymax) (x4,ymin) in a clockwise order(when θ<pi/2);
2)Choose a first-point as (x1,y1) and alculate 4 points;For me ,I choose top-left point(x1,ymin) when θ<pi/2 and (xmax,y1) when θ>=pi/2
3)Store the xml to txt.


More about OBB:
https://zhuanlan.zhihu.com/p/459018810



