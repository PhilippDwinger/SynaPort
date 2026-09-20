from synaport import banker, security
from synaport.core import architecture
from synaport.model_creation.model_config import ModelConfig

class SynaPortModel:
    def __init__(self, raw_config):
        model_config = ModelConfig()
        model_config.set_config_to_dict(raw_config)
        self.config = model_config

        model_security_key = security.get_key()
        model_architecture = architecture.build_nn_from_name(model_config.architecture_type, model_config)

        self.model_banker_id = banker.add_model(model_config, model_security_key, model_architecture)
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return str(self.__dict__)