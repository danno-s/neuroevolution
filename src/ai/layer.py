from .neuron import SigmoidNeuron

class Layer():
    def __init__(self, inputs, neurons, next_layer=None, previous_layer=None, **kwargs):
        self.neurons = [SigmoidNeuron(inputs, **kwargs) for _ in range(neurons)]
        self.inputs = inputs
        self.next_layer = next_layer
        self.previous_layer = previous_layer

    def process(self, inputs):
        assert len(inputs) == self.inputs, "Mismatched inputs in layer, should be {} not {}".format(self.inputs, len(inputs))
        
        results = [neuron.process(inputs) for neuron in self]

        if not self.next_layer:
            return results
        else:
            return self.next_layer.process(results)

    def to_list(self, answer):
        # Add my neurons
        answer.extend(self.neurons)

        # Ask the next layer to add it's neurons
        if self.next_layer:
            self.next_layer.to_list(answer)

        return answer

    def set_neurons(self, new_neurons):
        for i in range(len(self.neurons)):
            # The new neuron is always the first in the list
            new_neuron = new_neurons.pop(0)
            # We replace the old neuron
            self.neurons[i] = new_neuron

        if self.next_layer:
            self.next_layer.set_neurons(new_neurons)

    def propagate_error(self, expecteds=None):
        if expecteds is not None:
            for neuron, expected in zip(self.neurons, expecteds):
                error = expected - neuron.output
                neuron.adjust_delta(error)
        else:
            for i, neuron in enumerate(self):
                error = 0
                for next_neuron in self.next_layer:
                    error += next_neuron.weights[i] * next_neuron.delta
                neuron.adjust_delta(error)
            
        if self.previous_layer:
            self.previous_layer.propagate_error()

    def update_weights(self, initial_inputs):
        assert all([neuron.delta is not None for neuron in self]), "Some neurons have uninitialized deltas"

        if self.previous_layer:
            inputs = [neuron.output for neuron in self.previous_layer]
        else:
            inputs = initial_inputs

        for neuron in self:
            neuron.adjust_weights(inputs)
            neuron.adjust_bias()

        if self.next_layer:
            self.next_layer.update_weights(initial_inputs)

    def __iter__(self):
        '''If one iterates through a layer, then one iterates through its neurons.
        '''
        for neuron in self.neurons:
            yield neuron

    def __len__(self):
        return len(self.neurons)
