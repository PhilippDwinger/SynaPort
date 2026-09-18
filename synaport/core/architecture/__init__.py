from logging import warning

from synaport.core.architecture.dense_neuronal_network import DenseNeuronalNetwork

def build_dense_nn(config):
    neuronal_network = DenseNeuronalNetwork(config.input_amount, config.output_amount, config.hidden_layers)
    return neuronal_network

def build_nn_from_name(name, config):
    if name == "dense_neuronal_network":
        return build_dense_nn(config)
    else:
        warning(f"Unknown neural network name: {name}")
        return None