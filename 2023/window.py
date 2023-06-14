import os, tkinter as tk
class Window():
    def __init__(self):
        self.active = True
        self.root = tk.Tk()
        self.variables = self.Variables()
        self.root.title('F1 App Window')
        self.root.wm_title('F1 App Window')
        self.root.iconphoto(False, tk.PhotoImage(file='{}/../img/F1.png'.format(os.path.dirname(os.path.abspath(__file__)))))
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.geometry('{}x{}+0+0'.format(self.root.winfo_screenwidth() - 50, self.root.winfo_screenheight() - 50))
        self.root.attributes('-zoomed', True)
        self.session_string = tk.StringVar()
        tk.Label(self.root, textvariable=self.session_string).grid(row=0, column=0, sticky=tk.NW)
    class Variables():
        session = None
    def update(self):
        self.session_string.set(self.variables.session)
        self.root.update()
    def on_close(self):
        self.active = False
        self.update()
        self.destroy()
    def destroy(self):
        try:self.root.destroy()
        except:pass
app_window = Window()