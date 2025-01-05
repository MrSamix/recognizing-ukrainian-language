error_callback = None
error_handling = False

def set_error_callback(callback):
    global error_callback
    error_callback = callback

def get_error_callback():
    return error_callback

def set_error_handling(state):
    global error_handling
    error_handling = state

def is_error_handling():
    return error_handling