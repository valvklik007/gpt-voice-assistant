import speech_recognition

class MicrophoneStream:
    def __init__(self):
        self.__device  = 1
        self.__microphone = speech_recognition.Microphone(device_index=self.__device)
        self.__recognizer = speech_recognition.Recognizer()
        self.__recognizer.pause_threshold = 1.5

    def recordAndSave(self, nameFile: str):
        if not (isinstance(nameFile, str) and nameFile.endswith('.wav')):
            raise ValueError("Must be a string and format .wav")

        with self.__microphone:
            try:
                audio = self.__recognizer.listen(self.__microphone, timeout=2)
            except speech_recognition.UnknownValueError:
                print("The waiting time has passed")

        with (open(nameFile, 'wb')) as output:
            output.write(audio.get_wav_data())

    def __updateMicrophone(self):
        self.__microphone = speech_recognition.Microphone(device_index=self.__device)

    def setDevice(self, device):
        self.__device = device
        self.__updateMicrophone()

    def listDevice(self):
        for i, m in enumerate(self.__microphone.list_microphone_names()):
            print(f"Device {i}: {m}")