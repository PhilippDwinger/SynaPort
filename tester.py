from synaport import SynaPort
from synaport.model_creation import model_config

config = model_config.ModelConfig()
config.set_name("TestAi")
config.set_input_neuron_amount(10)
config.set_output_neuron_amount(1)
config.add_hidden_layer(5, "Sigmoid")

app = SynaPort("0.0.0.0", 5000)
app.register_model(config)

print(app)