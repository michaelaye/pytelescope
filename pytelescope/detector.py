from astropy import units as u


class CCD(object):
    def __init__(self, x=2048, y=2048, bits=15):
        self.x = x
        self.y = y
        self.dynamic_range = bits * u.bit

    @property
    def n_pixels(self):
        return self.x * self.y

    @property
    def total_bits(self):
        return self.n_pixels * self.dynamic_range

    @property
    def total_mbits(self):
        return self.total_bits.to(u.Mbit)

    def __repr__(self):
        s = f"{self.x} x {self.y}\n"
        s += f"N pixels: {self.n_pixels}\n"
        s += f"Dynamic range: {self.dynamic_range}\n"
        s += f"Total Mbits per CCD: {self.total_mbits:.1f}\n"
        return s

    def __str__(self):
        return self.__repr__()
