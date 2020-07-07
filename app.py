
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from resistor import Resistor


class App:

    def __init__(self):
        self.window = tk.Tk()
        self.fr_content = tk.Frame(self.window)

        self.menus = []
        self.menu_vars = []
        self.fr_menus = tk.Frame(self.fr_content)

        self.fr_rbuttons = tk.Frame(self.fr_content)
        self.rb_general = tk.Radiobutton(self.fr_rbuttons)
        self.rb_precision = tk.Radiobutton(self.fr_rbuttons)
        self.option = tk.IntVar()

        self.fr_result = tk.Frame(self.fr_content)
        self.lbl_result = tk.Label(self.fr_result)
        self.lbl_value = tk.Label(self.fr_result)

    # displays the gui of the application
    def run(self):

        # setting window size and location
        winx = int(self.window.winfo_screenwidth() / 2 - 250)
        winy = int(self.window.winfo_screenheight() / 2 - 150)
        self.window.geometry('500x300+{}+{}'.format(winx, winy))
        self.window.title('Resistor color code converter')

        # configuring main content
        self.fr_content.configure(bg='#273c75')
        self.fr_content.pack(fill='both', expand=True)

        # add menus
        self.fr_menus.configure(bg='#273c75')
        self.fr_menus.grid(row=0, column=0, sticky='nsew', padx=10, pady=25)
        self.configMenus()

        # radio buttons
        self.fr_rbuttons.configure(bg='#273c75')
        self.fr_rbuttons.grid(
            row=1, column=0, sticky='nsew', padx=60, pady=(0, 30))
        # radio button to select general purpose resistor calculation
        self.rb_general.configure(text='General Purpose', variable=self.option, value=0,
                                  command=self.configMenus, bg='#273c75', fg='#f5f6fa', font=font.Font(family='Calibri', size=16))
        self.rb_general.grid(row=0, column=0)
        # radio button to select precision resistor calculation
        self.rb_precision.configure(text='Precision', variable=self.option, value=1, command=self.configMenus,
                                    bg='#273c75', fg='#f5f6fa', font=font.Font(family='Calibri', size=16))
        self.rb_precision.grid(row=0, column=1)

        # displays the numerical value of the resistor based on user input
        self.fr_result.configure(bg='#273c75')
        self.fr_result.grid(row=2, column=0, sticky='nsew', padx=(60, 0))

        self.lbl_result.configure(text='Resistor value: ', font=font.Font(
            family='Calibri', size=25), bg='#273c75', fg='#f5f6fa')
        self.lbl_result.grid(row=0, column=0, sticky='nsew')

        self.lbl_value.configure(text='None', font=font.Font(
            family='Calibri', size=25, weight='bold'), bg='#273c75', fg='#32ff7e')
        self.lbl_value.grid(row=0, column=1, sticky='nsew', padx=10)

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
        self.lbl_value.configure(text='None')

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
            menu = ttk.OptionMenu(self.fr_menus, menu_var, *options)
            menu.grid(row=0, column=i, padx=(0, 10))
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
            resistor = Resistor(bands, True) if len(
                self.menus) > 4 else Resistor(bands, False)

            value = self.formatResult(
                resistor.getDigits(), resistor.getMultiplier())
            result = str(value) + '\u03A9 ' + \
                resistor.getTolerance() + resistor.getTempCo()

            self.lbl_value.configure(text=result)

        else:
            self.lbl_value.configure(text='Invalid', font=('Helvetica', 20))

    def formatResult(self, digits, mult):
        formatted = ''
        prefix = ''
        exp = mult

        # kilo
        if mult >= 3 and mult < 6:
            exp -= 3
            prefix = 'k'
        # mega
        if mult >= 6 and mult < 9:
            exp -= 6
            prefix = 'M'
        # giga
        if mult >= 9:
            exp = 0
            prefix = 'G'

        digits = round(float(digits) * (10 ** exp), 2)
        digits = str(digits)
        if digits[-2:] == '.0':
            formatted = digits.replace('.0', '') + prefix
        else:
            formatted = digits + prefix

        return formatted
