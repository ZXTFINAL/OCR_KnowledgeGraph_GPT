import requests
import cv2
import gradio as gr
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import json
from py2neo import Node, Graph, Relationship

class DataToNeo4j(object):
    """将excel中数据存入neo4j"""
    def __init__(self):
        """建立连接"""
        link = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
        self.graph = link
        # self.graph = NodeMatcher(link)
        self.graph.delete_all()

    def create_spo(self,result):
        start = Node(type='entity',name = result[0])
        end = Node(type='entity',name = result[2])
        self.graph.create(start)
        self.graph.create(end)
        r1 = Relationship(start, result[1], end)
        self.graph.create(r1)
    def create_node(self, name_node, type_node):
        """建立节点"""
        nodes = []
        for name_sentence, type_sentence in zip(name_node, type_node):
            nodes_sentence = []
            # for name_word, type_word in zip(name_sentence, type_sentence):
            # 创建节点
            node = Node(type_sentence, name =name_sentence )
            self.graph.create(node)
            # 保存下来
            nodes_sentence.append(node)
            nodes.append(nodes_sentence)

        print('节点建立成功')
        return nodes


    def create_relation(self, word):
        """建立联系"""

        try:
            # 关系要转化成字符串格式
            r = Relationship(word[0], word[1], word[2])
            self.graph.create(r)
        except AttributeError as e:
            print(e)

        print('关系建立成功')




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
                                         'A':xxx},
                                         ]\n'''
                                        +
                                        '''文档内容：
                                        {data}
                                        元组信息为：
                                        '''.format(data=response.content))])
    print(response.content)



    
    results = eval(response.content)
    alldata = {}
    for result in results:
        temp = result.copy()
        for i in temp:
            if not result[i]:
                result.pop(i)
        if len(list(result.keys()))==3 and '' not in list(result.keys()):

            try:
                if result['S'] not in alldata: 
                    nodes = spo.create_node([result['S']],type_node=['S'])
                    alldata[result['S']] = nodes
                if result['O'] not in alldata: 
                    nodes = spo.create_node([result['O']],type_node=['O'])
                    alldata[result['O']] = nodes
                spo.create_relation([alldata[result['S']][0][0],result['A'],alldata[result['O']][0][0]])

            except:
                if result['S'] not in alldata: 
                    nodes = spo.create_node([result['S']],type_node=['S'])
                    alldata[result['S']] = nodes
                if result['O'] not in alldata: 
                    nodes = spo.create_node([result['O']],type_node=['O'])
                    alldata[result['O']] = nodes
                spo.create_relation([alldata[result['S']][0][0],'属性',alldata[result['O']][0][0]])

        else:
            if result['S'] not in alldata: 
                nodes = spo.create_node([result['S']],type_node=['S'])
                alldata[result['S']] = nodes
            try:
                if result['O'] not in alldata: 
                    nodes = spo.create_node([result['O']],type_node=['O'])
                    alldata[result['O']] = nodes
                spo.create_relation([alldata[result['S']][0][0],'属性',alldata[result['O']][0][0]])
            except:
                if result['A'] not in alldata: 
                    nodes = spo.create_node([result['A']],type_node=['A'])
                    alldata[result['A']] = nodes
                spo.create_relation([alldata[result['S']][0][0],'属性',alldata[result['A']][0][0]])

    print('-' * 100)

    # response = chat.invoke([HumanMessage('''你是一个体检报告文档结构化助手，你需要根据根据文档内容识别出来用户想要知道的信息
    #                                     文档内容为结构化数据，包含具体的信息，你需要按照用户想知道的key进行查询，如果没有请返回"无信息",格式为:target1:info1|target2:info2
    #                                     文档内容：
    #                                     {data}
    #                                     用户想知道的信息：
    #                                     {target}
    #                                     查找出来的信息：'''.format(data=response.content,target=['用户信息']))])
    # print(response.content)
    # response = chat.invoke([HumanMessage('''你是一个体检报告文档结构化助手，你需要根据根据文档内容识别出来用户想要知道的信息
    #                                     文档内容为结构化数据，包含具体的信息，你需要按照用户想知道的key进行查询，如果没有请返回"无信息",格式为:target1:info1|target2:info2
    #                                     文档内容：
    #                                     {data}
    #                                     用户想知道的信息：
    #                                     {target}
    #                                     查找出来的信息：'''.format(data=response.content,target=['检查项目']))])
    # print(response.content)
    # response = chat.invoke([HumanMessage('''你是一个体检报告文档结构化助手，你需要根据根据文档内容识别出来用户想要知道的信息
    #                                     文档内容为结构化数据，包含具体的信息，你需要按照用户想知道的key进行查询，如果没有请返回"无信息",格式为:target1:info1|target2:info2
    #                                     文档内容：
    #                                     {data}
    #                                     用户想知道的信息：
    #                                     {target}
    #                                     查找出来的信息：'''.format(data=response.content,target=['结论']))])
    # print(response.content)
if __name__=='__main__':
    spo = DataToNeo4j()
    filenames = [i for i in os.listdir('./tjbg_2/')]
    filenames.sort()
    for i in filenames:
        print(i)
        test('tjbg_2/'+i)

