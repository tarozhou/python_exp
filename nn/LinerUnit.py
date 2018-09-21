from Perceptron import Perceptron

f=lambda x:x


class LinearUnit(Perceptron):

    def __init__(self,w_num):

        Perceptron.__init__(self,w_num,f)


def get_train_data():

    w_vec = [[5],[3],[8],[1.4],[10.1]]
    labels = [5500,2300,7600,1800,11400]

    return w_vec,labels

def train_liner_unit():

    lu = LinearUnit(1)
    w_vec,labels = get_train_data()

    lu.train(w_vec,labels,10,0.01)

    return lu


if __name__ == '__main__':

    lu = train_liner_unit()

    print lu.weights
    print lu.bias


    print '---------------------test-----------------'
    print lu.predict([3.4])
    print lu.predict([1.1])
    print lu.predict([8.7])

