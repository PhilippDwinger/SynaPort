from synaport import banker
from synaport.core.learning import reinforcement, supervised

def train_model(model_id, training_data, iterations, learning_type, learning_rate):
    model = banker.get_model(model_id)
    nn = model["neuronal_network"]

    if learning_type == "supervised":
        return supervised.train(nn, training_data, learning_rate, iterations, True)

    return None

