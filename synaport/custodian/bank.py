models = {}
_next_id = 0

def get_next_id():
    global _next_id
    _next_id += 1
    return _next_id

def get_free_id():
    global models
    max_count = len(models) + 100
    count = 0
    while count < max_count:
        count += 1
        current_id = get_next_id()
        if models.get(current_id) is None:
            return current_id
    return None

def get_model(model_id):
    return models[model_id]

def add_model(config, security_key):
    global models
    model_id = get_free_id()
    banker_entry = {
        "id": model_id,
        "config": config,
        "security_key": security_key,
        "architecture" : [],
    }
    models[model_id] = banker_entry
    return model_id