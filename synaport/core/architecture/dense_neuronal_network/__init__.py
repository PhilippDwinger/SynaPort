import random
from logging import warn, warning

import numpy as np

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
    elif activation_function_name == "leaky_relu":
        return leaky_relu
    else:
        warning(f"Activation function {activation_function_name} not implemented")
        return sigmoid

def get_derivative_from_name(derivative_function_name):
    if derivative_function_name == "sigmoid":
        return sigmoid_derivative
    elif derivative_function_name == "relu":
        return relu_derivative
    elif derivative_function_name == "tanh":
        return tanh_derivative
    elif derivative_function_name == "leaky_relu":
        return leaky_relu_derivative
    else:
        warning(f"Derivative function {derivative_function_name} not implemented")
        return sigmoid_derivative

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
        self.derivative_function = get_derivative_from_name(activation_function_name)
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
        self._init_data_set = {
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

    def train(self, data_set, learning_rate, iterations, shuffle_data_set=True):
        if shuffle_data_set:
            random.shuffle(data_set)
        for i in range(iterations):
            for data_set_entry in data_set:
                data_set_inputs = data_set_entry[0]
                data_set_outputs = data_set_entry[1]

                forward_pass = self.forward(data_set_inputs)

                network_deltas = []
                network_gradients = []

                # Output Layer
                output_deltas = []
                output_gradients = []

                last_hidden_layer_output = forward_pass[-2]
                for neuron_index, neuron in enumerate(self.output_layer.neurons):
                    output_layer_outputs = forward_pass[-1]
                    neuron_output = output_layer_outputs[neuron_index]
                    neuron_delta = 2 * (neuron_output - data_set_outputs[neuron_index]) * sigmoid_derivative(
                        neuron_output)

                    neuron_weight_gradients = []
                    for weight_index, weight in enumerate(
                            neuron.weights):  # <--- HIER GEÄNDERT: `weight_index` hinzugefügt, um das Gewicht direkt im RAM anzusteuern
                        weight_input = last_hidden_layer_output[
                            weight_index]  # <--- HIER GEÄNDERT: Holt den passenden Input über den Index aus dem Vorwärtspass
                        weight_gradient = neuron_delta * weight_input
                        weight_gradient = max(-1, min(1, weight_gradient))
                        neuron_weight_gradients.append(weight_gradient)

                        neuron.weights[
                            weight_index] -= learning_rate * weight_gradient  # <--- NEU: Zieht den berechneten Fehler-Schritt SOFORT vom echten Gewicht ab!

                    neuron.bias -= learning_rate * neuron_delta  # <--- NEU: Zieht den Fehler auch direkt vom Bias ab, damit das Neuron mitsamt seiner Kurve lernt!
                    output_gradients.append(neuron_weight_gradients)
                    output_deltas.append(neuron_delta)

                network_deltas.append(output_deltas)
                network_gradients.append(output_gradients)

                # Hidden Layers
                current_deltas = output_deltas
                for hidden_layer_index, hidden_layer in enumerate(reversed(self.hidden_layers)):
                    hidden_layer_deltas = []
                    hidden_layer_gradients = []
                    layer_entry = forward_pass[-hidden_layer_index - 2]
                    layer_input_layer_deltas = current_deltas
                    layer_input_layer_inputs = None

                    if -hidden_layer_index - 3 >= -len(forward_pass):
                        layer_input_layer_inputs = forward_pass[-hidden_layer_index - 3]
                    else:
                        layer_input_layer_inputs = data_set_inputs

                    for neuron_index, neuron in enumerate(hidden_layer.neurons):
                        neuron_gradients = []
                        neuron_fault = 0
                        neuron_output = layer_entry[neuron_index]

                        for weight, given_delta in zip(neuron.weights, layer_input_layer_deltas):
                            neuron_fault += given_delta * weight

                        neuron_delta = hidden_layer.derivative_function(neuron_output) * neuron_fault

                        for weight_index, given_input in enumerate(
                                layer_input_layer_inputs):
                            weight_gradient = neuron_delta * given_input
                            weight_gradient = max(-1, min(1, weight_gradient))
                            neuron_gradients.append(weight_gradient)

                            neuron.weights[
                                weight_index] -= learning_rate * weight_gradient

                        neuron.bias -= learning_rate * neuron_delta
                        hidden_layer_deltas.append(neuron_delta)
                        hidden_layer_gradients.append(neuron_gradients)

                    network_deltas.append(hidden_layer_deltas)
                    network_gradients.append(hidden_layer_gradients)

                    current_deltas = hidden_layer_deltas

    def predict(self, given_inputs, output_neuron_names):
        forward_pass = self.forward(given_inputs)
        outputs = forward_pass[-1]

        highest_output_neuron_index = np.argmax(outputs)

        return output_neuron_names[highest_output_neuron_index]

    def reset_neurons(self):
        self.__init__(self._init_data_set["input_amount"], self._init_data_set["output_amount"], self._init_data_set["hidden_layers"])