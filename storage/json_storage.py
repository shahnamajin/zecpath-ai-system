import json
import os


class JSONStorage:

    def save(self, data, folder, filename):

        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(folder, filename)

        with open(filepath, "w", encoding="utf-8") as file:

            json.dump(data, file, indent=4)

        return filepath