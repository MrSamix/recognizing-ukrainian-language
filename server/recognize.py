import os

def recognize_audio(files, model, language=None):
    result = ""
    print("Recognizing audio...")
    segments, info = model.transcribe(files, beam_size=5, language = language, vad_filter=True) # vad_filter=True
    # segments, info = model.transcribe(files[0], beam_size=5, language="ru")
    # segments, info = model.transcribe(filename, beam_size=7, language="uk")

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        result += segment.text
    print("FINISHED")
    return result
    # os.remove(files[0])
    # files.pop(0)