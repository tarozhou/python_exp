#-*- coding: utf-8 -*-

import numpy as np
from numpy import random,mat

class FullConnectedLayer(object):

    def __init__(self,input_size,output_size,activtor):

        self.input_size = input_size
        self.output_size = output_size
        self.activtor = activtor

        self.W_mtx = np.random.uniform(-0.1,0.1,(output_size,input_size))
        self.W_grad_mtx = np.zeros((output_size,input_size))

        self.b_arr = np.zeros((output_size,1))
        self.b_grad_arr = np.zeros((output_size,1))

        self.input_arr = np.zeros((output_size,1))

        self.output_arr = np.zeros((output_size,1))

        self.upstream_delta_arr = np.zeros((output_size,1))


    def cacul_delta_for_upstream(self,delta_from_downstream):

        self.upstream_delta_arr = self.activtor.backward(self.input_arr) * np.dot(self.W_mtx.T,delta_from_downstream)


    def forward(self,input_upstream_arr):

        self.input_arr = input_upstream_arr

        self.output_arr = self.activtor.forward(np.dot(self.W_mtx,input_upstream_arr).reshape(-1,1)+self.b_arr)


    def backward(self,delta_from_downstream):

        self.cacul_delta_for_upstream(delta_from_downstream)

        self.W_grad_mtx = np.dot(delta_from_downstream,self.input_arr.T)

        self.b_grad_arr = delta_from_downstream


    def update(self,learn_rate):

        self.W_mtx += learn_rate*self.W_grad_mtx
        self.b_arr += learn_rate*self.b_grad_arr


class SigmoidActivator(object):

    def forward(self, weighted_input):
        return 1.0 / (1.0 + np.exp(-weighted_input))


    def backward(self, output):
        return output * (1 - output)


class NetWork(object):

    def __init__(self,layers):

        self.layers=[]
        for i in range(len(layers)-1):
            self.layers.append(FullConnectedLayer(layers[i],layers[i+1],SigmoidActivator()))

    def predict(self,sample):

        output = sample
        for layer in self.layers:
            layer.forward(output)
            output = layer.output_arr

        return output


    def calc_delta_and_grad(self,label):

        #从输出层开始计算delta，注意，每一层layer的delta不是存储本层的delta，存储供给给上层的delta

        delta = self.layers[-1].activtor.backward(self.layers[-1].output_arr)*(np.array(label)-self.layers[-1].output_arr)

        for layer in self.layers[::-1]:
            layer.backward(delta)
            delta = layer.upstream_delta_arr


    def update_weight(self,rate):

        for layer in self.layers:
            layer.update(rate)


    def train_once(self,sample,label,rate):

        self.predict(sample)
        self.calc_delta_and_grad(label)
        self.update_weight(rate)


    def train(self,data_set,labels,rate,iteration):

        for i in range(iteration):
            for j  in range(len(data_set)):
                self.train_once(np.array(data_set[j]).reshape(-1,1),np.array(labels[j]).reshape(-1,1),rate)




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

    network.train(data_set,label,0.1,2000)

    print network.layers[0].W_mtx

    print "================================================"

    for data in data_set:
        print network.predict(np.array(data).reshape(-1,1))

