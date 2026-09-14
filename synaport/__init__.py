from synaport.model_creation import SynaPortModel

class SynaPort:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port

        self.connected_models = []

    def register_model(self, config):
        model = SynaPortModel(config)
        self.connected_models.append(config)
        return model

    def start_server(self):
        pass