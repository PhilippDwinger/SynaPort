#Utils
def _is_value_valid(value, valid_list) -> bool:
    is_valid = False
    for valid_condition in valid_list:
        if valid_condition["_flag"] == "value":
            if valid_condition["value"] == value:
                is_valid = True
                break
        elif valid_condition["_flag"] == "type":
            if valid_condition["type"] == type(value):
                is_valid = True
                break
    return is_valid

#Norming
def normalize_list(input_list, list_validation_rule, cancel_at_differents=False):
    normed_list = []
    for item in input_list:
        item_is_valid = _is_value_valid(item, list_validation_rule)

        if item_is_valid:
            normed_list.append(item)
        else:
            if cancel_at_differents: return None
    return normed_list

def normalize_dict(input_dict, master_dict, cancel_at_differents=False):
    normed_dict = {}
    for key, value in input_dict.items():
        if key in master_dict:
            other_valid_conditions = master_dict[key].get("other_valid_conditions")
            default_value = master_dict[key].get("default_value")

            is_valid = _is_value_valid(value, other_valid_conditions)

            if is_valid:
                normed_dict[key] = value
            else:
                if cancel_at_differents: return None
                normed_dict[key] = default_value["value"]

    for key in master_dict:
        if key not in normed_dict:
            default_value = master_dict[key]["default_value"]
            normed_dict[key] = default_value["value"]

    return normed_dict

#Create master class
def create_master_dict(key_list, all_valid_value_lists):
    master_dict = {}
    for key, value in zip(key_list, all_valid_value_lists):
        master_dict[key] = value
    return master_dict

#Rule creation
def create_validation_rule(*args):
    """If the validation rule is for a dictionary, the args need to be 'dictionary_conditions'!"""
    valid_conditions = []
    for arg in args:
        valid_conditions.append(arg)
    return valid_conditions

#Instance creation
def create_valid_dictionary_condition(default_value, *args):
    """Given parameters must be a dictionary with the type 'valid_value'!"""
    if default_value["_flag"] != "value": return None
    valid_conditions = []
    for arg in args:
        if arg == default_value: continue
        valid_conditions.append(arg)

    valid_conditions.append(default_value)

    valid_condition_list = {
        "default_value": default_value,
        "other_valid_conditions": valid_conditions
    }
    return valid_condition_list

def create_valid_value(value):
    return {
        "_flag": "value",
        "value": value
    }

def create_valid_type(allowed_type):
    return {
        "_flag": "type",
        "type": allowed_type,
    }

def create_valid_structure(structure):
    return {
        "_flag": "structure",
        "structure": structure
    }