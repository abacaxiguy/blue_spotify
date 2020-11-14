from time import sleep
import ctypes
from sound import Sound

def mute_spotify():
    sleep(1)
    Sound.volume_set(20)

    windows = ctypes.windll.user32.EnumWindows    
    proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    get_window_text = ctypes.windll.user32.GetWindowTextW
    get_window_length = ctypes.windll.user32.GetWindowTextLengthW
    is_window_visible = ctypes.windll.user32.IsWindowVisible
    titles = []

    def foreach_window(hwnd, lParam):
        if is_window_visible(hwnd):
            length = get_window_length(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            get_window_text(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True

    windows(proc(foreach_window), 0)

    if "Advertisement" in titles:
        if not Sound.is_muted():
            Sound.mute() 
        print('MUTING...')

    else:
        if Sound.is_muted():
            Sound.mute()
           