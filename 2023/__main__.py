# Built in Modules
import threading
from sys import argv as cli_options

# My F1 Modules
import udp_listen
from window import app_window

if __name__ == "__main__":
    threads = []
    t = threading.Thread(target=udp_listen.start, args=([cli_options[1] if len(cli_options) >=2 else 20777]))
    threads.append(t)
    t.start()
    try:
        while app_window.active: app_window.update()
    except KeyboardInterrupt:pass
    print('Stopping. Please Wait.')
    udp_listen.stop()
    app_window.destroy()
    for t in threads: t.join()
else:
    app_window.destroy()