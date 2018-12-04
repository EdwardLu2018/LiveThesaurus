## gets audio from the user

# CITATION: Audio code from: https://pythonspot.com/speech-recognition-using-google-speech-api/
import speech_recognition as sr
 
# records audio from computer and returns the audio as str
def getAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use "r.recognize_google(audio,
        # key="GOOGLE_SPEECH_RECOGNITION_API_KEY")"
        # instead of `r.recognize_google(audio)"
        audioText = r.recognize_google(audio)
        # print("Speech to Text: " + audioText)
        return audioText
    except sr.UnknownValueError:
        # print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        # print("Could not request results from Google Speech Recognition" + \
        #       "service; {0}".format(e))
        return None