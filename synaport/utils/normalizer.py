from typing import Any

#Utils
def _is_value_valid(value, valid_list) -> tuple[bool, None | list[Any] | dict[Any, Any]]:
    is_valid = False
    valid_values = None
    for valid_condition in valid_list:
        if valid_condition["_flag"] == "value":
            if valid_condition["value"] == value:
                is_valid = True
                break
        elif valid_condition["_flag"] == "type":
            if valid_condition["type"] == type(value):
                is_valid = True
                break
        elif valid_condition["_flag"] == "list_structure" and type(value) == list:
            result_list = normalize_list(value, valid_condition["structure"])
            if result_list:
                valid_values = result_list
                is_valid = True
                break
        elif valid_condition["_flag"] == "dictionary_structure" and type(value) == dict:
            result_list = normalize_dict(value, valid_condition["structure"])
            if result_list:
                valid_values = result_list
                is_valid = True
                break
    return is_valid, valid_values

#Norming
def normalize_list(input_list, validation_rule, cancel_at_differents=False):
    normed_list = []
    for item in input_list:
        item_is_valid, valid_values = _is_value_valid(item, validation_rule)

        if item_is_valid:
            if valid_values:
                normed_list.append(valid_values)
            else:
                normed_list.append(item)
        else:
            if cancel_at_differents: return None
    return normed_list

def normalize_dict(input_dict, master_dict, cancel_at_differents=False):
    normed_dict = {}
    for key, value in input_dict.items():
        if key in master_dict:
            condition = master_dict[key]

            if "_flag" in condition:
                other_valid_conditions = [condition]
                default_value = None
            else:
                other_valid_conditions = condition.get("other_valid_conditions")
                default_value = condition.get("default_value")
            is_valid, valid_values = _is_value_valid(value, other_valid_conditions)

            if is_valid:
                if valid_values:
                    normed_dict[key] = valid_values
                else:
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
    if default_value["_flag"] != "value" and default_value["_flag"] != "structure": return None
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

def create_valid_dictionary_structure(master_dict):
    if type(master_dict) != dict: return None
    return {
        "_flag": "dictionary_structure",
        "structure": master_dict,
    }

def create_valid_list_structure(validation_rule):
    if type(validation_rule) != list: return None
    return {
        "_flag": "list_structure",
        "structure": validation_rule,
    }