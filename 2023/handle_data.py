import threading, queue, time
from packets import PacketData
from window import app_window
_active = False
thread_queue = queue.Queue()
def _handle_session_data(data):
    match data.body.session_type:
        case 1:
            app_window.variables.session = 'P1'
        case 2:
            app_window.variables.session = 'P2'
        case 3:
            app_window.variables.session = 'P3'
        case 4:
            app_window.variables.session = 'P'
        case 5:
            app_window.variables.session = 'Q1'
        case 6:
            app_window.variables.session = 'Q2'
        case 7:
            app_window.variables.session = 'Q3'
        case 8:
            app_window.variables.session = 'Q'
        case 9:
            app_window.variables.session = 'OSQ'
        case 10:
            app_window.variables.session = 'R'
        case 11:
            app_window.variables.session = 'R2'
        case 12:
            app_window.variables.session = 'R3'
        case 13:
            app_window.variables.session = 'TT'
        case _: app_window.variables.session = ''
    app_window.variables.session_time_left = time.strftime('%H:%M:%S', time.gmtime(data.body.session_time_left))
    app_window.variables.total_laps = data.body.total_laps
    app_window.variables.pit_stop_window_ideal_lap = data.body.pit_stop_window_ideal_lap,
    app_window.variables.pit_stop_window_latest_lap = data.body.pit_stop_window_latest_lap,
    app_window.variables.pit_stop_rejoin_position = data.body.pit_stop_rejoin_position,
def _handle_data(bytes):
    global _active
    if _active: return thread_queue.task_done()
    if bytes[6] not in [1, 3, 4, 6, 7, 10, 11, 12]: return thread_queue.task_done()
    data = PacketData(bytes)
    match data.header.packet_id:
        case 1:
            _handle_session_data(data)
        case 3:
            pass
        case 4:
            pass
        case 6:
            pass
        case 7:
            pass
        case 10:
            pass
        case 11:
            pass
        case 12:
            pass
        case _:pass
    thread_queue.task_done()
def start(bytes):
    new_thread = threading.Thread(target=_handle_data, args = ([bytes]))
    thread_queue.put(new_thread)
    new_thread.start()
def stop():
    global _active
    _active = False
    thread_queue.join()