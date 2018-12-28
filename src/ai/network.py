from itertools import tee
from .layer import Layer

class Network():
    def __init__(self, layers, **kwargs):
        '''Receives a list of disconnected layers, and connects them in order.
        Only keeps a reference to the first layer.
        The list of layer can also be a list of integers, in which case the layers
        will be built by this class, and each number represents the number of inputs/outputs 
        of each layer. e.g. [3, 1, 3] Creates a network of 1 hidden layer, that receives 3 inputs, 
        has 3 outputs, and between the two layers one value is passed to and from each neuron.

        inputs |hidden layer| outputs
           ·     \       /       ·
           ·     -   ·   -       ·
           ·     /       \       ·

        Accepts any kwargs that are used in the constructors for layers and sigmoid neurons e.g. the
        learning rate of the network.
        '''
        def pairwise(iterable):
            a, b = tee(iterable)
            next(b, None)
            return zip(a, b)

        processed_layers = []
        if all([type(e)==int for e in layers]):
            for inputs, neurons in pairwise(layers):
                processed_layers.append(
                    Layer(inputs, neurons, **kwargs)
                )
        else:
            processed_layers = layers

        self.first_layer = processed_layers[0]
        self.last_layer = processed_layers[-1]

        for layer, next_layer in pairwise(processed_layers):
            layer.next_layer = next_layer
            next_layer.previous_layer = layer

    def process(self, inputs):
        return self.first_layer.process(inputs)

    def to_list(self):
        '''Returns a list containing every node of this network
        '''
        return self.first_layer.to_list([])

    def set_neurons(self, new_neurons):
        self.first_layer.set_neurons(new_neurons)

    def train(self, inputs, expecteds):
        for i, expected in zip(inputs, expecteds):
            # We don't need to store the outputs, so we just
            # make the network process it to mutate the
            # neurons' internal state (their outputs).
            self.process(i)
            self.propagate_error(expected)
            self.update_weights(i)

    def propagate_error(self, expecteds):
        self.last_layer.propagate_error(expecteds)

    def update_weights(self, inputs):
        self.first_layer.update_weights(inputs)
