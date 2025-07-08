import asyncio
from dotenv import load_dotenv
import os
import time
from MicrophoneStream import MicrophoneStream
from AiAgentGpt import AiAgentGpt
from SpeechToText import SpeechToText
from TextToSpeech import TextToSpeech

try:
    import vlc
    play = True
except:
    print("Установите VLC (https://www.videolan.org/) для автоматической озвучки.")
    print("Альтернатива: вручную откройте файл в любом аудиоплеере.")
    play = False


def player(path):
    player_vlc = vlc.MediaPlayer(path)
    player_vlc.play()

    duration_ms = player_vlc.get_length()
    time.sleep(0.9)
    while player_vlc.is_playing():
        time.sleep((duration_ms / 1000.0) + 0.5)



if __name__ == '__main__':
    load_dotenv()
    name_file = r"media/only.wav"
    output = r"media/output.mp3"
    openai_key = os.getenv("OPENAI_API_KEY")
    deepgram_key = os.getenv("DEEPGRAM_API_KEY")

    while True:
        try:
            mic = MicrophoneStream()
            print("Говорите")
            mic.recordAndSave(name_file)
            print("Получаем текст с записи")
            stt = SpeechToText(token_key=deepgram_key)
            text = stt.responseOnlyText(name_file)
            print(f"Ваш сообщения: {text}")
            gtp = AiAgentGpt(token_key=openai_key, system_prompt="Отвечай в пару фраз, ты ассистент квантовой физики")
            text_gtp = gtp.getMessagesGtp(text)
            print(f"Тест от chatGPT: {text_gtp}")
            tts = TextToSpeech()
            asyncio.run(tts.createAudio(text_gtp, outputNameFile=output))
            print(f"Аудио файл создан: {output}")
            if play:
                player(output)
            else:
                input("Нажмите Enter, что бы продолжить общение !")

        except Exception as e:
            print(e)
