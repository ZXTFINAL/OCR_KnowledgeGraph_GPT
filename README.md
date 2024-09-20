
# 基于PPOCR和Neo4j的图片转图谱系统
通过大模型的方式进行OCR数据结构化，用于进行后续GraphRag

## 示例图：
![企业微信截图_17268195376606](https://github.com/user-attachments/assets/f1184218-97cb-4feb-be5f-b8a9f853f8a4)
![企业微信截图_17268199422226](https://github.com/user-attachments/assets/6bdbe20d-2ae8-47ff-97b1-2a4f2efdd057)
## 图谱示例
![企业微信截图_17268176432311](https://github.com/user-attachments/assets/32ab414f-c1c2-4ea5-9207-3818b72cf822)
![企业微信截图_17268176054576](https://github.com/user-attachments/assets/5c137c95-38c1-4368-9a95-ae8d5bf0a11b)
![企业微信截图_17268172831927](https://github.com/user-attachments/assets/df177ed0-b389-4723-8091-24c9d3105ef9)

## Getting started
基于ppocr & gpt3.5 & neo4j 
### 部署neo4j
这一部分不赘述，可以参考：https://blog.csdn.net/Andy_shenzl/article/details/134461906
### 部署PPOCR
OCR采用onnx方式部署，加入了行列检测的逻辑，用于识别结构化数据，具体参考
'
ocr_app.py
'
### 脚本启动方式
#1.ocr接口启动方式：
python ocr_app.py

#2.单图片文件测试：
python single_image_detect.py

#3.多图片测试（会写到neo4j）：
python muti_images_detect.py# img2kg
