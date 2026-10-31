# Step 5: speak with the Windows voice directly (pyttsx3 went silent after one use).
import pythoncom
import win32com.client

pythoncom.CoInitialize()
voice = win32com.client.Dispatch("SAPI.SpVoice")
voice.Speak("bottle, left, close")
