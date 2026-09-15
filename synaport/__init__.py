from synaport import custodian
from synaport.model_creation import SynaPortModel
import synaport.security as security

class SynaPort:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port

        self.connected_models = []

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return str(self.__dict__)

    def register_model(self, config):
        model = SynaPortModel(config)
        self.connected_models.append(config)
        security_key = security.get_key()
        model_id = custodian.save_model(config, security_key)

        app = {
            "model": model,
            "key": security_key,
            "model_id": model_id,
        }

        return app

    def start_server(self):
        pass