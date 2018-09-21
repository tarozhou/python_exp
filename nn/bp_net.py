#-*- coding: utf-8 -*-

import math
import random


def sigmod(liner_v):
    return 1.0 / (1.0 + math.exp(-liner_v))


class Node(object):

    def __init__(self,layer_index,node_index):

        '''
        构造节点对象
        :param layer_index: 所在层的编号
        :param node_index:  节点编号
        '''

        self.layer_index = layer_index
        self.node_index = node_index
        self.downstream=[]
        self.upstream=[]
        self.output = 0.0
        self.delta = 0.0

    def set_output(self,output):
        self.output = output

    def cal_output(self):

        output = reduce(lambda ret,conn:ret+conn.upstreamNode.output*conn.weight,self.upstream,0.0)
        self.output = sigmod(output)
        #print "self.output：",self.output,"output:",output,"layer index:",self.layer_index,"node index:",self.node_index


    def cal_hidden_layer_delta(self):

        downstream_delta = reduce(
            lambda ret,conn:ret+conn.downstreamNode.delta*conn.weight,
            self.downstream,
            0.0
        )

        '''
        for stream  in self.downstream:

            if self.layer_index>0:
                print "--------"
                print "weight:", stream.weight, "layer index", self.layer_index, "node index", self.node_index, "output", self.output
                print "downstreamNode - delta:",stream.downstreamNode.delta," layer index:",stream.downstreamNode.layer_index,"node index:",stream.downstreamNode.node_index," output:",stream.downstreamNode.output
        '''


        self.delta = self.output*(1-self.output)*downstream_delta


    def cal_output_layer_delta(self,label):

        self.delta = self.output*(1-self.output)*(label - self.output)
        #print "output:",self.output,"label:",label,"delta:",self.delta,"layer index",self.layer_index,"node index",self.node_index


    def append_downstream_conn(self,conn):

        self.downstream.append(conn)

    def append_upstream_conn(self,conn):

        self.upstream.append(conn)


    def __str__(self):

        node_str = "%u - %u: output: %f delta: %f"%(self.layer_index,self.node_index,self.output,self.delta)
        downstream_str = reduce(lambda ret,conn:ret+"\n\t" + str(conn),self.downstream,'')
        upstream_str = reduce(lambda ret,conn:ret+"\n\t"+str(conn),self.upstream,'')
        return node_str+"\n\tdownstream:"+downstream_str+"\n\tupstream:"+upstream_str



class constNode(object):


    def __init__(self,layer_index,node_index):

        self.layer_index = layer_index
        self.node_index = node_index
        self.downstream = []
        self.output = 1.0
        self.delta = 0.0

    def append_downstream_conn(self,conn):

        self.downstream.append(conn)

    def cal_hidden_layer_delta(self):

        downstream_delta = reduce(
            lambda ret,conn:ret+conn.downstreamNode.delta*conn.weight,
            self.downstream,
            0.0
        )

        self.delta = self.output*(1-self.output)*downstream_delta


    def __str__(self):

        node_str = "%u - %u: output: %f delta: %f"%(self.layer_index,self.node_index,self.output,self.delta)
        downstream_str = reduce(lambda ret,conn:ret+"\n\t" + str(conn),self.downstream,'')
        return node_str+"\n\tdownstream:"+downstream_str


class Layer(object):

    def __init__(self,layer_index,node_count):

        self.layer_index = layer_index
        self.nodes = []

        for i in range(node_count):
            self.nodes.append(Node(layer_index,i))
        self.nodes.append(constNode(layer_index,node_count))

    def set_output(self,data):

        for i in range(len(data)):
            self.nodes[i].set_output(data[i])

    def cal_output(self):

        for node in self.nodes[:-1]:
            node.cal_output()


    def dump(self):

        for node in self.nodes:
            print node



class Connection(object):

    def __init__(self,upstreamNode,downstreamNode):

        self.upstreamNode = upstreamNode
        self.downstreamNode = downstreamNode
        self.weight = random.uniform(-0.1,0.1)
        self.grad = 0.0

    def get_grad(self):

        return self.grad


    def cal_grad(self):

        self.grad = self.upstreamNode.output*self.downstreamNode.delta

    def update_weight(self,rate):

        self.cal_grad()
        self.weight+=rate*self.grad

    def __str__(self):

        return "(%u-%u) -> (%u-%u) = %f"%(

            self.upstreamNode.layer_index,
            self.upstreamNode.node_index,
            self.downstreamNode.layer_index,
            self.downstreamNode.node_index,
            self.weight
        )



class Connections(object):

    def __init__(self):

        self.connections = []

    def add_connection(self,conn):

        self.connections.append(conn)

    def dump(self):

        for conn in self.connections:
            print conn


class NetWork(object):

    def __init__(self,layers):

        self.connections  = Connections()
        self.layers = []

        for i in range(len(layers)):
            self.layers.append(Layer(i,layers[i]))

        for layer in range(len(self.layers)-1):
            connections = [Connection(upstreamNode,downstreamNode)
                                for upstreamNode in self.layers[layer].nodes
                                for downstreamNode in self.layers[layer+1].nodes[:-1]]

            for conn in connections:
                self.connections.add_connection(conn)
                conn.downstreamNode.append_upstream_conn(conn)
                conn.upstreamNode.append_downstream_conn(conn)


    def cal_delta(self,label):

        out_put_node = self.layers[-1].nodes
        for i in range(len(label)):
            out_put_node[i].cal_output_layer_delta(label[i])

        for layer in self.layers[-2::-1]:
            for node in layer.nodes:
                node.cal_hidden_layer_delta()

    def predict(self,sample):

        self.layers[0].set_output(sample)
        for layer in self.layers[1:]:
            layer.cal_output()

        return map(lambda node:node.output,self.layers[-1].nodes[:-1])


    def update_weight(self,rate):

        for layer in self.layers[:-1]:
            for node in layer.nodes:
                for conn in node.downstream:
                    conn.update_weight(rate)

    def train_one_sample(self,sample,label,rate):

        self.predict(sample)
        self.cal_delta(label)
        self.update_weight(rate)


    def train(self,labels,data_set,rate,iteration):

        for i in range(iteration):
            for j in range(len(data_set)):
                self.train_one_sample(data_set[j],labels[j],rate)

    #用于梯度检查的2个函数
    def cal_grad(self):

        for layer in self.layers[:-1]:
            for node in layer.nodes:
                for conn in node.downstream:
                    conn.cal_grad()


    def get_grad(self,label,sample):

        self.predict(sample)
        self.cal_delta(label)
        self.cal_grad()

    def dump(self):

        for layer in self.layers:
            layer.dump()


def check_grad(network,sample_feature,sample_label):


    network_error = lambda vec1,vec2: 0.5*reduce(lambda a,b:a+b,map(lambda v:(v(0) - v(1))*(v(0)-v(1)),zip(vec1,vec2)))

    network.get_grad(sample_label,sample_feature)

    for conn in network.connections:

        actual_grad = conn.get_grad()


        epsilon = 0.0001
        conn.weight+=epsilon
        error1 = network_error(network.predict(sample_feature),sample_label)

        conn.weight-=2*epsilon
        error2 = network_error(network.predict(sample_feature),sample_label)

        expected_grad = (error2-error1)/(2*epsilon)

        print "expected_grad:%f  actual_grad:%f "%(expected_grad,actual_grad)











if __name__ == '__main__':


    data_set=[[0,0,0],
              [0,0,0],
              [0,0,0],
              [0,0,0],
              [0,0,0],
              [1,1,1],
              [1,1,1],
              [1,1,1],
              [1,1,1],
              [1,1,1]]

    label=[[1,0],
           [1,0],
           [1,0],
           [1,0],
           [1,0],
           [0,1],
           [0,1],
           [0,1],
           [0,1],
           [0,1]]


    network = NetWork([3,5,2])


    print "================================================"

    network.train(label,data_set,0.1,2000)
    network.dump()

    print "================================================"


    for data in data_set:
        print network.predict(data)
