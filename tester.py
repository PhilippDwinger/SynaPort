from synaport import SynaPort
from synaport.model_creation import model_config

config = model_config.ModelConfig()
config.set_name("AndGateAi")
config.set_input_neuron_amount(2)
config.set_output_neuron_amount(1)

config.add_hidden_layer(3, "relu", "he_uniform")
config.add_hidden_layer(2, "relu", "he_uniform")

config.set_architecture_type("dense_neuronal_network")

app = SynaPort("0.0.0.0", 5000)
ai, nn = app.register_model(config)

TrainingData = [
    ([0, 0], 0),
    ([0, 1], 0),
    ([1, 0], 0),
    ([1, 1], 1)
]
learningRate = 0.1
iterations = 1

nn.train(TrainingData, learningRate, iterations)