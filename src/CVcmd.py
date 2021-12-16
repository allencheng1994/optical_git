class CV_Basic(object):
    def __init__(self, TheApplication):
        self.app = TheApplication

    def command(self, cmd):
        result = self.app.command(cmd)


class CV_CLASSIFIED(CV_Basic):
    def __init__(self, TheApplication):
        super().__init__(TheApplication)
        self.SystemFile = SystemFile(TheApplication)
        self.Material = Material(TheApplication)
        self.Field = Field(TheApplication)
        self.Wavelength = Wavelength(TheApplication)
        self.Tolerance = Tolerance(TheApplication)
        self.Compensator = Compensator(TheApplication)
        self.Buffer = Buffer(TheApplication)
        self.Plot = Plot(TheApplication)

    def command(self, cmd):
        pass


class SystemFile(CV_Basic):
    def __init__(self, TheApplication):
        super().__init__(TheApplication)
        self.zmxFile = ""
        self.plasticprv = ""

    def inputZMX(self, file):
        self.zmxFile = file
        cmd = 'in "C:/CODEV102/macro/zemaxtocv.seq" "' + self.zmxFile + '"'
        self.command(cmd)

    def inputPlastic(self, plasticprv="C:/CVUSER/plasticprv.seq"):
        self.plasticprv = plasticprv
        cmd = 'in "' + self.plasticprv + '"'
        self.command(cmd)

    def inputNew(self):
        cmd = "LEN NEW"
        self.command(cmd)

    def setTitle(self, title):
        cmd = 'TIT "' + title + '"'
        self.command(cmd)


class Field(CV_Basic):
    def __init__(self, TheApplication):
        super().__init__(TheApplication)

    def insertField(self, num):
        self.command("INS F" + str(num) + "+1")

    def setFieldTypeRIH(self):
        self.command("in CV_MACRO:cvsetfldtype RIH")

    def setIMH_RIH(self, field, imh):
        self.command("in CV_MACRO:cvsetfield Y " + str(imh) + " " + "F" + str(field))

    def setCRA(self):
        self.command("in cv_macro:cradjfz 1 21 1 1")

    def setWeight(self, field, weight):
        self.command("WTF F" + str(field) + " " + str(weight))


class Material(CV_Basic):
    def __init__(self, TheApplication):
        super().__init__(TheApplication)

    def setGL1(self, surface, material):
        self.command("GL1 " + surface + ' "' + material + '"')


class Wavelength(CV_Basic):
    def __init__(self, TheApplication):
        super().__init__(TheApplication)

    def setRGB(self):
        self.command(
            "WL 650 610 555 510 470; WTW 107 503 1000 503 91; CLS WVL RED RED"
            " CYA BLU MAG"
        )

    def set850(self):
        self.command(
            "WL 870 860 850 840 830; WTW 107 503 1000 503 91; CLS WVL RED RED"
            " CYA BLU MAG"
        )

    def setWave(self, wavelength, weight, line_color):
        wl_str = "WL "
        wtw_str = "WTW "
        color_str = "CLS WVL "

        for nm in wavelength:
            wl_str = wl_str + str(nm) + " "
        wl_str = wl_str + ";"

        for w in weight:
            wtw_str = wtw_str + str(w) + " "
        wtw_str = wtw_str + ";"

        for color in line_color:
            color_str = color_str + color

        cmd = wl_str + wtw_str + color_str
        self.command(cmd)


class Tolerance(CV_Basic):
    def __init__(self, TheApplication):
        super().__init__(TheApplication)

    def clear(self):
        self.command("DEL TOL SA")
        self.command("Buf Del b0")
        self.command("Buf Del b1")

    def tor(self):
        self.command("TOR")

    def torPTIC(self, frequency):
        self.tor()
        self.command("AZI F1..11 90")
        self.command("AZI F12..21 0")
        self.command("FRE F1..21 " + str(frequency))

    def dlx(self, surface, tol):
        self.command("DLX " + surface + " " + str(tol))

    def dly(self, surface, tol):
        self.command("DLY " + surface + " " + str(tol))

    def dsx(self, part, tol):
        self.command("DSX " + part + " " + str(tol))

    def dsy(self, part, tol):
        self.command("DSX " + part + " " + str(tol))

    def btx(self, part, tol):
        self.command("BTX " + part + " " + str(tol))

    def bty(self, part, tol):
        self.command("BTY " + part + " " + str(tol))

    def til(self, surface, tol):
        self.command("TIL " + surface + " " + str(tol))

    def dls(self, surface, tol):
        self.command("DLS " + surface + " " + str(tol))

    def dlt(self, surface, tol):
        self.command("DLT " + surface + " " + str(tol))


class Compensator(CV_Basic):
    def __init__(self, TheApplication):
        super().__init__(TheApplication)

    def dlt(self, unit, quan):
        self.command("CMP DLT " + unit + " " + str(quan))


class Plot(CV_Basic):
    def __init__(self, TheApplication):
        super().__init__(TheApplication)

    def plotGrid(self, runs=1000, upper=1, lower=0, step=0.1):
        self.command(
            "PLO GRD "
            + str(runs)
            + " "
            + str(upper)
            + " "
            + str(lower)
            + " "
            + str(step)
        )


class Buffer(CV_Basic):
    def __init__(self, TheApplication):
        super().__init__(TheApplication)

    def wmc(self, buffer):
        self.command("WBF " + buffer + " MC")

    def wpb(self, buffer):
        self.command("WBF PER " + buffer)


if __name__ == "__main__":
    pass
