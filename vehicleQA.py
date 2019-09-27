# -*- coding: utf-8 -*-
'''
create in 20190828
only three tuples
perform not good in recommend
'''
import random
from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher
import json
import jieba
jieba.load_userdict("./data/usr_dict.txt")
import jieba.posseg as pseg

class searchCarInNeo4j():

    def __init__(self):
        with open('./data/synonymDict.json','r') as f:
            dict_synonym = json.load(f)
        self.dict_ci = dict_synonym['ci']
        self.dict_vi = dict_synonym['vi']
        self.dict_vm = dict_synonym['vm']
        #self.dict_ri = dict_synonym['ri']
        self.dict_city = dict_synonym['city']
        self.dict_area = dict_synonym['area']
        self.dict_manu = dict_synonym['manu']
        self.mark_list = ['ci','vm','vi','ri','city','area','manu','kd']
        self.kg = Graph("bolt://localhost:7687", auth=('neo4j', '123456'))
        #self.kg = Graph("http://localhost:3389", username="neo4j", password="123456")
        self.introduction = {'CI':'配件','RI':'限制','VI':'车型信息','LO1':'city','LO2':'area','DE':'经销商','VM':'车型','KD':'品牌'}

    def searchOneComp(self,carmodel,entity):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})-->(b:car)-->(c:ci {name:'"+entity[0]+"'}) RETURN b.carname,c.value").data()
        if result_list == []:
            answer = ['没有找到相关信息']
        else:
            answer.append(result)
            for i in result_list:
                if '国VI' in i['b.carname']:
                    result = i['b.carname']+'--'+i['c.value']+'--'+entity[0]
                    answer.append(result)
                elif '国V' in i['b.carname']:
                    pass
                else:
                    result = i['b.carname']+'--'+i['c.value']+'--'+entity[0]
                    answer.append(result)
        return answer

    def searchOneVichleInfo(self,carmodel,entity):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})-->(b:car)-->(c:ci {name:'"+entity[0]+"'}) RETURN b.carname,c.value").data()
        if result_list == []:
            result = '没有找到相关信息'
            answer.append(result)
        else:
            answer.append(result)
            for i in result_list:
                if '国VI' in i['b.carname']:
                    result = i['b.carname']+'的'+entity[0]+'是'+i['c.value']
                    answer.append(result)
                elif '国V' in i['b.carname']:
                    pass
                else:
                    result = i['b.carname']+'的'+entity[0]+'是'+i['c.value']
                    answer.append(result)
        return answer

    def searchVMLODE(self,carmodel,entity):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})<--(b:manu)-->(c:dealer)<-[:has*1..2]-(d:city {name:'"+entity[0]+"'}) RETURN c.address,c.city,c.dealer,c.phone,c.area").data()
        if result_list == []:
            result = '没有找到相关信息'
            answer.append(result)
        else:
            answer.append(result)
            for i in result_list:
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address']
                answer.append(result)
        return answer

    def searchVMArea(self,carmodel,entity):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})<--(b:manu)-->(c:dealer)<--(d:area {name:'"+entity[0]+"'}) RETURN c.address,c.city,c.dealer,c.phone,c.area").data()
        if result_list == []:
            result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})<--(b:manu)-->(c:dealer)<-[:has*1..2]-(e:city),(f:area {name:'"+entity[0]+"'})<--(e:city) RETURN c.address,c.city,c.dealer,c.phone,c.area").data()
            result = '没有在'+entity[0]+'范围内找到相关经销商，不过不用担心，小柯基自动为您扩大搜索范围，找到如下信息：'
        if result_list == []:
            result = '没有找到相关信息'
            answer.append(result)
        else:
            answer.append(result)
            for i in result_list:
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address']
                answer.append(result)
        return answer

    def searchCityArea(self,carmodel, entity1, entity2):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})<--(b:manu)-->(c:dealer)<--(d:area {name:'"+entity2[0]+"'})<--(e:city {name:'"+entity1[0]+"'}) RETURN c.address,c.city,c.dealer,c.phone,c.area").data()
        if result_list == []:
            result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})<--(b:manu)-->(c:dealer)<-[:has*1..2]-(d:city {name:'"+entity1[0]+"'}) RETURN c.address,c.city,c.dealer,c.phone,c.area").data()
            result = '没有在'+entity2[0]+'范围内找到相关经销商，不过不用担心，小柯基自动为您扩大搜索范围，找到如下信息：'
        if result_list == []:
            result = '没有找到相关信息'
            answer.append(result)
        else:
            answer.append(result)
            for i in result_list:
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address']
                answer.append(result)
        return answer

    def searchManuCity(self,manu,entity):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (b:manu {manu:'"+manu+"'})-->(c:dealer)<-[:has*1..2]-(d:city {name:'"+entity[0]+"'}) RETURN c.address,c.city,c.dealer,c.phone,c.area").data()
        if result_list == []:
            result = '没有找到相关信息'
            answer.append(result)
        else:
            answer.append(result)
            for i in result_list:
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address']
                answer.append(result)
        return answer
    
    def searchManuArea(self,manu,entity):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (b:manu {manu:'"+manu+"'})-->(c:dealer)<--(d:area {name:'"+entity[0]+"'}) RETURN c.address,c.city,c.dealer,c.phone,c.area").data()
        if result_list == []:
            result_list = self.kg.run("MATCH (b:manu {manu:'"+manu+"'})-->(c:dealer)<-[:has*1..2]-(e:city),(f:area {name:'"+entity[0]+"'})<--(e:city) RETURN c.address,c.city,c.dealer,c.phone,c.area").data()
            result = '没有在'+entity[0]+'范围内找到相关经销商，不过不用担心，小柯基自动为您扩大搜索范围，找到如下信息：'
        if result_list == []:
            result = '没有找到相关信息'
            answer.append(result)
        else:
            answer.append(result)
            for i in result_list:
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address']
                answer.append(result)
        return answer

    def searchTwoComp(self,carmodel,entity):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})-->(b:car)-->(c:ci {name:'"+entity[0]+"'}),(b:car)-->(d:ci {name:'"+entity[1]+"'}) RETURN b.carname,c.value,d.value").data()
        if result_list == []:
            result = '没有找到相关信息'
            answer.append(result)
            #print(result)
        else:
            answer.append(result)
            for i in result_list:
                if '国VI' in i['b.carname']:
                    result =  i['b.carname']+' '+i['c.value']+' '+entity[0]+' '+i['d.value']+' '+entity[1]
                    answer.append(result)
                elif '国V' in i['b.carname']:
                    pass
                else:
                    result =  i['b.carname']+' '+i['c.value']+' '+entity[0]+' '+i['d.value']+' '+entity[1]
                    answer.append(result)
        return answer

    def searchTwoVI(self,carmodel,entity):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})-->(b:car)-->(c:ci {name:'"+entity[0]+"'}),(b:car)-->(d:ci {name:'"+entity[1]+"'}) RETURN b.carname,c.value,d.value").data()
        if result_list == []:
            result = '没有找到相关信息'
            answer.append(result)
            #print(result)
        else:
            answer.append(result)
            for i in result_list:
                if '国VI' in i['b.carname']:
                    result =  i['b.carname']+'的'+entity[0]+'是'+i['c.value']+';'+entity[1]+'是'+i['d.value']
                    answer.append(result)
                elif '国V' in i['b.carname']:
                    pass
                else:
                    result =  i['b.carname']+'的'+entity[0]+'是'+i['c.value']+';'+entity[1]+'是'+i['d.value']
                    answer.append(result)
        return answer

    def searchCompVI(self,carmodel,entity1,entity2):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})-->(b:car)-->(c:ci {name:'"+entity1[0]+"'}),(b:car)-->(d:ci {name:'"+entity2[0]+"'}) RETURN b.carname,c.value,d.value").data()
        if result_list == []:
            result = '没有找到相关信息'
            answer.append(result)
            #print(result)
        else:
            answer.append(result)
            for i in result_list:
                if '国VI' in i['b.carname']:
                    result =  i['b.carname']+'的'+entity1[0]+'是'+i['c.value']+';'+i['d.value']+'--'+entity2[0]
                    answer.append(result)
                elif '国V' in i['b.carname']:
                    pass
                else:
                    result =  i['b.carname']+'的'+entity1[0]+'是'+i['c.value']+';'+i['d.value']+'--'+entity2[0]
                    answer.append(result)
        return answer
    
    def searchManuCityArea(self,manu,entity1,entity2):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (b:manu {manu:'"+manu+"'})-->(c:dealer)<--(e:area{name:'"+entity2[0]+"'})<--(d:city {name:'"+entity1[0]+"'}) RETURN c.address,c.city,c.dealer,c.phone,c.area").data()
        if result_list == []:
            result_list = self.kg.run("MATCH (b:manu {manu:'"+manu+"'})-->(c:dealer)<-[:has*1..2]-(d:city {name:'"+entity1[0]+"'}) RETURN c.address,c.city,c.dealer,c.phone,c.area").data()
            result = '没有在'+entity2[0]+'范围内找到相关经销商，不过不用担心，小柯基自动为您扩大搜索范围，找到如下信息：'
        if result_list == []:    
            result = '没有找到相关信息'
            answer.append(result)
        else:
            answer.append(result)
            for i in result_list:
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address']
                answer.append(result)
        return answer

    def searchManu(self,manu):
        answer = []
        result_list = self.kg.run("MATCH (a:manu {manu:'"+manu+"'})-->(b:carmodel) RETURN b.carmodel").data()
        if result_list == []:
            result = '没有找到相关信息'
            answer.append(result)
            #print(result)
        else:
            result = '小柯基为您找到'+manu+'旗下的'+str(len(result_list))+'款车型：'
            answer.append(result)
            for i in result_list:
                result =  i['b.carmodel']
                answer.append(result)
        return answer

    def countParaNum(self,result):
        num_CI, num_VI, num_RI, num_MANU, num_LO1, num_LO2, num_VM, num_KD = 0, 0, 0, 0, 0, 0, 0, 0
        for key,value in result.items():
            if key == 'ci':
                num_CI = len(value)
            if key == 'vi':
                num_VI = len(value)
            if key == 'ri':
                num_RI = len(value)
            if key == 'manu':
                num_MANU = len(value)
            if key == 'vm':
                num_VM = len(value)
            if key == 'kd':
                num_KD = len(value)
            if key == 'city':
                num_LO1 = len(value)
            if key == 'area':
                num_LO2 = len(value)
        return num_CI, num_RI, num_VI, num_MANU, num_LO1, num_LO2,num_VM, num_KD

    def entityRecoByJieba(self, message):
        words = pseg.cut(message)
        result = {}
        counter = {}
        num_CI, num_VI, num_RI, num_manu, num_city, num_area, num_VM, num_KD = 0, 0, 0, 0, 0, 0, 0, 0
        for word, flag in words:
            print(word,flag)
            if flag == 'ci':
                result.setdefault(flag, []).append(self.dict_ci[word])
                num_CI += 1
            elif flag == 'vi':
                result.setdefault(flag, []).append(self.dict_vi[word])
                num_VI += 1
            elif flag == 'vm':
                result.setdefault(flag, []).append(self.dict_vm[word])
                num_VM += 1
            elif flag == 'city':
                result.setdefault(flag, []).append(self.dict_city[word])
                num_city += 1
            elif flag == 'area':
                result.setdefault(flag, []).append(self.dict_area[word])
                num_area += 1
            elif flag == 'manu':
                result.setdefault(flag, []).append(self.dict_manu[word])
                num_manu += 1
            else:
                pass
        counter = {'ci':num_CI, 'vi':num_VI, 'ri':num_RI, 'manu':num_manu, 'city':num_city, 'area':num_area, 'vm':num_VM, 'kd':num_KD}
        total_num = num_CI + num_VI + num_RI + num_manu + num_city + num_area + num_VM + num_KD
        return result,counter,total_num     

    def search(self, message):
        message = message.upper()
        result, counter_jieba, total_num = self.entityRecoByJieba(message)
        #result = self.entityReco()
        #result = self.confirmCarMdoel(result)
        print(result,counter_jieba)
        answer = ['我可能是没听懂你说什么']
        if total_num == 1:
            if counter_jieba['ci'] == 1:
                #配件介绍
                pass
            elif counter_jieba['vi'] == 1:
                #车型信息介绍
                pass
            elif counter_jieba['vm'] == 1:
                answer = self.searchOneVichleInfo(result['vm'][0],['厂商指导价(万元)'])
            elif counter_jieba['manu'] == 1:
                answer = self.searchManu(result['manu'][0])
            else:
                pass
                #answer = '你是想问'+result['LO1']+'的经销商信息吗？快告诉我你想知道的品牌或者车型吧，例如：温州这边有奥迪的4S店吗？\n东莞这边有卖帕萨特的吗？'
        elif total_num == 2:
            if counter_jieba['vm'] == 1:
                if counter_jieba['ci'] == 1:
                    answer = self.searchOneComp(result['vm'][0],result['ci'])
                elif counter_jieba['vi'] == 1:
                    answer = self.searchOneVichleInfo(result['vm'][0],result['vi'])
                elif counter_jieba['city'] == 1:
                    answer = self.searchVMLODE(result['vm'][0],result['city'])
                elif counter_jieba['area'] == 1:
                    answer = self.searchVMArea(result['vm'][0],result['area'])
                else:
                    pass
            elif counter_jieba['manu'] == 1:
                if counter_jieba['city'] == 1:
                    answer = self.searchManuCity(result['manu'][0],result['city'])
                elif counter_jieba['area'] == 1:
                    answer = self.searchManuArea(result['manu'][0],result['area'])
                else:
                    pass
        elif total_num == 3:
            if counter_jieba['vm'] == 1:
                if counter_jieba['city'] == 1 and counter_jieba['area'] == 1:
                    answer = self.searchCityArea(result['vm'][0], result['city'], result['area'])
                elif counter_jieba['ci'] == 2:
                    answer = self.searchOneComp(result['vm'][0],result['ci'])
                elif counter_jieba['vi'] == 2:
                    answer = self.searchTwoVI(result['vm'][0],result['vi'])
                elif counter_jieba['vi'] ==1 and counter_jieba['ci'] ==1:
                    answer = self.searchCompVI(result['vm'][0],result['vi'],result['ci'])
                elif counter_jieba['manu'] == 1 and counter_jieba['area'] == 1:
                    answer = self.searchVMArea(result['vm'][0],result['area'])
                elif counter_jieba['manu'] == 1 and counter_jieba['city'] == 1:
                    answer = self.searchVMLODE(result['vm'][0],result['city'])
                else:
                    pass
            elif counter_jieba['manu'] == 1 and counter_jieba['city'] == 1 and counter_jieba['area'] == 1:
                answer = self.searchManuCityArea(result['manu'][0],result['city'],result['area'])
        else:
            list_anwser = ['说实话，我没法跟你沟通。','我感觉还得过几年我才能懂你的意思。','这个有点难啊。','你是在刁难我吗？',
            '我这么可爱，你忍心这样刁难我吗？','放过我吧，好吗？','我听不懂你在说啥，可能是因为我还是个孩子。']
            answer = [random.choice(list_anwser)]
        return answer
        
        

if __name__ == "__main__":
    '''
    while True:
        message=input("你想问什么：")
        searchN = searchCarInNeo4j(message)
        searchN.search()
    '''
    searchN = searchCarInNeo4j()
    while True:
        message=input("你想问什么：")
        answer = searchN.search(message)
        for i in answer:
            print(i)
