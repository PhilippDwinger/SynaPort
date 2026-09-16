import math
from synaport import SynaPort
from synaport.model_creation import model_config
import random

config = model_config.ModelConfig()
config.set_name("ClubBouncerAi")  # Coolerer Name!

# WICHTIG: Jetzt 3 Inputs für Alter, Dresscode und VIP-Status
config.set_input_neuron_amount(3)
config.set_output_neuron_amount(1)

# Ein etwas größerer Hidden Layer (6 Neuronen), da das Problem komplexer ist
config.add_hidden_layer(12, "relu", "he_uniform")

config.set_architecture_type("dense_neuronal_network")

app = SynaPort("0.0.0.0", 5000)
ai, nn = app.register_model(config)

# Trainingsdaten: ([Alter, Dresscode, VIP], [Einlass (0=Nein, 1=Ja)])
TrainingData = [
    ([0, 0, 0], [0]),  # Jung, unpassend, kein VIP -> Nein
    ([0, 1, 0], [0]),  # Jung, schick, kein VIP -> Nein
    ([1, 0, 0], [0]),  # Alt, unpassend, kein VIP -> Nein
    ([1, 1, 0], [1]),  # Alt, schick, kein VIP -> JA! (Standard-Gast)

    ([0, 0, 1], [1]),  # Jung, unpassend, ABER VIP -> JA!
    ([0, 1, 1], [1]),  # Jung, schick, UND VIP -> JA!
    ([1, 0, 1], [1]),  # Alt, unpassend, ABER VIP -> JA!
    ([1, 1, 1], [1]),  # Alt, schick, UND VIP -> JA!
]

# Da das Problem komplexer ist, nutzen wir eine stabile Lernrate
learningRate = 0.01
iterations = 30000  # 5.000 Runden reichen dank Sigmoid/Xavier dicke aus

# 1. Trainiere das Netzwerk NUR EINMAL richtig (z. B. mit 30.000 Runden)
print("Training läuft...")
nn.train(TrainingData, learningRate, iterations)
print("Training beendet!\n")

# 2. Teste JETZT alle 8 Gäste nacheinander, ohne das Netz dazwischen zurückzusetzen!
for index, entry in enumerate(TrainingData):
    inputs = entry[0]
    target = entry[1][0]

    # Vorhersage der KI holen
    output = nn.forward(inputs)[-1][0]
    error = abs(target - output) * 100

    print(
        f"Gast {index} | Input: {inputs} | Ziel: {target} | KI-Ausgabe: {round(output, 2)} | Fehler: {round(error, 1)}%")
