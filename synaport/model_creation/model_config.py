from synaport.utils.normalizer import (
    create_master_dict,
    create_validation_rule,
    create_valid_dictionary_condition,
    create_valid_dictionary_structure,
    create_valid_list_structure, normalize_dict,
)
from synaport.utils.normalizer import create_valid_value as cv
from synaport.utils.normalizer import create_valid_type as ct

name_condition = create_valid_dictionary_condition(
    cv("Unnamed"),
    ct(str),
)

input_amount_condition = create_valid_dictionary_condition(
    cv(0),
    ct(int),
)

output_amount_condition = create_valid_dictionary_condition(
    cv(0),
    ct(int),
)

neuron_amount_condition = create_valid_dictionary_condition(
    cv(0),
    ct(int),
)

activation_function_condition = create_valid_dictionary_condition(
    cv("Sigmoid"),
    cv("ReLu"),
    cv("Tanh"),
)

hidden_layer_master_dict = create_master_dict(
    [
        "NeuronAmount",
        "ActivationFunction",
    ],
    [
        neuron_amount_condition,
        activation_function_condition,
    ],
)

hidden_layer_dictionary_structure = create_valid_dictionary_structure(
    hidden_layer_master_dict
)

hidden_layer_list_rule = create_validation_rule(
    hidden_layer_dictionary_structure,
)

hidden_layer_list_structure = create_valid_list_structure(
    hidden_layer_list_rule
)

hidden_layers_condition = create_valid_dictionary_condition(
    cv([]),
    hidden_layer_list_structure,
)

master_dict = create_master_dict(
    [
        "name",
        "input_amount",
        "output_amount",
        "hidden_layers",
    ],
    [
        name_condition,
        input_amount_condition,
        output_amount_condition,
        hidden_layers_condition,
    ],
)

def normalize_model_config(config):
    config_string = config.get_config_dict()
    normal_config = normalize_dict(config_string, master_dict)
    return normal_config

class ModelConfig:
    def __init__(self):
        self.name = None
        self.input_amount = None
        self.output_amount = None
        self.hidden_layers = []
    def __str__(self) -> str:
        return str(self.__dict__)
    def __repr__(self) -> str:
        return str(self.__dict__)
    def set_input_neuron_amount(self, input_amount):
        self.input_amount = input_amount
    def set_output_neuron_amount(self, output_amount):
        self.output_amount = output_amount
    def add_hidden_layer(self, neuron_amount, activation_function="ReLu"):
        self.hidden_layers.append({
            "NeuronAmount": neuron_amount,
            "ActivationFunction": activation_function
        })
    def set_hidden_layer_structure(self, hidden_layer_structure):
        self.hidden_layers = []
        for hidden_layer in hidden_layer_structure:
            if hidden_layer["NeuronAmount"] is not None and hidden_layer["ActivationFunction"] is not None:
                self.add_hidden_layer(hidden_layer["NeuronAmount"], hidden_layer["ActivationFunction"])
    def set_name(self, name):
        self.name = name
    def get_config_string(self):
        return str(self.__dict__)
    def get_config_dict(self):
        return self.__dict__

