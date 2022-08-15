import tkinter as tk, colour, time, sys, os
from tkinter.constants import W
from PIL import ImageTk as PIL_ImageTk, Image as PIL_Image
compass = {
    'ALL': tk.W+tk.E+tk.N+tk.S,
    'X': tk.W+tk.E,
    'Y': tk.N+tk.S,
    'N': tk.N,
    'E': tk.E,
    'S': tk.S,
    'W': tk.W,
    'U': tk.W+tk.E+tk.S,
    'L': tk.W+tk.S
}
hex = colour.hex().from_string
def img(filename):
    return '{}/img/{}'.format(os.path.dirname(os.path.abspath(__file__)),filename)
def new_frame(master, row, column, rowconfigure=[], columnconfigure=[], rowspan=1, columnspan=1, border=0, padding=None):
    frame = tk.Frame(master, padx=(padding if padding else border), pady=(padding if padding else border), borderwidth=border, relief='groove')
    try:
        frame.pack(fill=tk.BOTH, expand=1)
    except:
        pass
    for [r,w] in rowconfigure:
        frame.rowconfigure(r, weight=w)
    for [c,w] in columnconfigure:
        frame.columnconfigure(c, weight=w)
    frame.grid(row = row, column = column, rowspan=rowspan, columnspan=columnspan, sticky = compass['ALL'])
    return frame
def new_text_var():
    var = tk.StringVar()
    var.set(' ')
    return var
def label_text(master, text, row, column, font_size=16, bg=None, fg=None, border=0, rowspan=1, columnspan=1, sticky='ALL', border_style='groove', align=None, padding=None):
    label = tk.Label(master, text = text, font=(None, font_size), padx=(padding if padding else border), pady=(padding if padding else border), borderwidth=border, relief=border_style, justify=align)
    label.grid(row = row, column = column, rowspan=rowspan, columnspan=columnspan, sticky = compass[sticky])
    if bg:
        label.config(bg=hex(bg))
    if fg:
        label.config(fg=hex(fg))
    return label
def label_text_var(master, text, row, column, font_size=16, bg=None, fg=None, border=0, rowspan=1, columnspan=1, sticky='ALL', border_style='groove', align=None, padding=None):
    label = tk.Label(master, textvariable = text, font=(None, font_size), padx=(padding if padding else border), pady=(padding if padding else border), borderwidth=border, relief=border_style, justify=align)
    label.grid(row = row, column = column, rowspan=rowspan, columnspan=columnspan, sticky = compass[sticky])
    if bg:
        label.config(bg=hex(bg))
    if fg:
        label.config(fg=hex(fg))
    return label
def label_img(master, img, row, column, bg=None, fg=None, border=0, rowspan=1, columnspan=1, border_style='groove', align=None, padding=None):
    label = tk.Label(master, image = img, padx=(padding if padding else border), pady=(padding if padding else border), borderwidth=border, relief=border_style, justify=align)
    label.grid(row = row, column = column, rowspan=rowspan, columnspan=columnspan, sticky = compass['ALL'])
    label.image = img
    if bg:
        label.config(bg=bg)
    if fg:
        label.config(fg=fg)
    return label
def _weather_frame_(master, weather, time, row, column, columnspan=1):
    frame = new_frame(master, row, column, border=2, columnspan=columnspan, columnconfigure=[(0,1)])
    try:
        label_img(frame, weather, 0, 0)
    except:
        label_text(frame, weather, 0, 0)
    label_text(frame, time, 1, 0)
def _damage_pct_(percent):
    if percent:
        return '{:2.0f}%'.format(percent)
    return ''
def _damage_hex_(percent):
    if type(percent) != str:
        if percent <= 15:
            return '#00FF00'
        if percent <= 30:
            return colour.rgb_to_hex(int(255*(percent-15)//15),255,0)
        if percent <= 45:
            return colour.rgb_to_hex(255,255-int(255*(percent-30)//15),0)
        return '#FF0000'
    return '#FFFFFF'
def _temp_hex_(temp, tyre):
    if type(temp) != str:
        pct = int(2.55*10*abs(temp-100))
        if tyre == 'Wet':
            return '#FFFFFF'
        if tyre == 'Intermediate':
            return '#FFFFFF'
        if temp <= 90:
            return '#00FFFF'
        if temp <= 100:
            return colour.rgb_to_hex(0,255,pct)
        if temp <= 110:
            return colour.rgb_to_hex(pct,255,0)
        if temp <= 110:
            return colour.rgb_to_hex(255,255 - int(2.55*10*(abs(temp-100)-10)),0)
        return '#FF0000'
    return '#FFFFFF'
class window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title('F1 App Window')
        self.root.iconphoto(False, tk.PhotoImage(file=img('F1.png')))
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.geometry('{}x{}+0+0'.format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.root.attributes('-zoomed', True)
        self.active = True
        self._driver_list_ = []
        self._main_frame_ = tk.Frame(self.root)
        self._main_frame_.pack(fill=tk.BOTH, expand=1)
        self._main_frame_.columnconfigure(1, weight=1)
        self._main_frame_.rowconfigure(1, weight=1)
        self._terminal_ = tk.Listbox(self._main_frame_, bg='#300A24', fg='#FFFFFF', borderwidth=2)
        self._terminal_.grid(row=1, column=2, sticky = compass['ALL'])
        self._ip_data_ = new_text_var()
        label_text_var(self._main_frame_, self._ip_data_, 0, 2, 14, sticky='L', align=tk.LEFT).config(width=24)
        self._data_version_ = new_text_var()
        label_text_var(self._main_frame_, self._data_version_, 2, 2)
        self._timestamp_ = new_text_var()
        label_text_var(self._main_frame_, self._timestamp_, 2, 1)
        self.DSQ = False
        self.CHQF = False
        self._session_ = new_text_var()
        self._session_label_ = label_text_var(self._main_frame_, self._session_,0,0,60)
        self._sc_ = new_text_var()
        self._sc_label_ = label_text_var(self._main_frame_, self._sc_,0,1,60)
        self._left_frame_ = new_frame(self._main_frame_, 1, 0, [(4,1)], rowspan=2)
        label_text(self._left_frame_, 'Pit Strategy', 0, 0, 20)
        self._pit_frame_ = new_frame(self._left_frame_, 1, 0, border=2, columnconfigure=[(0,2),(1,1)])
        label_text(self._pit_frame_, 'Ideal Lap',1, 0)
        label_text(self._pit_frame_, 'Latest Lap',2, 0)
        label_text(self._pit_frame_, 'Rejoin Position',3, 0)
        label_text(self._pit_frame_, 'Extra Laps of Fuel',4, 0)
        self._pit_target_ = new_text_var()
        label_text_var(self._pit_frame_, self._pit_target_, 1, 1)
        self._pit_latest_ = new_text_var()
        label_text_var(self._pit_frame_, self._pit_latest_, 2, 1)
        self._pit_rejoin_ = new_text_var()
        label_text_var(self._pit_frame_, self._pit_rejoin_, 3, 1)
        self._extra_fuel_ = new_text_var()
        label_text_var(self._pit_frame_, self._extra_fuel_, 4, 1)
        label_text(self._left_frame_, 'Weather Forecast', 2, 0, 20)
        self._forecast_frame_ = new_frame(self._left_frame_, 4, 0)
        self._last_weather_ = ''
        self._last_forecast_ = []
        self._weather_imgs_ = {}
        for weather in ['Clear','Light Cloud', 'Overcast', 'Light Rain', 'Heavy Rain', 'Storm']:
            self._weather_imgs_[weather] = PIL_ImageTk.PhotoImage(PIL_Image.open(img('weather/{}.png'.format(weather))).resize((72,72)))
        self._car_frame_ = new_frame(self._main_frame_, 1, 1, rowconfigure=[(0,1),(8,1)], columnconfigure=[(0,1),(9,2)])
        self._last_tyre_ = ''
        self._tyre_damage_ = [new_text_var(),new_text_var(),new_text_var(),new_text_var()]
        self._tyre_damage_labels_ = [
            label_text_var(self._car_frame_, self._tyre_damage_[0], 3,1,40, sticky='X'),
            label_text_var(self._car_frame_, self._tyre_damage_[1], 3,8,40, sticky='X'),
            label_text_var(self._car_frame_, self._tyre_damage_[2], 5,1,40, sticky='X'),
            label_text_var(self._car_frame_, self._tyre_damage_[3], 5,8,40, sticky='X')
        ]
        self._tyre_temp_ = [new_text_var(),new_text_var(),new_text_var(),new_text_var()]
        self._tyre_temp_labels_ = [
            label_text_var(self._car_frame_, self._tyre_temp_[0], 2,1, sticky='E'),
            label_text_var(self._car_frame_, self._tyre_temp_[1], 2,8, sticky='W'),
            label_text_var(self._car_frame_, self._tyre_temp_[2], 6,1, sticky='E'),
            label_text_var(self._car_frame_, self._tyre_temp_[3], 6,8, sticky='W')
        ]
        self._tyres_ = [
            label_text(self._car_frame_, '│  ', 2,2,70,'black', rowspan=2, columnspan=2, sticky='E', border=2, border_style='raised'),
            label_text(self._car_frame_, '  │', 2,6,70,'black', rowspan=2, columnspan=2, sticky='W', border=2, border_style='raised'),
            label_text(self._car_frame_, '│  ', 5,2,70,'black', rowspan=2, columnspan=2, sticky='E', border=2, border_style='raised'),
            label_text(self._car_frame_, '  │', 5,6,70,'black', rowspan=2, columnspan=2, sticky='W', border=2, border_style='raised')
        ]
        self._wing_damage_ = [new_text_var(),new_text_var(),new_text_var()]
        self._wings_ = [
            label_text_var(self._car_frame_, self._wing_damage_[0], 1,3,40, columnspan=2, border=2, border_style='sunken'),
            label_text_var(self._car_frame_, self._wing_damage_[1], 1,5,40, columnspan=2, border=2, border_style='sunken'),
            label_text_var(self._car_frame_, self._wing_damage_[2], 7,3,40, columnspan=4, border=4, border_style='ridge')
        ]
        label_text(self._car_frame_, '═╬═', 2,4,80, rowspan=2, columnspan=2)
        label_text(self._car_frame_, ' ║ ', 4,4,80, columnspan=2)
        label_text(self._car_frame_, '═╩═', 5,4,80, rowspan=2, columnspan=2)
    def terminal(self, text):
        self._terminal_.insert(tk.END, '')
        for txt in str(text).split('\n'):
            self._terminal_.insert(tk.END, txt)
        self._terminal_.yview(tk.END) 
        print(text)
    def host (self, this_ip, port, f1_ip = ['...']):
        self._ip_data_.set('UDP Listening on\n    {}:{}\nData recieved from\n    {}'.format(this_ip, port, f1_ip[0]))
    def version_info(self, protocol, major, minor):
        self._data_version_.set('Data Version: {}\nGame Version: {}.{}'.format(protocol, major, minor))
    def driver_list(self, the_list=[]):
        self._driver_list_ = the_list
    def session(self, session):
        if session != 'None':
            self._session_.set(session)
        else:
            self._sc_.set('')
    def safety_car(self, sc):
        if sc != 'None':
            self._sc_.set('{} Safety Car'.format(sc))
        else:
            self._sc_.set('')
    def flag(self, flag):
        if flag == 'White':
            self._sc_label_ = label_text_var(self._main_frame_, self._sc_,0,1,60,bg='white')
            self._session_label_.config(bg='#FFFFFF')
            return
        if not (flag == 'CHQF' or flag == 'DSQ'):
            self._session_label_.config(bg=hex(flag if flag != 'None' else 'green'))
        if self.DSQ:return
        if flag == 'DSQ':
            self._sc_label_.config(bg=hex('black'))
            self.DSQ = True
            return
        if self.CHQF:return
        if flag == 'CHQF':
            chqf = PIL_ImageTk.PhotoImage(PIL_Image.open(img('CHQF.png')).resize((int(16*self._sc_label_.winfo_height()),self._sc_label_.winfo_height()),PIL_Image.NEAREST).crop((0,0,self._sc_label_.winfo_width(),self._sc_label_.winfo_height())))
            self._sc_label_.config(image = chqf)
            self._sc_label_.image = chqf
            self.CHQF = True
            return
        self._sc_label_.config(bg=hex(flag if flag != 'None' else 'green'))
    def pit_info(self, target, latest, rejoin):
        self._pit_target_.set(target)
        self._pit_latest_.set(latest)
        if rejoin:
            self._pit_rejoin_.set(rejoin)
        self._pit_frame_.update()
    def extra_fuel(self, extra_fuel):
        try:self._extra_fuel_.set(round(extra_fuel,1))
        except:self._extra_fuel_.set('')
    def weather_info(self, current, forecast=[]):
        if current != self._last_weather_:
            if current != 'None':
                self._last_weather_ = current
                _weather_frame_(self._left_frame_, self._weather_imgs_[current], 'Now', 3, 0)
            else:
                label_text(self._left_frame_, '', 3, 0)
        if forecast == []:
            self._last_forecast_ = forecast
            self._forecast_frame_.grid_forget()
            self._forecast_frame_.destroy()
            self._forecast_frame_ = new_frame(self._left_frame_, 4, 0)
            return
        s = ''
        y = 1
        x = 0
        for i in range(min(3,max(len(forecast),len(self._last_forecast_)))):
            x += 1
            if i<len(forecast):
                weather = forecast[i]
                if weather.session != s:
                    s = weather.session
                    y += 1
                    x = 0
                if (len(forecast) > len(self._last_forecast_) or str(weather) != str(self._last_forecast_[i])) and weather.weather and x < 5:
                    try:
                        _weather_frame_(self._forecast_frame_, self._weather_imgs_[weather.weather], '{}\n+{}m'.format(weather.session, weather.time_to_forcast), y, x)
                    except:
                        self.terminal('{} - {}\n    {} +{}m'.format(weather._weather_, weather.weather, weather.session, weather.time_to_forcast))
                continue
            label_text(self._forecast_frame_, '', y, x)
        self._last_forecast_ = forecast
    def tyre_compound(self, compound):
        if compound != self._last_tyre_:
            self._last_tyre_ = compound
            for tyre in self._tyres_:
                tyre.config(fg=hex({
                    '': 'black',
                    'None': 'black',
                    'Dry': 'black',
                    'Super Soft': 'magenta',
                    'Soft': 'red',
                    'Medium': 'yellow',
                    'Hard': 'white',
                    'Intermediate': 'green',
                    'Wet': 'cyan',
                    'C5': '#FF0099', #hyper soft
                    'C4': '#9900FF', #super soft
                    'C3': 'red',
                    'C2': 'yellow',
                    'C1': 'white'
                }[compound]))
    def damage(self, tyre_damage=[], wing = []):
        for i in range(4):
            self._tyre_damage_[i].set(_damage_pct_(tyre_damage[i]))
            self._tyre_damage_labels_[i].config(bg=_damage_hex_(tyre_damage[i]))
        for i in range(3):
            self._wing_damage_[i].set(_damage_pct_(wing[i]))
            self._wings_[i].config(bg=_damage_hex_(wing[i]))
    def tyre_temp(self, tyre_temps=[]):
        for i in range(4):
            self._tyre_temp_[i].set('{}℃'.format(tyre_temps[i]) if tyre_temps[i] else '')
            self._tyre_temp_labels_[i].config(bg=_temp_hex_(tyre_temps[i], self._last_tyre_))
    def penalty(self, penalty_data):
        self.terminal('-------------------------------------\n---------Incident Lap {}----------\n-------------------------------------'.format(penalty_data.lap))
        self.terminal('Car {}'.format((self._driver_list_[penalty_data.car] if penalty_data.car < len(self._driver_list_) else penalty_data.car)))
        self.terminal('{}{} - {}'.format(
            '{}{} '.format(
                '{}s'.format(penalty_data.time) if penalty_data.time > 0 else '',
                '{} Place'.format(penalty_data.grid_penalty) if penalty_data.grid_penalty > 0 else ''
            ), penalty_data.type, penalty_data.infringement))
        if penalty_data.other_car > 0:
            self.terminal('    on car {}'.format((self._driver_list_[penalty_data.other_car] if penalty_data.other_car < len(self._driver_list_) else penalty_data.other_car)))
        if penalty_data.places_gained > 0:
            self.terminal('Gained {} places'.format(penalty_data.places_gained))
        self.terminal('-------------------------------------')
    def speed_trap(self, speed_data):
        self.terminal('Speed Trap\nCar {} - {:.0f}kph{}'.format(
            (self._driver_list_[speed_data.car] if speed_data.car < len(self._driver_list_) else speed_data.car),
            speed_data.speed, ('\n    Fastest Speed in Session' if speed_data.session_fastest else '')
        ))
    def update(self):
        self._timestamp_.set(time.strftime('%Y-%m-%d %H:%M:%S'))
        self._main_frame_.update()
    def reset(self):
        self._driver_list_ = []
        self.session('')
        self.safety_car('None')
        self.DSQ = False
        self.CHQF = False
        self.flag('White')
        self.pit_info('','','')
        self.extra_fuel('')
        self.weather_info('None',[])
        self.tyre_compound('None')
        self.damage(['','','',''],['','',''])
        self.tyre_temp(['','','',''])
    def on_close(self):
        self.terminal('Closing graphical interface')
        self.active = False
        self.root.destroy()
if __name__ == '__main__':
    new_app = window()
    new_app.safety_car(input('SC Status: '))
    input('enter to end')
