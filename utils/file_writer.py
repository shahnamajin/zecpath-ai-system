import json


class FileWriter:

    def save(self, data, path):

        with open(path, "w", encoding="utf-8") as file:

            json.dump(data, file, indent=4)