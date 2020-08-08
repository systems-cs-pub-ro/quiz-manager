import json


def openJsonConfig():
    with open('config.json') as json_file:
        conf = json.load(json_file)
    return conf


if __name__ == '__main__':
    config = openJsonConfig()
    print(config)

