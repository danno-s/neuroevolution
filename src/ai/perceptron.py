from random import random

class Perceptron():
    def __init__(self, weights, bias=0, learning_rate=0.5, output_fun=lambda x: int(x > 0)):
        self.weights = weights
        self.bias = bias
        self.output_fun = output_fun
        self.learning_rate = learning_rate

    def process(self, inputs):
        assert len(inputs) == len(self), "Mismatched inputs, should be {} elements, not {}".format(len(self), len(inputs))

        s = 0
        for i, w in zip(inputs, self.weights):
            s += i * w

        return self.output_fun(s + self.bias)


    def train(self, inputs, expecteds):
        for inp, expected in zip(inputs, expecteds):
            result = self.process(inp)

            if result != expected:
                diff = expected - result

                for i in range(len(self.weights)):
                    self.weights[i] += self.learning_rate * inp[i] * diff

                self.bias += self.learning_rate * diff

    def __len__(self):
        return len(self.weights)

AND = Perceptron([1, 1], bias=-1.9)
OR = Perceptron([1, 1])
NAND = Perceptron([-1, -1], bias=1.9)
Identity = Perceptron([1], output_fun=lambda x: x)

class RandomPerceptron(Perceptron):
    def __init__(self, inputs, **kwargs):
        self.weights = [random() * 2 - 1 for _ in range(inputs)]
        self.bias = random() * 2 - 1
        self.delta = None
        self.output = None
        super(RandomPerceptron, self).__init__(self.weights, self.bias, **kwargs)
