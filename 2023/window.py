import os, tkinter as tk
class Window():
    def __init__(self):
        self.active = True

        # Window Root
        self.root = tk.Tk()
        self.variables = self.Variables()
        self.root.title('F1 App Window')
        self.root.wm_title('F1 App Window')
        self.root.iconphoto(False, tk.PhotoImage(file='{}/../img/F1.png'.format(os.path.dirname(os.path.abspath(__file__)))))
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.geometry('{}x{}+0+0'.format(self.root.winfo_screenwidth() - 50, self.root.winfo_screenheight() - 50))
        self.root.attributes('-zoomed', True)
        self.root.rowconfigure(1, weight=1)

        # Status Header Bar
        self.status_frame = tk.Frame(self.root)
        self.status_frame.grid(row=0,column=0,sticky=tk.NSEW)
        self.status_frame.rowconfigure(0, weight=1)
        self.status_frame.columnconfigure(3, weight=1)

        self.session_string = tk.StringVar()
        tk.Label(self.status_frame, textvariable=self.session_string, font=(None, 32)).grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)
        
        self.player_laps_string = tk.StringVar()
        tk.Label(self.status_frame, textvariable=self.player_laps_string, font=(None, 24)).grid(row=1, column=0, sticky=tk.E)
        tk.Label(self.status_frame, text='/', font=(None, 24)).grid(row=1, column=1, sticky=tk.EW)
        self.total_laps_string = tk.StringVar()
        tk.Label(self.status_frame, textvariable=self.total_laps_string, font=(None, 24)).grid(row=1, column=2, sticky=tk.W)
        
        self.session_time_left_string = tk.StringVar()
        tk.Label(self.status_frame, textvariable=self.session_time_left_string, font=(None, 16)).grid(row=2, column=0, columnspan=3, sticky=tk.EW)
        
        # Body Frame
        self.body_frame = tk.Frame(self.root)
        self.body_frame.grid(row=1,column=0,sticky=tk.NSEW)

        # Pit Window
        self.pit_frame = tk.Frame(self.body_frame)
        self.pit_frame.grid(row=0,column=0,sticky=tk.NSEW)
        self.pit_frame.columnconfigure(0, weight=1)

        tk.Label(self.pit_frame, text='Ideal Lap').grid(row=0, column=0, sticky=tk.EW)
        tk.Label(self.pit_frame, text='-').grid(row=0, column=1, sticky=tk.EW)
        self.pit_stop_window_ideal_lap_string = tk.StringVar()
        tk.Label(self.pit_frame, textvariable=self.pit_stop_window_ideal_lap_string).grid(row=0, column=2, sticky=tk.EW)

        tk.Label(self.pit_frame, text='Last Lap').grid(row=1, column=0, sticky=tk.EW)
        tk.Label(self.pit_frame, text='-').grid(row=1, column=1, sticky=tk.EW)
        self.pit_stop_window_latest_lap_string = tk.StringVar()
        tk.Label(self.pit_frame, textvariable=self.pit_stop_window_latest_lap_string).grid(row=1, column=2, sticky=tk.EW)

        tk.Label(self.pit_frame, text='Rejoin Pos').grid(row=2, column=0, sticky=tk.EW)
        tk.Label(self.pit_frame, text='-').grid(row=2, column=1, sticky=tk.EW)
        self.pit_stop_rejoin_position_string = tk.StringVar()
        tk.Label(self.pit_frame, textvariable=self.pit_stop_rejoin_position_string).grid(row=2, column=2, sticky=tk.EW)
        
    class Variables():
        session = ''
        session_time_left = ''
        player_laps = 'X'
        total_laps = ''
        pit_stop_window_ideal_lap = 0
        pit_stop_window_latest_lap = 0
        pit_stop_rejoin_position = 0
    def update(self):
        self.session_string.set(self.variables.session)
        self.session_time_left_string.set(self.variables.session_time_left)
        self.player_laps_string.set(self.variables.player_laps)
        self.total_laps_string.set(self.variables.total_laps)
        self.pit_stop_window_ideal_lap_string.set(self.variables.pit_stop_window_ideal_lap)
        self.pit_stop_window_latest_lap_string.set(self.variables.pit_stop_window_latest_lap)
        self.pit_stop_rejoin_position_string.set(self.variables.pit_stop_rejoin_position)
        self.root.update()
    def on_close(self):
        self.active = False
        self.update()
        self.destroy()
    def destroy(self):
        try:self.root.destroy()
        except:pass
app_window = Window()