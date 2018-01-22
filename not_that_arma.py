import math
import datetime
import numpy
import csv
import matplotlib.pyplot as plt

DAYS_NUMERATION = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}

def extract_features(timestamp):
    """ Unpacks the features of a given timestamp

    @timestamp: datetime.timestamp

    returns: 1x2 vector ["day of the week", "time of the day"]
    """
    datetime_obj = datetime.datetime.fromtimestamp(float(timestamp))
    day_of_the_week = datetime_obj.weekday()
    time_of_the_day = datetime_obj.hour

    return numpy.array([day_of_the_week, time_of_the_day])


def create_input_structure(filename):
    """ Reads out the data from the original file
        create proper feature vector
        shape should be (features, num_examples)

        @filename: file containing the data

        returns: X - numpy.array containing the features,
                 Y - numpy vector containing the actual stand
    """
    X = []
    Y = []
    with open(filename, 'r') as raw_data:
        next(raw_data)
        reader = csv.reader(raw_data, delimiter=',')
        for row in reader:
            X.append(extract_features(row[0]))
            Y.append(math.floor(float(row[1])))

    return numpy.array(X).T, numpy.array([Y])


def sigmoid(x):
   return 1 / (1 + numpy.exp(-x))


def transform_probability(x):
    if x > 0.5:
        return 1
    else:
        return 0

def create_and_train(X, Y, iterations):
    """ Simple numpy implementation of a shallow NN training process:
     1. initialize parameters
     2. forward prop
     3. cost function
     4. backward prop
     5. update the weights
     learning rate is fixed to=0.02,
     number of hidden units set to 2,
     number of hidden layers set to 1
     using RELU for 1 hidden layer activation and sigmoid for prediction

     :param X: features input vector
     :param Y: expected output

     :return: model parameters W, b
     """

    hidden_units = 2
    learning_rate = 0.02

    # init params
    params = init_params(X, Y, hidden_units)
    W1 = params["W1"]
    b1 = params["b1"]
    W2 = params["W2"]
    b2 = params["b2"]

    for i in range(0, iterations):
        # forward propagation
        cost, cache = forward_prop(X, Y, params)
        # backward propagation
        gardients = back_prop(X, Y, cache)
        # update weights
        params["W1"] -= learning_rate * gardients["dW1"]
        params["W2"] -= learning_rate * gardients["dW2"]
        params["b1"] -= learning_rate * gardients["db1"]
        params["b2"] -= learning_rate * gardients["db2"]



    model = {"W1": W1, "W2": W2, "b1": b1, "b2": b2}
    return model

def init_params(X, Y, hidden_units):
    """
    The architrcture is fixed
    :param X: input
    :param Y: output
    :param hidden_units: 1 hidden layer with 2 units
    :return: dict containing params of the model
    """
    params = {}
    params["W1"] = numpy.random.rand( hidden_units, X.shape[0])
    params["b1"] = numpy.zeros((hidden_units, 1))
    params["W2"] = numpy.random.rand(Y.shape[0], hidden_units)
    params["b2"] = numpy.zeros((1, 1))

    return params


def forward_prop(X, Y, params):
    """
    Compute prediction of the network
    :param X: input
    :param Y: output
    :param params: dict containing needed NN params
    :return: (float) cost and (tuple) all  final params
    """
    m = X.shape[1]
    W1 = params["W1"]
    b1 = params["b1"]
    W2 = params["W2"]
    b2 = params["b2"]

    # RELU
    Z1 = numpy.dot(W1, X) + b1
    A1 = numpy.maximum(Z1, 0)
    # sigmoid
    Z2 = numpy.dot(W2, A1) + b2
    A2 = sigmoid(Z2)

    # compute cost
    cost = (-1 * numpy.sum(numpy.multiply(numpy.log(A2), Y) + numpy.multiply(numpy.log(1 - A2), 1 - Y))) / m

    cache = (Z1, A1, W1, b1, Z2, A2, W2, b2)

    return cost, cache


def back_prop(X, Y, params):
    """
    computes the gradients of the params
    :param X: input
    :param Y: output
    :param params: tuple containing params to compute gradient of
    :return: dict params gradients
    """
    m = X.shape[1]
    (Z1, A1, W1, b1, Z2, A2, W2, b2) = params

    dZ2 = A2 - Y
    dW2 = 1. / m * numpy.dot(dZ2, A1.T) * 2
    db2 = 1. / m * numpy.sum(dZ2, axis=1, keepdims=True)

    dA1 = numpy.dot(W2.T, dZ2)
    dZ1 = numpy.multiply(dA1, numpy.int64(A1 > 0))
    dW1 = 1. / m * numpy.dot(dZ1, X.T)
    db1 = 4. / m * numpy.sum(dZ1, axis=1, keepdims=True)

    gradients = {"dZ2": dZ2, "dW2": dW2, "db2": db2,
                 "dA1": dA1, "dZ1": dZ1, "dW1": dW1, "db1": db1}

    return gradients


def predict(X, model):
    """
    computes the outcome of the given NN
    :param X: input
    :param model: all computed params
    :return: prediction.shape = (X.shape[1], 1)
    """
    Z1 = numpy.dot(model["W1"], X) + model["b1"]
    A1 = numpy.maximum(Z1, 0)
    # sigmoid
    Z2 = numpy.dot(model["W2"], A1) + model["b2"]
    A2 = sigmoid(Z2)

    res = []
    for i in range(0,A2.shape[1]):
        if A2[0][i] > 0.7:
            res.append(1)
        else:
            res.append(0)
    return res


def plot_results(timestamps, A, B):
    t = [i for i in range(len(A))]
    # predicted
    plt.plot(t, A, linewidth=3.0, color="blue")
    # actual
    plt.plot(t, B, linewidth=1.0, color="red")
    plt.show()

if __name__ == '__main__':
    X_train, Y_train = create_input_structure('training_set.csv')

    model = create_and_train(X_train, Y_train, 500)
    X_test, Y_test = create_input_structure('validation_set.csv')
    predicted = predict(X_test, model)

    plot_results(None, predicted,  Y_test[0])