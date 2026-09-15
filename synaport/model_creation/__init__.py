from synaport.model_creation.model_config import normalize_model_config

class SynaPortModel:
    def __init__(self, raw_config):
        self.config = normalize_model_config(raw_config)
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return str(self.__dict__)