from synaport import SynaPort
from synaport.utils import normalizer

app = SynaPort()

test_dictionary = {
    "Name" : "TestName",
    "ActivationFunction" : "ReLu",
    "Addresses" : {
        "Max" : [1, 3],
        "Tom" : [4, 5],
        "Jim" : [6, 7],
    },
    "Alphabet" : ["A", "B", "C"],
    "Zahlen" : [1, 2, 3],
    "HardTest" : {
        "TestList" : [
            {"Name" : "TestName", "Age": 7}, 1, 3
        ]
    }
}

