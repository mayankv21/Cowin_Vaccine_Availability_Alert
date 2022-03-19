'''
return apllication config dictionary 
'''
import json


def getAppConfigDict(fName="secret/config.json")->dict:
    """ read config.json and return application configuration dictionary.

    Args:
        fName (str, optional): _description_. Defaults to "secret/config.json".

    Returns:
        dict: Application configuration dictionary
    """    
    # load config json into the dictionary
    with open(fName) as f:
        appConf = json.load(f)
        return appConf