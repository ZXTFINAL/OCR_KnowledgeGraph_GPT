from ppocronnx.predict_system import TextSystem
import cv2
import json
import numpy as np
from flask import Flask, request, jsonify
import operator
from math import sqrt
import pandas as pd
text_sys = TextSystem(thread_num=10)
app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr_handler():
    if request.method == 'POST':
        json_data = request.get_json()
        image_path = json_data['img']

        img = cv2.imread(image_path)

        img = img[:img.shape[1]*3,:img.shape[1],:]
        res = text_sys.detect_and_ocr(img)
        ocr_result = []
        row_data = []
        rows = []

        col_data = []
        cols = []
        for c, boxed_result in enumerate(res):
            print("{}, {:.3f}".format(boxed_result.ocr_text, boxed_result.score))
            box = np.array(boxed_result.box)
            min_x,max_x,min_y,max_y = min(box[:,0]),max(box[:,0]),min(box[:,1]),max(box[:,1])
            mid_x,mid_y = (min_x+max_x)/2,(min_y+max_y)/2

            if not rows:
                rows.append([[boxed_result,min_x,max_x,min_y,max_y,mid_x,mid_y,c]])
                row_data.append(min_y)
            else:
                flag = 0
                for key,value in enumerate(row_data):
                    if abs(value-min_y)<((max_y-min_y)):
                        rows[key].append([boxed_result,min_x,max_x,min_y,max_y,mid_x,mid_y,c])
                        row_data[key] = min_y
                        flag = 1
                        break
                    elif value-min_y>0:
                        rows.insert(key,[[boxed_result,min_x,max_x,min_y,max_y,mid_x,mid_y,c]])
                        row_data.append(min_y)
                        flag = 1
                        break
                if not flag:
                    rows.append([[boxed_result,min_x,max_x,min_y,max_y,mid_x,mid_y,c]])
                    row_data.append(min_y)

                      
            

            ocr_result.append(boxed_result.ocr_text)
        def takeSecond(elem):
            return elem[1]
        for row in rows:
            row.sort(key=takeSecond,reverse=False)
        num_col = max([len(i) for i in rows])
        data = np.zeros([len(rows),num_col])
        data = np.array(data,dtype=str)
        max_col = 0
        max_col_idx = []
        for rdx,row in enumerate(rows):
            data[rdx] = ['']*num_col
            if len(row)>=max_col:
                for cdx,col in enumerate(row):

                    data[rdx,cdx] = col[0].ocr_text
                max_col = len(row)
                max_col_idx = [i[1] for i in row]
            else:
                for cdx,col in enumerate(row):
                    match_idx = np.argmax([-1*abs(col[1]-max_col_idx) for i in max_col_idx])
                    data[rdx,match_idx] += col[0].ocr_text
        print(data)
        # pd.DataFrame(data).to_csv('test.csv',index=False)
        return json.dumps({'result': data.tolist()},ensure_ascii=False)
 
if __name__ == '__main__':
    app.run('0.0.0.0')