import math
import numpy as np

def he_uniform(fan_in, fan_out):
    limit = math.sqrt(6 / fan_in)
    return np.random.uniform(-limit, limit, (fan_out, fan_in))


def he_normal(fan_in, fan_out):
    standard_deviation = math.sqrt(2 / fan_in)
    return np.random.normal(0, standard_deviation, (fan_out, fan_in))


def xavier_uniform(fan_in, fan_out):
    limit = math.sqrt(6 / (fan_in + fan_out))
    return np.random.uniform(-limit, limit, (fan_out, fan_in))


def xavier_normal(fan_in, fan_out):
    standard_deviation = math.sqrt(2 / (fan_in + fan_out))
    return np.random.normal(0, standard_deviation, (fan_out, fan_in))


def orthogonal(fan_in, fan_out):
    shape = (fan_out, fan_in)

    if fan_out >= fan_in:
        matrix = np.random.normal(0, 1, shape)
        q, r = np.linalg.qr(matrix)
        q *= np.sign(np.diag(r))
        return q
    else:
        matrix = np.random.normal(0, 1, (fan_in, fan_out))
        q, r = np.linalg.qr(matrix)
        q *= np.sign(np.diag(r))
        return q.T