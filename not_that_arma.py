import math
import datetime
import numpy
import csv

DAYS_NUMERATION = {1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday", 7:"Sunday"}

def extract_features(timestamp):
    """ Unpacks the features of a given timestamp

    @timestamp: datetime.timestamp

    returns: 1x2 vector ["day of the week", "time of the day"]
    """
    datetime_obj = datetime.datetime.fromtimestamp(float(timestamp))
    day_of_the_week = datetime_obj.day
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

     @X: features input vector
     @Y: expected output

     return: model parameters W, b
     """

    hidden_units = 2
    learning_rate = 0.02
    m = X.shape[1]

    # init params
    W1 = numpy.random.rand(X.shape[0], hidden_units)
    print("W1 shape is",W1.shape)
    b1 = numpy.zeros((hidden_units, m))
    print("b1 shape is",b1.shape)
    W2 = numpy.random.rand(hidden_units, Y.shape[0])
    print("W2 shape is",W2.shape)
    b2 = numpy.zeros((1, 1))
    print("b2 shape is",b2.shape)

    delta_cost = 0

    for i in range(0, iterations):
        # forward prop
        Z1 = numpy.dot(W1.T, X) + b1
        # print("Z1 shape is",Z1.shape)
        A1 = numpy.maximum(Z1, 0)
        # print("A1 shape is", A1.shape)
        Z2 = numpy.dot(W2.T, A1) + b2
        # print("Z2 shape is",Z2.shape)
        A2 = sigmoid(Z2) # this is our predictor in probabilities
        # print("A2 shape is", A2.shape)

        # compute cost
        log_part1 = Y * numpy.log(A2)
        log_part2 = (1 - Y) * numpy.log(1 - A2)
        cost = -1 * numpy.sum(log_part1 + log_part2, axis=1, keepdims=True)
        delta_cost += cost
        print("delta cost is {}".format(delta_cost))
        # backprop
        dZ2 = A2 - Y
        # print("dZ2 shape is", dZ2.shape)
        dW2 = numpy.dot(A1, dZ2.T) / m
        # print("dW2 shape is", dW2.shape)
        db2 = numpy.sum(dZ2, axis=1, keepdims=True) / m
        # print("db2 shape is", db2.shape)
        dA1 = numpy.dot(W2, dZ2)
        # print("dA1 shape is", dA1.shape)
        dZ1 = numpy.dot(W2, dZ2)
        # print("dZ1 shape is", dZ1.shape)
        dW1 = numpy.dot(dZ1, X.T) / m
        # print("dW1 shape is", dW1.shape)
        db1 = numpy.sum(dZ1, axis=1, keepdims=True) / m
        # print("db1 shape is", db1.shape)

        # update weights
        W1 = W1 - learning_rate * dW1
        W2 = W2 - learning_rate * dW2
        b1 = b1 - learning_rate * db1
        b2 = b2 - learning_rate * db2

    model = {"W1": W1, "W2": W2, "b1": b1, "b2": b2}
    return model

def classify(X_test, Y_test, model):
    Z1 = numpy.dot(model['W1'].T, X_test) + model['b1']
    A1 = numpy.max(Z1, 0)
    Z2 = numpy.dot(model['W2'].T, A1) + model['b2']
    A2 = sigmoid(Z2) # this is our predictor in probabilities

    cost = -1 * numpy.sum(Y_test * numpy.log(A2), (1 - Y_test) * numpy.log(1 - A2))
    print("Cost is {}".format(cost))

    for i in  range(len(A2)):
        print("Predicted {} where expected was {}".format(A2[i], Y_test[i]))

    return A2


if __name__ == '__main__':
    # i will try a low percision time first time is split into 24 categories
    X_train, Y_train = create_input_structure('training_set.csv')
    model = create_and_train(X_train, Y_train, 500)
    X_test, Y_test = create_input_structure('validation_set.csv')
    predict = classify(X_test, Y_test, model)

