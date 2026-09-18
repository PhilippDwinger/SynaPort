from fastapi import FastAPI

def create_app(synaport):
    fast_api_app = FastAPI()

    @fast_api_app.get("/")
    def root():
        return {
            "name": "Synaport",
            "status": "online",
        }

    @fast_api_app.post("/create")
    def create_ai_model(raw_config: dict):
        app, neuronal_network = synaport.register_model(raw_config)

        model_id = app["model_id"]

        print(model_id)

        return model_id

    @fast_api_app.post("/train")
    def train(data: dict):
        model_id = data["model_id"]
        train_data = data["train_data"]

        model = synaport.get_model(model_id)
        nn = model.neuronal_network

        nn.train(train_data)

        return {
            "status": "trained"
        }

    @fast_api_app.post("/predict")
    def predict(data: dict):
        model_id = data["model_id"]
        input_data = data["input_data"]
        output_neuron_names = data["output_neuron_names"]

        model = synaport.get_model(model_id)
        nn = model.neuronal_network

        return nn.predict(input_data, output_neuron_names)

    return fast_api_app