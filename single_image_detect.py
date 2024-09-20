import requests
import cv2
import gradio as gr
import os
# from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import json


def test(img):
    payload = {'img': img}
    r = requests.post('http://127.0.0.1:5000/ocr', json=payload)
    # print(r.text)
    data = '\n'.join([' | '.join(i) for i in json.loads(r.text)['result']])
    chat = AzureChatOpenAI(
        openai_api_key='xxxxxxxxx',  
        openai_api_version="2023-05-15",
        azure_endpoint="https://azure-openai-test-001-hnlb.openai.azure.com/",
        deployment_name="gpt-35-turbo-16k-hnlb",
    )

    response = chat.invoke([HumanMessage('''你是一个体检报告的文档结构化助手，你需要根据根据文档内容识别出来用户想要知道的信息
                                        查出文档内容包含的检查信息，并通过json形成结构化的数据
                                        json结构按检查项目区分'''+'''{"检查项目":[...]}'''+'''，每个项目的json格式保持一致
                                        文档内容：
                                        {data}
                                        信息为：
                                        '''.format(data=data))])
    print(response.content)
    response = chat.invoke([HumanMessage('''你是一个体检报告文档结构化助手，你需要根据根据文档内容生成知识图谱的三元组数据
                                        文档内容为结构化数据，包含具体的信息，你需要生成知识图谱的三元组或二元组数据
                                        元组信息的重点在于识别检查项目的信息和结论，格式有两种:
                                         1.['S','A','O'] 两个实体之间的联系
                                         2.['S','O'] 单个实体的属性特征
                                        输出格式为json:\n'''
                                         +
                                         '''[
                                         {'S':xxx,
                                         'A':xxx,
                                         'O':xxx},
                                         {'S':xxx,
                                         'O':xxx},
                                         ]\n'''
                                        +
                                        '''文档内容：
                                        {data}
                                        元组信息为：
                                        '''.format(data=response.content))])
    print(response.content)


test('test.png')
