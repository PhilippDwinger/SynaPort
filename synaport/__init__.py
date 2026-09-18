from synaport import custodian
from synaport.core import architecture
from synaport.model_creation import SynaPortModel
import uvicorn
from synaport.api import server
import synaport.security as security

class SynaPort:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port

        self.connected_models = []
        self._randomNumber = 0

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return str(self.__dict__)

    def register_model(self, raw_config):
        print("register_model: ", raw_config)
        model = SynaPortModel(raw_config)
        security_key = security.get_key()

        neuronal_network = architecture.build_nn_from_name(model.config.architecture_type, model.config)
        model_architecture = {
            "hidden_layers": neuronal_network.hidden_layers,
            "output_layer": neuronal_network.output_layer,
        }
        model_id = custodian.save_model(model, security_key, neuronal_network, model_architecture)

        app = {
            "synaport_model": model,
            "key": security_key,
            "model_id": model_id,
        }

        self.connected_models.append(app)

        return app, neuronal_network

    def get_model(self, model_id):
        self._randomNumber = 1
        return custodian.get_model_from_banker(model_id)

    def start_server(self):
        app = server.create_app(self)

        uvicorn.run(app, host=self.host, port=self.port)