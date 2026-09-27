import uuid
from logging import warning

models = {}

def get_id():
    return str(uuid.uuid4())

def get_free_id():
    max_count = len(models) + 100
    for _ in range(max_count):
        uuid_id = str(uuid.uuid4())
        if not models.get(uuid_id):
            return uuid_id
    warning(f"No free id found! {max_count} trys.")
    return None

def get_model(model_id):
    return models[model_id]

def add_model(config, security_key, neuronal_network):
    global models
    model_id = get_free_id()
    if not model_id: return None
    banker_entry = {
        "id": model_id,
        "config": config,
        "security_key": security_key,
        "neuronal_network" : neuronal_network
    }
    models[model_id] = banker_entry
    print("Added model", model_id)
    return model_id

def change_neuronal_network(model_id, config, neuronal_network):
    global models
    print("Changing neuronal network", model_id)
    entry = models[model_id]
    entry["config"] = config
    entry["neuronal_network"] = neuronal_network