from synaport import custodian
from synaport.core import architecture
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

    def register_model(self, raw_config):
        model = SynaPortModel(raw_config)
        security_key = security.get_key()
        model_id = custodian.save_model(model, security_key)

        neuronal_network = architecture.build_nn_from_name(model.config["architecture_type"], model.config)

        app = {
            "synaport_model": model,
            "key": security_key,
            "model_id": model_id,
        }

        self.connected_models.append(app)

        return app, neuronal_network

    def start_server(self):
        pass