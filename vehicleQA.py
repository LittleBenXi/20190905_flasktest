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
        self.list_ci = ['厂商指导价(万元)','厂商','上市时间','排量(L)','燃油标号','轴距(mm)','发动机型号','变速箱','发动机','长*宽*高(mm)','官方0-100km/h加速(s)','工信部综合油耗(L/100km)']
        self.result_non = '抱歉，小柯基没有找到相关信息。'
        self.mark_list = ['ci','vm','vi','ri','city','area','manu','kd','pr','date']
        self.kg = Graph("bolt://localhost:7687", auth=('neo4j', '123456'))
        #self.kg = Graph("http://localhost:7474", username="neo4j", password="123456")
        self.introduction = {'ci':'配件','ri':'限制','vi':'车型信息','city':'city','area':'area','DE':'经销商','vm':'车型','manu':'品牌','pr':'price','data':'上市日期'}

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
                    result = i['b.carname'] + '--' + i['c.value'] + '--' + entity[0] + '\n'
                    answer.append(result)
                elif '国V' in i['b.carname']:
                    pass
                else:
                    result = i['b.carname'] + '--' + i['c.value'] + '--' + entity[0] + '\n'
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
                    result = i['b.carname']+'的'+entity[0]+'是'+i['c.value'] + '\n'
                    answer.append(result)
                elif '国V' in i['b.carname']:
                    pass
                else:
                    result = i['b.carname']+'的'+entity[0]+'是'+i['c.value'] + '\n'
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
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address'] + '\n'
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
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address'] + '\n'
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
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address'] + '\n'
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
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address'] + '\n'
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
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address'] + '\n'
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
                    result =  i['b.carname']+' '+i['c.value']+' '+entity[0]+' '+i['d.value']+' '+entity[1] + '\n'
                    answer.append(result)
                elif '国V' in i['b.carname']:
                    pass
                else:
                    result =  i['b.carname']+' '+i['c.value']+' '+entity[0]+' '+i['d.value']+' '+entity[1] + '\n'
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
                    result =  i['b.carname']+'的'+entity[0]+'是'+i['c.value']+';'+entity[1]+'是'+i['d.value'] + '\n'
                    answer.append(result)
                elif '国V' in i['b.carname']:
                    pass
                else:
                    result =  i['b.carname']+'的'+entity[0]+'是'+i['c.value']+';'+entity[1]+'是'+i['d.value'] + '\n'
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
                    result =  i['b.carname']+'的'+entity1[0]+'是'+i['c.value']+';'+i['d.value']+'--'+entity2[0] + '\n'
                    answer.append(result)
                elif '国V' in i['b.carname']:
                    pass
                else:
                    result =  i['b.carname']+'的'+entity1[0]+'是'+i['c.value']+';'+i['d.value']+'--'+entity2[0] + '\n'
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
                result =  i['c.dealer']+'\n地区：'+i['c.city']+' '+i['c.area']+'\n电话：'+i['c.phone']+'\n地址：'+i['c.address'] + '\n'
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

    def searchVMPR(self,carmodel,price):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})-->(b:car)-->(c:ci {name:'厂商指导价(万元)'}) WHERE c.value='"+price+
        "万' RETURN b.carname").data()
        #print(list(result_list))
        if result_list == []:
            answer.append(self.result_non)
            return answer
        if len(result_list) == 1:
            node_name = result_list[0]['b.carname']
        else:
            node_name = result_list[0]['b.carname']
            for i in result_list:
                if '国VI' in i['b.carname']:
                    node_name = i['b.carname']
        a=self.kg.nodes.match('car',carname=node_name).first()
        if a == None:
            answer.append(self.result_non)
        else:
            answer.append(result)
            answer.append('车款：' + node_name)
            for i in self.list_ci:
                if i in a:
                    answer.append(i+':'+str(a[i]))
        return answer

    def searchVMPRDate(self,carmodel,price,date):
        answer = []
        result = '小柯基为您找到如下相关信息：'
        result_list = self.kg.run("MATCH (a:carmodel {carmodel:'"+carmodel+"'})-->(b:car)-->(c:ci {name:'厂商指导价(万元)'}) WHERE c.value='"+price+
        "万' RETURN b.carname").data()
        if result_list == []:
            answer.append(self.result_non)
            return answer
        if len(result_list) == 1:
            node_name = result_list[0]['b.carname']
        else:
            node_name = result_list[0]['b.carname']
            for i in result_list:
                if date in i['b.carname']:
                    node_name = i['b.carname']
        a=self.kg.nodes.match('car',carname=node_name).first()
        if a == None:
            answer.append(self.result_non)
        else:
            answer.append(result)
            answer.append('车款：' + node_name)
            for i in self.list_ci:
                if i in a:
                    if type(a[i]) == float:
                        answer.append(i+':'+str(round(a[i],2)))
                    else:    
                        answer.append(i+':'+str(a[i]))
        return answer

    def entityRecoByJieba(self, message):
        words = pseg.cut(message)
        result = {}
        counter = {}
        num_CI, num_VI, num_RI, num_manu, num_city, num_area, num_VM, num_KD,num_pr, num_date = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
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
            elif flag == 'pr':
                result.setdefault(flag, []).append(word)
                num_pr +=1
            elif flag == 'date':
                result.setdefault(flag, []).append(word)
                num_date +=1
            else:
                pass
        counter = {'ci':num_CI, 'vi':num_VI, 'ri':num_RI, 'manu':num_manu, 'city':num_city, 'area':num_area, 'vm':num_VM, 'kd':num_KD, 'pr':num_pr, 'date':num_date}
        total_num = num_CI + num_VI + num_RI + num_manu + num_city + num_area + num_VM + num_KD + num_pr + num_date
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
                elif counter_jieba['pr'] == 1:
                    answer = self.searchVMPR(result['vm'][0],result['pr'][0])
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
                elif counter_jieba['date'] == 1 and counter_jieba['pr'] ==1:
                    answer = self.searchVMPRDate(result['vm'][0],result['pr'][0],result['date'][0])
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
