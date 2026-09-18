from synaport.model_creation.model_config import ModelConfig
class SynaPortModel:
    def __init__(self, raw_config):
        model_config = ModelConfig()
        model_config.set_config_to_dict(raw_config)
        self.config = model_config
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return str(self.__dict__)