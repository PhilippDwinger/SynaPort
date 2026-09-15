import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
def sigmoid_derivative(x):
    return x * (1 - x)

def tanh(x):
    return math.tanh(x)
def tanh_derivative(x):
    return 1 - x ** 2

def relu(x):
    return max(0, x)
def relu_derivative(x):
    return 1 if x > 0 else 0