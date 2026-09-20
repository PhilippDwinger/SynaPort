import copy
import json

from fastapi import FastAPI

import synaport
from synaport.core.architecture.dense_neuronal_network import serialize_neuronal_network, deserialize_neuronal_network


def create_app():
    fast_api_app = FastAPI()

    @fast_api_app.get("/")
    def root():
        return {
            "name": "Synaport",
            "status": "online",
        }

    @fast_api_app.get("/status")
    def status():
        return {}

    @fast_api_app.post("/model")
    def create_model(raw_config: dict):
        synaport_model = synaport.create_model(raw_config)
        return synaport_model.model_banker_id

    @fast_api_app.post("/model/pull")
    def get_model_banker_entry(data: dict):
        model_banker_id = data["model_id"]
        model = synaport.get_model(model_banker_id)
        model_copy = copy.deepcopy(model)

        neuronal_network = model_copy["neuronal_network"]
        raw_nn_architecture = serialize_neuronal_network(neuronal_network)
        json.dumps(raw_nn_architecture)
        model_copy["neuronal_network"] = raw_nn_architecture

        return model_copy

    @fast_api_app.post("/model/push")
    def set_model_banker_entry(data: dict):
        nn_architecture = deserialize_neuronal_network(data["raw_nn_architecture"])
        synaport.change_model_neuronal_network(data["model_id"], data["matching_config"], nn_architecture)

    @fast_api_app.post("/model/train")
    def train_model(data: dict):
        training_data = data["training_data"]
        iterations = data["iterations"]
        learning_rate = data["learning_rate"]
        learning_type = data["learning_type"]
        model_id = data["model_id"]

        return synaport.train_model(model_id, training_data, iterations, learning_type, learning_rate)

    @fast_api_app.delete("/model")
    def delete_model():
        pass

    @fast_api_app.post("/model/predict")
    def model_predict(data: dict):
        model_id = data["model_id"]
        input_data = data["input_data"]
        return synaport.predict_model(model_id, input_data)
    @fast_api_app.post("/model/reset")
    def reset_model():
        pass

    return fast_api_app