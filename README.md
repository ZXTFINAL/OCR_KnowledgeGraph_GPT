
# 基于PPOCR和Neo4j的图片转图谱系统
通过大模型的方式进行OCR数据结构化，用于进行后续GraphRag

## 示例图：
![企业微信截图_17268195376606](https://github.com/user-attachments/assets/70023229-b43b-4624-95ab-3ebd12827da0)
![企业微信截图_17268199422226](https://github.com/user-attachments/assets/30c9c58f-eec4-4f83-8164-f2967800928b)
![企业微信截图_17268176432311](https://github.com/user-attachments/assets/61b06691-887b-4422-a126-8da028620e1d)
![企业微信截图_17268172831927](https://github.com/user-attachments/assets/616d9511-0823-47aa-9100-123f9e1b6e4e)
![企业微信截图_17268176054576](https://github.com/user-attachments/assets/c7e8b281-217d-442e-bfc7-9241c850c2c2)

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
