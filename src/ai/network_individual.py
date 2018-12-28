from random import randint, random
from .network import Network
from .neuron import SigmoidNeuron

mutation_rate = 0.2

'''Clase que representa una solución al problema de N reinas en un tablero de NxN.
La solución se representa simplemente con las posiciones de las N reinas.
'''
class NetworkIndividual:
    def __init__(self, n):
        '''Crea una red neuronal para un juego de snake de N casilleros totales
        El diseño de la red serán todos los casilleros como un input, 16 neuronas como capa
        oculta, y 4 neuronas como capa de salida (las 4 direcciones posibles de movimiento).

        Cada individuo registra su propio puntaje y tiempo de vida, para luego ser usado como fitness
        '''
        self.n = n
        self.network = Network([self.n, 16, 4])
        self.score = 0
        self.lifetime = 0

    def reproduce(self, another_network):
        list_repr = self.network.to_list()
        another_list_repr = another_network.network.to_list()

        # the breakpoint is one of all the nodes in the network
        breakpoint = randint(0, self.n + 16 + 4)

        child_neurons = list_repr[:breakpoint] + another_list_repr[breakpoint:]

        for i in range(len(child_neurons)):
            if random() < mutation_rate:
                # First layer, n inputs
                if i < 16:
                    layer_len = self.n
                # Seond layer, 16 inputs
                else:
                    layer_len = 16
                # Replace the previous neuron with a new, random one
                child_neurons[i] = SigmoidNeuron(layer_len)

        child = NetworkIndividual(self.n)

        child.network.set_neurons(child_neurons)

        return child
