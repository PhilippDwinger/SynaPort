from synaport.utils.normalizer import create_master_dict, create_validation_rule, create_valid_dictionary_condition
from synaport.utils.normalizer import create_valid_value as cv
from synaport.utils.normalizer import create_valid_type as ct

config_master_dictionary = create_master_dict(
    ["Name", "InputNeurons", "HiddenLayers", "OutputNeurons", "ActivationFunction", "LearningRate"],
    create_validation_rule(
        create_valid_dictionary_condition(cv("Unnamed"), ct(str)),
        create_valid_dictionary_condition(cv(1), ct(int)),
        create_valid_dictionary_condition(cv([1]), ct(list)),
        create_valid_dictionary_condition(cv(1), ct(int)),
        create_valid_dictionary_condition(cv(["ReLu"]), ct(list)),
        create_valid_dictionary_condition(cv(0.1), ct(float)),
    ),
)

class SynaPortModel:
    def __init__(self, config):
        self.config = config
