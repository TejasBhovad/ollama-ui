import json
import datetime


class Logger:
    def __init__(self, filename="user_data.json"):

        self.filename = filename

    def log_user_input(self, user_input):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        print(data)
        data.append(
            {
                "timestamp": str(datetime.datetime.now()),
                "user_input": user_input,
            }
        )

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def log_response(self, param):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        # Convert data to a string before concatenating
        data_str = json.dumps(data)  # Convert data to JSON string

        print("Res: " + data_str)  # Concatenate string and string
        data[-1]["response"] = param
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)
