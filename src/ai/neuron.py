from math import exp
from .perceptron import RandomPerceptron

class SigmoidNeuron(RandomPerceptron):
    '''A Neuron, adds the capability of storing two new values to ease in back-propagation:
        - output: The result of the last calculation made by this neuron.
        - delta: The error of the last calculation times the derivative of its output.
    '''
    def __init__(self, inputs, activation_fun = lambda x: 1 / (1 + exp(-x)),**kwargs):
        kwargs['output_fun'] = activation_fun
        super(SigmoidNeuron, self).__init__(inputs, **kwargs)

    def process(self, inputs):
        self.output = super(SigmoidNeuron, self).process(inputs)
        return self.output

    def adjust_delta(self, error):
        # Error * transfer derivative
        self.delta = error * self.output * (1 - self.output)

    def adjust_bias(self):
        self.bias += self.learning_rate * self.delta

    def adjust_weights(self, inputs):
        for index, i in enumerate(inputs):
            self.weights[index] += self.learning_rate * self.delta * i
