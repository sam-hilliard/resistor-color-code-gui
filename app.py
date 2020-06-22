
import tkinter as tk
from tkinter import ttk
from resistor import Resistor


class App:

    def __init__(self):
        self.window = tk.Tk()
        self.fr_content = tk.Frame(self.window)
        self.menu_vars = []

    # displays the gui of the application
    def run(self):
        # setting window size and location
        winx = int(self.window.winfo_screenwidth() / 2 - 250)
        winy = int(self.window.winfo_screenheight() / 2 - 150)
        self.window.geometry('500x300+{}+{}'.format(winx, winy))
        self.window.title('Resistor color code converter')

        # configuring main content
        self.fr_content.pack(fill='both', expand=True)
        self.configMenus()

        tk.mainloop()

    # adds the drop down menus to the window
    def configMenus(self):
        default_options = ['black', 'brown', 'red', 'orange', 'yellow',
                           'green', 'blue', 'violet', 'grey', 'white', 'gold',
                           'silver', 'none']

        for i in range(6):
            options = ['none', 'none']
            for j in range(len(default_options)):
                add_option = False
                if i == 3:
                    if j <= 6 or (j >= 10 and j <= 11):
                        add_option = True
                elif i == 4:
                    if (j > 0 and j < 3) or (j > 4 and j < 8) or (j > 9 and j < 12):
                        add_option = True
                elif i == 5:
                    if j < 9:
                        add_option = True
                else:
                    if j < 10:
                        add_option = True

                if add_option:
                    options.append(default_options[j])
            menu_var = tk.StringVar(self.fr_content)
            menu = ttk.OptionMenu(self.fr_content, menu_var, *options)
            menu.grid(row=1, column=i, padx=5)
            self.menu_vars.append(menu_var)
            menu_var.trace_add('write', self.calculate)

    # interprets the number values of the drop downs to a numerical value
    def calculate(self, var, indx, mode):
        bands = []

        for var in self.menu_vars:
            bands.append(var.get())

        resistor = Resistor(bands)
        numBands = resistor.getNumBands()