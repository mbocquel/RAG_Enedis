import json


class Config:
    """Config class which contains data, train and model hyperparameters"""

    def __init__(self, llm, chain):
        self.llm = llm
        self.chain = chain

    @classmethod
    def from_json(cls, cfg):
        """Creates config from json"""
        params = json.loads(json.dumps(cfg), object_hook=HelperObject)
        return cls(params.llm, params.chain)


class HelperObject(object):
    """Helper class to convert json into Python object"""
    def __init__(self, dict):
        self.__dict__.update(dict)