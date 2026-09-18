from synaport.custodian.bank import add_model, get_model

def save_model(config, security_key, neuronal_network, model_architecture=None):
    if model_architecture is None:
        model_architecture = []
    return add_model(config, security_key, neuronal_network, model_architecture)

def get_model_from_banker(config, model_id):
    return get_model(model_id)