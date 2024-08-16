import aiohttp
import asyncio
import random
import edge_tts

async def fetch_audio(text, voiceName = "en-US-JennyNeural") -> bytes:
    communicate = edge_tts.Communicate(text, voiceName, pitch='+5Hz', rate='+22%')
    audio_bytes = b""
    async for element in communicate.stream():
        if element["type"] == 'audio':
            audio_bytes += element["data"]
    return audio_bytes


async def TextToSpeechBytes(Text) -> bytes:

        Data = str(Text).split(".")

        responses = ["The rest of the result has been printed to the chat screen, kindly check it out sir."
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."]

        if len(Data)>6 and len(Text)>=500:
            return await fetch_audio(" ".join(Text.split(".")[0:2])+ ". " + random.choice(responses))

        else:
            return await fetch_audio(Text)

if __name__ == "__main__":
    while True:
        print(TextToSpeechBytes(input(">>> ")))
