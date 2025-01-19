def recognize_audio(files, model, language=None):
    result = ""
    print("Recognizing audio...")
    segments, info = model.transcribe(files, beam_size=5, language = language, vad_filter=True)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    for segment in segments:
        # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)) # for debugging
        result += segment.text
    # print("FINISHED") # for debugging
    return result