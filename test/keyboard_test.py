import keyboard as kb

text = "Hello, World!"
kb.add_hotkey('Ctrl + /', lambda: kb.write('Speeching!'))
kb.add_hotkey('Ctrl + .', lambda: kb.write('Stop speeching!'))

kb.wait('esc')
kb.write(text, delay=0.1)