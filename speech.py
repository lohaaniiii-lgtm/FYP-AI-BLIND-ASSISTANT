import threading
import queue

_q = queue.Queue()


def _worker():
    import pythoncom
    import win32com.client

    pythoncom.CoInitialize()
    voice = win32com.client.Dispatch("SAPI.SpVoice")
    while True:
        text = _q.get()
        print("speaking:", text)
        try:
            voice.Speak(text)
        except Exception as e:
            print("speech error:", e)


threading.Thread(target=_worker, daemon=True).start()


def say(text):
    _q.put(text)


def is_idle():
    return _q.empty()
