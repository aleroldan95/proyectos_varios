import numpy as np
import matplotlib.pyplot as plt
import sklearn
import sklearn.datasets
from math import sqrt

class NN:
    def __init__(self, nn_config={}):

        # Attributes from Configuration
        self.X = nn_config.get('X', None)
        self.Y = nn_config.get('Y', None)
        self.learning_rate = nn_config.get('learning_rate', 0.01)
        self.num_iterations = nn_config.get('num_iterations', 15000)
        self.print_cost = nn_config.get('print_cost', True)
        self.initialization = nn_config.get('initialization', 'random')
        self.layers_dims = nn_config.get('layers_dims', [3, 2, 1])
        self.activations = nn_config.get('activations', ['relu', 'relu', 'sigmoid'])

        # Internal Attributes
        self.grads = {}
        self.m = self.X.shape[1]
        self.n_x = self.X.shape[0]
        self.n_y = 1
        self.parameters = {}
        self.cache = {}

        np.random.seed(3)

    def run(self):
        # Initialize parameters dictionary.
        if self.initialization == "random":
            self.parameters = self.initialize_parameters_random()
        elif self.initialization == "he":
            self.parameters = self.initialize_parameters_he()

        # Loop (gradient descent)
        for i in range(0, self.num_iterations):

            # Forward propagation: LINEAR -> RELU -> LINEAR -> RELU -> LINEAR -> SIGMOID.
            AL = self.forward_propagation()

            # Loss
            cost = self.compute_cost(AL, self.Y)

            # Backward propagation.
            self.backward_propagation(AL)

            # Update parameters.
            self.update_parameters()

            # Print the loss every 1000 iterations
            costs = []
            if self.print_cost and i % 1000 == 0:
                print("Cost after iteration {}: {}".format(i, cost))
                costs.append(cost)

        # plot the loss
        plt.plot(costs)
        plt.ylabel('cost')
        plt.xlabel('iterations (per hundreds)')
        plt.title("Learning rate =" + str(self.learning_rate))
        plt.show()


    def initialize_parameters_random(self):
        parameters = {}
        L = len(self.layers_dims)  # integer representing the number of layers

        for l in range(1, L):
            ### START CODE HERE ### (≈ 2 lines of code)
            parameters['W' + str(l)] = np.random.randn(self.layers_dims[l], self.layers_dims[l - 1]) * 10
            parameters['b' + str(l)] = np.zeros((self.layers_dims[l], 1))
            ### END CODE HERE ###

        return parameters

    def initialize_parameters_he(self):
        """
        initialization uses a scaling factor for the weights  W[l]W[l]  of sqrt(1./layers_dims[l-1])
        where He initialization would use sqrt(2./layers_dims[l-1]).)
        """
        L = len(self.layers_dims) - 1  # integer representing the number of layers

        for l in range(1, L + 1):
            self.parameters['W' + str(l)] = np.random.randn(self.layers_dims[l], self.layers_dims[l - 1]) * sqrt(
                2. / self.layers_dims[l - 1])
            self.parameters['b' + str(l)] = np.zeros((self.layers_dims[l], 1))


    def forward_propagation(self):
        """
        z[1](i)=W[1]x(i)+b[1]
        a[1](i)=tanh(z[1](i))
        """
        # Retrieve each parameter from the dictionary "parameters"
        L = len(self.layers_dims) - 1
        self.cache['A0'] = self.X
        for l in range(1, L + 1):
            W = self.parameters['W' + str(l)]
            b = self.parameters['b' + str(l)]

            self.cache['Z' + str(l)] = np.dot(W, self.parameters['A' + str(l-1)]) + b
            self.cache['A' + str(l)] = self.get_activation(self.cache["Z" + str(l)], self.activations[l-1])

        return self.cache['A' + str(L)]

    def compute_cost(self, AL, Y):
        # Compute loss from aL and y.
        cost = -(1 / self.m) * np.sum(np.dot(Y, np.log(AL).T) + np.dot(1 - Y, np.log(1 - AL).T))
        cost = np.squeeze(cost)  # To make sure your cost's shape is what we expect (e.g. this turns [[17]] into 17).
        assert (cost.shape == ())

        return cost

    def backward_propagation(self, AL):
        """
        Implement the backward propagation
        """
        L = len(self.layers_dims)  # the number of layers
        Y = self.Y.reshape(AL.shape)  # after this line, Y is the same shape as AL

        # Initializing the backpropagation
        self.grads['dA' + str(L)] = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))

        for l in reversed(range(1, L)):
            self.grads['dZ' + str(l)] = self.activation_backward(dA=self.grads['dA' + str(l)],
                                                                 Z=self.cache['Z' + str(l)],
                                                                 activation_mode= self.activations[L-1])
            self.grads['dW' + str(l)] = (1/self.m)*np.dot(self.grads['dZ' + str(l)],  self.cache['A' + str(l-1)].T)
            self.grads['db' + str(l)] = (1 / self.m) * np.sum(self.grads['dZ' + str(l)], axis=1, keepdims=True)
            self.grads['dA' + str(l-1)] = np.dot(self.parameters['W' + str(l)].T, self.grads['dZ' + str(l)])

    def update_parameters(self):

        """
        Update parameters using gradient descent
        """
        L = len(self.layers_dims)  # integer representing the number of layers

        for l in range(1, L):
            self.parameters["W" + str(l)] = self.parameters["W" + str(l)] - self.learning_rate * self.grads["dW" + str(l)]
            self.parameters["b" + str(l)] = self.parameters["b" + str(l)] - self.learning_rate * self.grads["db" + str(l)]


    def activation_backward(self, dA, Z, activation_mode):
        if activation_mode=='sigmoid':
            s = self.get_activation(Z, 'sigmoid')
            return np.dot(dA, s*(1-s))
        elif activation_mode=='relu':
            return max(0.00000001, Z)
        elif activation_mode=='tahn':
            return 1.0 - np.tanh(Z)**2
        elif activation_mode=='softmax':
            KeyError('Continuar aquí mañana')


    def get_activation(self, Z, activation_mode):
        if activation_mode == 'relu':
            A = np.maximum(0, Z)
        elif activation_mode == 'sigmoid':
            A = 1 / (1 + np.exp(-Z))
        elif activation_mode == 'softmax':
            expo = np.exp(Z)
            expo_sum = np.sum(np.exp(Z))
            A = expo / expo_sum
        elif activation_mode == 'tahn':
            A = np.tanh(Z)

        return A

    def get_parameters(self):
        return self.parameters

    def get_grads(self):
        return self.grads

    def get_cache(self):
        return self.cache