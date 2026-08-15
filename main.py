from gtts import gTTS
text = "Hello, this is a test of the Google Text-to-Speech library."
tts = gTTS(text=text, lang=language_code)
tts.save("test.mp3")
print("Audio file 'test.mp3' has been created.")