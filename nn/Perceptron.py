#-*- coding: utf-8 -*-


class Perceptron(object):

    def __init__(self,w_num,active_fun):

        self.weights = [0.0 for _ in range(w_num)]
        self.active_fun = active_fun
        self.bias = 0.0


    def predict(self,x_vec):

        return self.active_fun(reduce(lambda x,y:x+y,map(lambda (x,w):x*w,zip(x_vec,self.weights)),0.0)+self.bias)


    def update_weight(self,x_vec,y,yp,rate):

        delta =  yp - y
        self.weights = map(lambda (x,w):w - rate*delta*x,zip(x_vec,self.weights))
        self.bias+=rate*delta


    def one_iter(self,x_matrix,y_vec,rate):

        samples = zip(x_matrix,y_vec)
        for(x_vec,y) in samples:
            yp = self.predict(x_vec)
            self.update_weight(x_vec,y,yp,rate)


    def train(self,x_matrix,y_vec,iteration,rate):

        for i in range(iteration):
            self.one_iter(x_matrix,y_vec,rate)

def f(x):

    return 1 if x>0 else 0


def get_train_data():

    x_matrix = [[1,1],[0,0],[1,0],[0,1]]
    y_vec = [1,0,0,0]

    return x_matrix,y_vec

def train_percetron():

    x_matrix,y_vec = get_train_data()

    perceptron = Perceptron(2,f)

    perceptron.train(x_matrix,y_vec,10,0.1)

    return perceptron


if __name__ == '__main__':

    perceptron = train_percetron()

    print perceptron.weights
    print perceptron.bias

    print "---------------test...------------------"

    print perceptron.predict([1.0, 1.0])
    print perceptron.predict([0, 0])
    print perceptron.predict([1, 0])
    print perceptron.predict([0, 1])
