from itertools import product
from sklearn.utils import check_X_y, check_random_state
from sklearn.base import clone

def _flatten_parameters_list(parameters_list):
    """Flattens a dictionaries' list of parameters."""
    flat_parameters = []
    for parameters_dict in parameters_list:
        flat_parameters += [dict(zip(parameters_dict.keys(), parameter_product)) for parameter_product in product(*parameters_dict.values())]
    return flat_parameters

def check_datasets(datasets):
    """Checks that datasets is a list of (X,y) pairs or a dictionary of dataset-name:(X,y) pairs."""
    if isinstance(datasets, list):
        return {("dataset_" + str(ind + 1)):check_X_y(*dataset) for ind, dataset in enumerate(datasets)} 
    elif isinstance(datasets, dict):
        datasets_names = datasets.keys()
        are_all_strings = all([isinstance(dataset_name, str) for dataset_name in datasets_names])
        are_unique = len(list(datasets_names)) == len(set(datasets_names))
        if not are_all_strings or not are_unique:
            raise ValueError("The names of the datasets should be unique strings.")
        return {dataset_name:check_X_y(*dataset) for dataset_name, dataset in datasets.items()}
    else:
        raise ValueError("The datasets should be a list of (X,y) pairs or a dictionary of dataset-name:(X,y) pairs.")

def check_random_states(random_state, repetitions):
    """Creates random states for experiments."""
    return [check_random_state(random_state).randint(0, 2 ** 32 - 1) for ind in range(repetitions)]

def check_models(models, model_type):
    """Creates """
    try:
        flat_models = []
        for model_name, model, *param_grid in models:
            if param_grid == []:
                flat_models += [(model_name, model)]
            else:
                flat_parameters = _flatten_parameters_list(param_grid[0])
                for ind, parameters in enumerate(flat_parameters):
                    flat_models += [(model_name + str(ind + 1), clone(model).set_params(**parameters))]
    except: 
        raise ValueError("The {model_type}s should be a list of ({model_type} name, {model_type}) pairs or ({model_type} name, {model_type}, parameters grid) triplets.".format(model_type=model_type))
    return flat_models