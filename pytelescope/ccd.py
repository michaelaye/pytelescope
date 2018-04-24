class CCD(object):
    def __init__(self, x=2048, y=2048, bits=15):
        self.x = x
        self.y = y
        self.bits_per_pixel = bits

    @property
    def n_pixels(self):
        return self.x * self.y

    @property
    def total_bits(self):
        return self.n_pixels * self.bits_per_pixel

    @property
    def total_mbits(self):
        return self.total_bits / (1024 * 1024)

    def __repr__(self):
        s = "{} x {} pixels per CCD\n".format(self.x, self.y)
        s += "N pixels: {}\n".format(self.n_pixels)
        s += "Dynamic range: {} bits\n".format(self.bits_per_pixel)
        s += "Total Mbits per CCD: {}\n".format(self.total_mbits)
        return s

    def __str__(self):
        return self.__repr__()
