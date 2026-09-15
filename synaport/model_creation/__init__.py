from synaport.model_creation.model_config import normalize_model_config

class SynaPortModel:
    def __init__(self, raw_config):
        self.config = normalize_model_config(raw_config)