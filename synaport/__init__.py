from synaport import banker, model_creation
from synaport.core import architecture
from synaport.model_creation import SynaPortModel
import uvicorn
from synaport.api import server
import synaport.security as security
import synaport.core.learning as learning
import os

def create_model(raw_config: dict):
    synaport_model = SynaPortModel(raw_config)
    return synaport_model


def get_model(model_id: str):
    return banker.get_model(model_id)

def change_model_neuronal_network(model_id, config, nn):
    banker.change_neuronal_network(model_id, config, nn)


def train_model(model_id, training_data, iterations, learning_type, learning_rate):
    return learning.train_model(model_id, training_data, iterations, learning_type, learning_rate)


def predict_model(model_id, input_data):
    model = banker.get_model(model_id)
    nn = model["neuronal_network"]

    result = nn.forward(input_data)

    return result[-1]


class SynaPort:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port

        self.models = {}
        self.connections = {}

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return str(self.__dict__)

    def delete_model(self):
        pass

    def start(self, connection_mode="unsafe"):
        app = server.create_app()

        if connection_mode == "safe":
            uvicorn.run(
                app,
                host=self.host,
                port=self.port,
                ssl_keyfile="localhost+2-key.pem",
                ssl_certfile="localhost+2.pem",
            )
        elif connection_mode == "unsafe":
            uvicorn.run(app, host=self.host, port=self.port)
        else:
            raise ValueError("Invalid connection mode")

    def stop(self):
        pass

    def restart(self):
        os._exit(0)