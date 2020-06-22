class Resistor:

    def __init__(self, bands):
        self.bands = bands

    # determines the digits based on bands 1-3
    def getDigits(self):
        print('getting digits')

    # determines the mulitplier based on bands 3-4
    def getMultiplier(self):
        print('getting the multiplier')

    # determines the tolerance based 4-5
    def getTolerance(self):
        print('gettting tolerance')

    # determines the temperature coefficient based on band 6
    def getTempCo(self):
        print('getting the temp coefficient')

    def getNumBands(self):
        bandNum = 0
        isNone = False
        

        for band in self.bands:
            if band == 'none':
                isNone = True
            else:
                if not isNone:
                    bandNum += 1
                else:
                    bandNum = -1

        if bandNum == 1 and self.bands[0] != 'black':
            return -1


        return bandNum

    def toString(self):
        return 'hi'
