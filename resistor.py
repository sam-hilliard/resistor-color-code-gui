class Resistor:

    def __init__(self, bands, isPrecision):
        self.bands = bands
        self.isPrecision = isPrecision

    # determines the digits based on bands 1-3
    def getDigits(self):
        colorCode = {'black': '0', 'brown': '1', 'red': '2', 'orange': '3', 'yellow': '4',
                     'green': '5', 'blue': '6', 'violet': '7', 'grey': '8', 'white': '9'}
        digits = 0
        numDigits = 3 if self.isPrecision else 2
        strDigits = ''

        if len(self.bands) > 1:
            for i in range(numDigits):
                strDigits += colorCode[self.bands[i]]
            digits = int(strDigits)
        

        return digits

    # determines the mulitplier based on bands 3-4
    def getMultiplier(self):
        colorCode = {'black': 0, 'brown': 1, 'red': 2, 'orange': 3, 'yellow': 4,
                     'green': 5, 'blue': 6, 'violet': 7, 'grey': 8, 'white': 9, 'gold': -1, 'silver': -2}
        multNum = 3 if self.isPrecision else 2

        return colorCode[self.bands[multNum]]

    # determines the tolerance based 4-5
    def getTolerance(self):
        colorCode = {'brown': '1%', 'red': '2%', 'green': '0.50%', 'blue': '0.25%',
                     'violet': '0.10%', 'grey': '0.05%', 'gold': '5%', 'silver': '10%'}
        tolerance = ''

        if self.isPrecision:
            tolerance = colorCode[self.bands[4]]
        else:
            if len(self.bands) > 3:
                tolerance = colorCode[self.bands[3]]
            else:
                tolerance = '20%'

        return '\u00B1' + tolerance


    # determines the temperature coefficient based on band 6
    def getTempCo(self):
        colorCode = {'black': '250', 'brown': '100', 'red': '50', 'orange': '15', 'yellow': '25',
                     'green': '20', 'blue': '10', 'violet': '5', 'grey': '1'}

        if self.isPrecision and len(self.bands) > 5:
            return colorCode[self.bands[5]] + 'ppm/K'
        
        return ''

        
