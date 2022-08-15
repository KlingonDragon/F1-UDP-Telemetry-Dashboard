class rgb:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.cyan = (0, 255, 255)
        self.magenta = (255, 0, 255)
        self.yellow = (255, 255, 0)
class hex:
    def __init__(self):
        self.white = '#FFFFFF'
        self.black = '#000000'
        self.red = '#FF0000'
        self.green = '#00FF00'
        self.blue = '#0000FF'
        self.cyan = '#00FFFF'
        self.magenta = '#FF00FF'
        self.yellow = '#FFFF00'
    def from_string(self, string):
        if len(string) == 7 and string[0] == '#': return string
        return self.__dict__[string.lower()]
def rgb_to_hex(r,g,b):
    return '#{:02X}{:02X}{:02X}'.format(r,g,b)