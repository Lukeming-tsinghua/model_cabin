import numpy as np
import json
from pyecharts.charts.basic_charts.graph import Graph
from pyecharts import options as opts
from pyecharts.globals import ThemeType

class data:
    def __init__(self,path = './'):
        self.entities_train = np.load(path+'entities_train.npy')
        self.entities_test = np.load(path+'entities_test.npy')
        self.label_train = np.load(path+'label_train.npy')
        self.label_test = np.load(path+'label_test.npy')

    def makeDict(self):
        entities_dict = {1:[],2:[],3:[]}
        for i in range(self.entities_train.shape[0]):
            if self.entities_train[i] and self.label_train[i]:
                label = np.where(self.label_train[i][0]==1)[0][0]
                if label:
                    entities_dict[label].append(self.splitCui(self.entities_train[i]))
        for i in range(self.entities_test.shape[0]):
            if self.entities_test[i] and self.label_test[i]:
                label = np.where(self.label_test[i][0]==1)[0][0]
                if label:
                    entities_dict[label].append(self.splitCui(self.entities_test[i]))
        return entities_dict

    def makeJson(self):
        total_cui_list = self.makeDict()[1]+self.makeDict()[2]+self.makeDict()[3]
        node_list = sum(total_cui_list,[])
        node_unique_list = list(set(node_list))
        node_value = [node_list.count(item) for item in node_unique_list]
        node = []
        link = []
        mycolor = ('#FFFFFF','#FF3030','#FFF68F')
        for i in range(len(node_unique_list)):
            node.append({
                "name":node_unique_list[i],
                "symbolSize":node_value[i]*0.8,
                "draggable":"true"
                })
        for index in (1,2,3):
            tmp_data = self.makeDict()[index]
            for i in range(len(tmp_data)):
                link.append({'source':tmp_data[i][0],'target':tmp_data[i][1],'color':opts.LineStyleOpts(color=mycolor[index-1],width=1,curve=0.3)})
        return node,link

    def splitCui(self,cui_string):
        return [cui_string[0:8],cui_string[8:16]]

node,link = data().makeJson()

graph = Graph(init_opts=opts.InitOpts(width="1500px",height="1000px",theme=ThemeType.CHALK))
graph.add(
        "Name: ",
        node,
        link,
        repulsion=1000,
        label_opts=opts.LabelOpts(is_show=False),
).set_global_opts(
        title_opts=opts.TitleOpts(title="Relation Graph")
)
graph.render()
