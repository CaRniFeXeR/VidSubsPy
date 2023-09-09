from src.datastructures.transcript import Transcript
from src.llm.chatgpt import ChatGPT
from copy import deepcopy

class TranscriptTranslator:

    def __init__(self, target_lang : str) -> None:
        self.target_lang = target_lang
        self.system_message = f"""
       Please translate the following text into {target_lang}? 
       Respond with nothing else except the resulting translated text.
       No explainations or other text."""


    def translate(self, transcript : Transcript) -> Transcript:
        # make sure to return a new object
        translated_trans = deepcopy(transcript)
        for seg in translated_trans.segments:
            chatGPT = ChatGPT()
            chatGPT.add_system_message(self.system_message)
            response = chatGPT.get_response(seg.text).replace("*u*","")
            print("translated: \n", seg.text, "\nto: \n", response)
            seg.text = response

        return translated_trans

