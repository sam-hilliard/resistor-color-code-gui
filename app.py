
import tkinter as tk
from tkinter import ttk
from resistor import Resistor


class App:

    def __init__(self):
        self.window = tk.Tk()
        self.fr_content = tk.Frame(self.window)
        self.menus = []
        self.menu_vars = []
        self.lbl_result = ttk.Label(self.fr_content)
        self.option = tk.IntVar()

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

        # radio button to select general purpose resistor calculation
        rb_general = ttk.Radiobutton(
            self.fr_content, text='General Purpose', variable=self.option, value=0, command=self.configMenus)
        rb_general.grid(row=1, column=0)

        # radio button to select precision resistor calculation
        rb_precision = ttk.Radiobutton(
            self.fr_content, text='Precision', variable=self.option, value=1, command=self.configMenus)
        rb_precision.grid(row=1, column=1)

        # displays the numerical value of the resistor based on user input
        self.lbl_result.configure(text='Resistor value: None')
        self.lbl_result.grid(row=2, column=0)

        tk.mainloop()

    # adds the drop down menus to the window
    def configMenus(self):
        # make sure no extra menus are left on the screen when switching between modes
        if len(self.menu_vars) > 0:
            for menu in self.menus:
                menu.destroy()
            self.menu_vars.clear()
            self.menus.clear()

        # makes sure label doesn't display previous value when switching options
        self.lbl_result.configure(text='Resistor value: None')

        # all possible colors to select from
        default_options = ['black', 'brown', 'red', 'orange', 'yellow',
                           'green', 'blue', 'violet', 'grey', 'white', 'gold',
                           'silver']

        # creates up to six drop downs where user will select band color from
        for i in range(6):
            # set so that the 'none' is both selected and a list item
            options = ['none', 'none']
            for j in range(len(default_options)):
                add_option = False
                # color code chart does not make use of every default color option for each section (tolerance, multiplier, etc...)
                if i == 3:
                    if j <= 6 or (j >= 10 and j <= 11):
                        add_option = True
                elif i == 4:
                    if (j > 0 and j < 3) or (j > 4 and j < 9) or (j > 9 and j < 12):
                        add_option = True
                elif i == 5:
                    if j < 9:
                        add_option = True
                else:
                    if j < 10:
                        add_option = True

                # only colors that correspond to the resistor code chart are adde
                if add_option:
                    options.append(default_options[j])

            if self.option.get() == 0 and (i == 2 or i == 5):
                continue

            menu_var = tk.StringVar(self.fr_content)
            menu = ttk.OptionMenu(self.fr_content, menu_var, *options)
            menu.grid(row=0, column=i, padx=5)
            self.menus.append(menu)
            self.menu_vars.append(menu_var)
            menu_var.trace_add('write', self.calculate)

    # interprets the number values of the drop downs to a numerical value
    def calculate(self, var, indx, mode):
        bands = []
        isValid = False

        # adds usable input from each drop down menu
        for menu_var in self.menu_vars:
            if menu_var.get() != 'none':
                bands.append(menu_var.get())
            else:
                break
        
        # determines if input given follows resistor color code
        if len(bands) == 1:
            if bands[0] == 'black':
                isValid = True
        else:
            if len(bands) > 2 and len(self.menus) - len(bands) <= 1:
                isValid = True

        if isValid:
            resistor =  Resistor(bands, True) if len(self.menus) > 4 else Resistor(bands, False)

            value = resistor.getDigits() * (10 ** resistor.getMultiplier())
            result = str(value) + '\u03A9 ' + resistor.getTolerance() + resistor.getTempCo()

            self.lbl_result.configure(text=f'Resistor value: {result}')

        else:
            self.lbl_result.configure(text='Resitor value: Invalid')
