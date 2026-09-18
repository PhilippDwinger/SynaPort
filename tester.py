import math
from asyncio import start_server

import synaport
from synaport import SynaPort
from synaport.model_creation import model_config
import random

config = model_config.ModelConfig()
#config.set_name("ClubBouncerAi")  # Coolerer Name!

# WICHTIG: Jetzt 3 Inputs für Alter, Dresscode und VIP-Status
#config.set_input_neuron_amount(3)
#config.set_output_neuron_amount(1)

# Ein etwas größerer Hidden Layer (6 Neuronen), da das Problem komplexer ist
#config.add_hidden_layer(12, "leaky_relu", "he_uniform")

#config.set_architecture_type("dense_neuronal_network")

config_dict = {
    "name" : "ClubBouncerAi",
    "input_amount" : 3,
    "output_amount" : 1,
    "hidden_layers" : [{"NeuronAmount" : 3, "ActivationFunction" : "leaky_relu", "InitializationFunction" : "he_uniform"}],
    "architecture_type" : "dense_neuronal_network"
}

app = SynaPort("0.0.0.0", 5000)
#ai, nn = app.register_model(config_dict)

app.start_server()