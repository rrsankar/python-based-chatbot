import os
import random
import json
import datetime

# Get current working dir
CWD = os.getcwd()
print(CWD)

# SET PATH
USER_INFO_PATH = os.path.join(CWD, "user_info")

FLIGHTS_INFO_PATH = os.path.join(CWD, "flights", "flights")
with open(FLIGHTS_INFO_PATH, "r") as f:
    FLIGHTS_INFO = json.loads(f.read())

USER_HISTORY_PATH = os.path.join(CWD, "history")


class User:

    def __init__(self):
        super().__init__()
        self.username = ""
        self.user_data = {}

    def _create_user(self):
        new_user_file_path = os.path.join(USER_INFO_PATH, self.username)
        with open(new_user_file_path, "w") as new_user_f:
            new_user_f.write(json.dumps(self.user_data))

    def _get_user_info(self):
        user_data_path = os.path.join(USER_INFO_PATH, self.username)
        if os.path.exists(user_data_path):
            with open(user_data_path, "r+") as user_f:
                self.user_data = json.loads(user_f.read())

    def _convert_user_data_to_string(self):
        if self.user_data:
            output_string = ""
            for k, v in self.user_data.items():
                output_string += f"{k}: {v}\n"
            return output_string

    def _save_user_history(self):
        user_history_file_path = os.path.join(USER_HISTORY_PATH, self.username)
        history = {
            f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}": self.flight_list[self.flight_choice-1]
        }

        if os.path.exists(user_history_file_path):
            with open(user_history_file_path, "r") as hist_f:
                content = hist_f.read()
            if content:
                user_history = json.loads(content)
                user_history.update(history)
                write_content = json.dumps(user_history)
            else:
                write_content = json.dumps(history)

            with open(user_history_file_path, "w") as hist_f:
                hist_f.write(write_content)

        else:
            with open(user_history_file_path, "w+") as new_hist_f:
                new_hist_f.write(json.dumps(history))


class Flight:

    def __init__(self):

        super().__init__()
        self.flight_source = ""
        self.flight_destination = ""
        self.flight_choice = None

    def _get_list_of_flights(self):
        output_string = ""
        if all([self.flight_source, self.flight_destination]):
            self.flight_list = []
            flights = list(FLIGHTS_INFO.values())
            for i in flights:
                if i["start"] == self.flight_source and i["end"] == self.flight_destination:
                    self.flight_list.append(i)
            count = 1
            for i in self.flight_list:
                output_string += f"{count}. "
                for k, v in i.items():
                    output_string += f"{k}: {v}\t"
                output_string += f"\n"
                count += 1
        return output_string

    def _get_history(self):
        output_string = ""
        if all([self.username]):
            user_history_path = os.path.join(USER_HISTORY_PATH, self.username)
            if os.path.exists(user_history_path):
                with open(user_history_path, "r") as hist_f:
                    history_dict = json.loads(hist_f.read())
                count = 1
                for hist_key, hist_value in history_dict.items():
                    output_string += f"{count}. Date: {(datetime.datetime.strptime(hist_key, '%Y-%m-%d_%H-%M-%S'))} "
                    for val_k, val_v in hist_value.items():
                        output_string += f"{val_k}: {val_v} "
                    output_string += f"\n"
                    count += 1

        return output_string


class BaseBot(User, Flight):

    def __init__(self):
        super().__init__()
        self._stories()

    def _stories(self):
        self.story_beginning = [
            ("response", "utter_greet", "intent", "greet"),
            ("response", "ask_username", "intent", "username"),
        ]

        self.no_user_data_story = [
            ("response", "confirm_no_exist", "intent", "approve"),
            ("response", "ask_first_name", "intent", "first_name"),
            ("response", "ask_last_name", "intent", "last_name"),
            ("response", "ask_age", "intent", "age"),
            ("response", "ask_email", "intent", "email"),
            ("response", "ask_mobile", "intent", "mobile"),
            ("response", "ask_confirm_details", "intent", "confirm_details"),
        ]

        self.existing_user_data_story = [
            ("response", "confirm_data_exist", "intent", None),
            ("response", "display_user_data", "intent", None),
        ]

        self.story_ending = [
            ("response", "ask_service", "intent", "book_ticket"),
            ("response", "ask_source_airport", "intent", "source_airport"),
            ("response", "ask_destination_airport", "intent", "destination_airport"),
            ("response", "utter_flight_list", "intent", None),
            ("response", "ask_for_choice", "intent", "flight_choice"),
            ("response", "utter_flight_confirmation", "intent", None),
            ("response", "ask_additional_service", "intent", "booking_history"),
            ("response", "utter_history", "intent", None),
            ("response", "ask_additional_service", "intent", "deny"),
            ("response", "utter_good_day", "intent", "end_program"),
        ]

    def _display(self, text):
        print(text)

    def _fetch_input(self):
        input_text = input()
        return input_text

    def _action(self, intent, text):
        if intent == "username":
            self.username = text
            self._get_user_info()
        elif intent == "first_name":
            self.user_data["first_name"] = text
        elif intent == "last_name":
            self.user_data["last_name"] = text
        elif intent == "age":
            self.user_data["age"] = text
        elif intent == "email":
            self.user_data["email"] = text
        elif intent == "mobile":
            self.user_data["mobile"] = text
        elif intent == "confirm_details":
            self._create_user()
        elif intent == "source_airport":
            self.flight_source = text.strip().lower()
        elif intent == "destination_airport":
            self.flight_destination = text.strip().lower()
        elif intent == "flight_choice":
            self.flight_choice = int(text)
            self._save_user_history()
        elif intent == "end_program":
            exit()

    def conversation(self):
        """
        This function is to initiate the conversion.
        :return:
        """

        # Initial conversation
        for i in self.story_beginning:
            response_text = self._response(key=i[1])
            self._display(response_text)
            # Expecting an intent and take action.
            if i[3]:
                input_text = self._fetch_input()
                self._action(intent=i[3], text=input_text)

        # Case: User data exists.
        if self.user_data:
            for i in self.existing_user_data_story:
                response_text = self._response(key=i[1])
                self._display(response_text)
                if i[3]:
                    input_text = self._fetch_input()
                    self._action(intent=i[3], text=input_text)

        # Todo: User data does not exist.
        else:
            for i in self.no_user_data_story:
                response_text = self._response(key=i[1])
                self._display(response_text)
                # Expecting an intent and take action.
                if i[3]:
                    input_text = self._fetch_input()
                    self._action(intent=i[3], text=input_text)

        # Ending conversation
        for i in self.story_ending:
            response_text = self._response(key=i[1])
            self._display(response_text)
            # Expecting an intent and take action.
            if i[3]:
                input_text = self._fetch_input()
                self._action(intent=i[3], text=input_text)


class CheerfulBot(BaseBot):

    def __init__(self):
        super().__init__()
        self.character = "Sasha"

    def _response(self, key):
        responses = {
            "utter_greet": [
                f"Hi. This is {self.character}, how are you doing today?",
                f"Hello, my name is {self.character}, how are you?"
            ],
            "utter_good_day": [
                "Have a great day!",
                "Have a nice day!"
            ],
            "ask_username": [
                "May I know your username please?",
                "Can I get your username?"
            ],
            "confirm_data_exist": [
                "We have you in our system. Please find the details below."
            ],
            "display_user_data": [
                self._convert_user_data_to_string()
            ],
            "confirm_no_exist": [
                "Looks like we don't have your records on our system. Can I get some details from you?"
            ],
            "ask_first_name": [
                "May I know your first name please?",
                "Can I get your first name?"
            ],
            "ask_last_name": [
                "May I know your last name please?",
                "Can I get your last name?"
            ],
            "ask_age": [
                "May I know your age please?",
                "Can I get your age?"
            ],
            "ask_email": [
                "May I know your email please?",
                "Can I get your email?"
            ],
            "ask_mobile": [
                "May I know your mobile number please?",
                "Can I get your mobile number?"
            ],
            "ask_confirm_details": [
                "Can you confirm the above details?"
            ],
            "ask_service": [
                "How can I help you today?",
                "How may I be of service?"
            ],
            "ask_source_airport": [
                "Can I get the source airport please?",
                "Where are you planning to catch your flight from?"
            ],
            "ask_destination_airport": [
                "Where are you planning to travel to?",
                "Can I get the destination please?"
            ],
            "utter_flight_list": [
                self._get_list_of_flights()
            ],
            "ask_for_choice": [
                "Which flight do you want me to book for you?",
            ],
            "utter_flight_confirmation": [
                f"Your booking has been confirmed."
            ],
            "utter_history": [
                self._get_history()
            ],
            "ask_additional_service": [
                "Anything else I can help you with today?",
                "Can I help you with anything else today?"
            ]
        }

        # Return a random response from list.
        random_response = random.choice(responses[key])

        return random_response


# Todo: fill this up.
class GrumpyBot(BaseBot):

    def __init__(self):
        super().__init__()
        self.character = "Mark"

    def _response(self, key):
        responses = {
            "utter_greet": [
                f"This is {self.character}, how are you?",
            ],
            "utter_good_day": [
                "You do well.",
            ],
            "ask_username": [
                "What is your username?",
            ],
            "confirm_data_exist": [
                "We have you here."
            ],
            "display_user_data": [
                self._convert_user_data_to_string()
            ],
            "confirm_no_exist": [
                "Can't find you in our system. You have to give details first."
            ],
            "ask_first_name": [
                "What is your first name?"
            ],
            "ask_last_name": [
                "What is your last name?"
            ],
            "ask_age": [
                "What is your age?"
            ],
            "ask_email": [
                "What is your email?"
            ],
            "ask_mobile": [
                "What is your mobile?"
            ],
            "ask_confirm_details": [
                "Make sure the entered details are correct."
            ],
            "ask_service": [
                "What are you expecting from me today?"
            ],
            "ask_source_airport": [
                "Where do you want your ticket from?"
            ],
            "ask_destination_airport": [
                "Where are you going?"
            ],
            "utter_flight_list": [
                self._get_list_of_flights()
            ],
            "ask_for_choice": [
                "Select one number from the list above.",
            ],
            "utter_flight_confirmation": [
                f"Your booking is done."
            ],
            "utter_history": [
                self._get_history()
            ],
            "ask_additional_service": [
                "Do you want anything else?",
            ]
        }

        # Return a random response from list.
        random_response = random.choice(responses[key])

        return random_response


if __name__ == "__main__":

    print(f"Welcome to ABC airlines.\n"
          f"Please select a character.\n")
    print("1. Cheerful.\n"
          "2. Grumpy.\n")

    character = int(input())

    if character > 2:
        raise ValueError("Unknown option selected.")

    if character == 1:
        CheerfulBot().conversation()

    elif character == 2:
        GrumpyBot().conversation()

    else:
        raise ValueError("Selected character does not exist.")
