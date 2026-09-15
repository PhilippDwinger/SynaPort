import random
from logging import warn, warning

from synaport.core.activation_functions import *
from synaport.core.initialization_functions import he_uniform, he_normal, xavier_uniform, xavier_normal, orthogonal

def get_initialization_from_activation(activation_function_name):
    if activation_function_name == "relu":
        return "he_uniform"
    elif activation_function_name == "sigmoid":
        return "xavier_uniform"
    elif activation_function_name == "tanh":
        return "xavier_uniform"
    else:
        warning(f"Activation function {activation_function_name} not implemented")
        return "xavier_uniform"

def get_activation_function_from_name(activation_function_name):
    if activation_function_name == "sigmoid":
        return sigmoid
    elif activation_function_name == "relu":
        return relu
    elif activation_function_name == "tanh":
        return tanh
    else:
        warning(f"Activation function {activation_function_name} not implemented")
        return sigmoid

def get_initialization_from_name(initialization_function_name, activation_function_name=None):
    if initialization_function_name == "auto":
        initialization_function_name = get_initialization_from_activation(activation_function_name)

    if initialization_function_name == "he_uniform":
        return he_uniform
    elif initialization_function_name == "he_normal":
        return he_normal
    elif initialization_function_name == "xavier_uniform":
        return xavier_uniform
    elif initialization_function_name == "xavier_normal":
        return xavier_normal
    elif initialization_function_name == "orthogonal":
        return orthogonal
    else:
        warning(f"Initialization function {initialization_function_name} not implemented")
        return xavier_uniform

class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias
    def __str__(self) -> str:
        return str(self.__dict__)
    def __repr__(self) -> str:
        return str(self.__dict__)
    def forward(self, given_inputs, activation_function):
        output = 0
        for weight, given_input in zip(self.weights, given_inputs):
            output += weight * given_input
        output += self.bias
        return activation_function(output)

class Dense:
    def __init__(self, neuron_amount, activation_function_name, initialization_function_name, input_amount):
        initialization_function = get_initialization_from_name(initialization_function_name, activation_function_name)
        weights = initialization_function(input_amount, neuron_amount)
        neurons = []
        for i in range(neuron_amount):
            weights_for_neuron = weights[i]
            neurons.append(Neuron(weights_for_neuron, random.uniform(0.01, 0.1)))
        self.neurons = neurons
        self.activation_function = get_activation_function_from_name(activation_function_name)
        self.initialization_function = initialization_function
    def __str__(self) -> str:
        return str(self.__dict__)
    def __repr__(self) -> str:
        return str(self.__dict__)
    def forward(self, given_inputs):
        outputs = []
        for neuron in self.neurons:
            neuron_output = neuron.forward(given_inputs, self.activation_function)
            outputs.append(neuron_output)
        return outputs

class DenseNeuronalNetwork:
    def __init__(self, input_amount, output_amount, hidden_layer_config):
        self.init_data_set = {
            "input_amount": input_amount,
            "output_amount": output_amount,
            "hidden_layers": hidden_layer_config
        }
        hidden_layers = []
        for entry in hidden_layer_config:
            neurons = entry["NeuronAmount"]
            hidden_layers.append(Dense(neurons, entry["ActivationFunction"], entry["InitializationFunction"], input_amount))
            input_amount = entry["NeuronAmount"]
        self.hidden_layers = hidden_layers

        last_hidden_layer = hidden_layers[-1]
        last_hidden_layer_neuron_amount = len(last_hidden_layer.neurons)

        self.output_layer = Dense(
            output_amount,
            "sigmoid",
            "he_uniform",
            last_hidden_layer_neuron_amount
        )
    def __str__(self) -> str:
        return str(self.__dict__)
    def __repr__(self) -> str:
        return str(self.__dict__)
    def forward(self, given_inputs):
        cache = []
        for hidden_layer in self.hidden_layers:
            cache.append(hidden_layer.forward(given_inputs))
            given_inputs = cache[-1]

        cache.append(self.output_layer.forward(given_inputs))
        return cache
    def train(self, data_set, learning_rate, iterations):
        for i in range(iterations):
            for data_set_entry in data_set:
                data_set_inputs = data_set_entry[0]
                data_set_outputs = data_set_entry[1]

                forward_pass = self.forward(data_set_inputs)

                network_gradients = []
                network_deltas = []
                network_biases = []

                #Output Layer
                output_deltas = []
                output_gradients = []
                output_biases = []

                last_hidden_layer_output = forward_pass[-2]
                for neuron_index, neuron in enumerate(self.output_layer.neurons):
                    output_layer_outputs = forward_pass[-1]
                    neuron_output = output_layer_outputs[neuron_index]

                for hidden_layer in reversed(self.hidden_layers):
                    pass


    def reset_neurons(self):
        self.__init__(self.init_data_set["input_amount"], self.init_data_set["output_amount"], self.init_data_set["hidden_layers"])