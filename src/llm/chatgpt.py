import os
import openai

from src.utils.timeouthandler import retry_with_timeout

class ChatGPT:
    def __init__(self, temperature : float = 0.5, model : str = "gpt-3.5-turbo", user_delimiter : str = "*u*", assistant_delimiter : str = "*a*") -> None:
        self.user_delimiter = user_delimiter
        self.assistant_delimiter = assistant_delimiter
        self.model = model
        self.messages = []
        self._temperature = temperature
        openai.api_key = os.environ["OPENAI_API_KEY"]

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value : float) -> None:
        if value >= 0 and value <= 1:
            self._temperature = value

    def add_system_message(self, message: str) -> None:
        self.messages.append({"role": "system", "content": message})

    def add_assistant_message(self, message: str) -> None:
        self.messages.append({"role": "assistant", "content": f"{self.assistant_delimiter}{message}{self.assistant_delimiter}"})
    
    def add_user_message(self, message: str) -> None:
        self.messages.append({"role": "user", "content": f"{self.user_delimiter}{message}{self.user_delimiter}"})

    @retry_with_timeout(max_retries=4,timeout_s=8,wait_time=2)
    def get_response(self, message: str, add_to_history : bool = False) -> str:
        new_msg = {"role": "user", "content": f"{self.user_delimiter}{message}{self.user_delimiter}"}
        msgs = self.messages + [new_msg]

        if add_to_history:
            self.messages.append(new_msg)
       
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=msgs,
            temperature=self.temperature,
            timeout=10
        )


        choice = completion["choices"][0]
        response = choice["message"]

        if "content" in choice["message"].keys():
            res = response["content"].replace(self.assistant_delimiter, "")

            if add_to_history:
                self.messages.append({"role": "assistant", "content": f"{self.assistant_delimiter}{res}{self.assistant_delimiter}"})

            return res
        else:
            raise Exception("No content in response")