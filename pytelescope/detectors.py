from astropy import units as u
import pandas as pd
from matplotlib import pyplot as plt
from astropy.visualization import quantity_support


class Detector(object):
    """Camera detector class.

    Parameters
    ----------
    x : int
        Number of lines
    y : int
        Number of samples
    bits : int
        Dynamic range for digitization
    qe : pd.Series
        Quantum efficiency data for the detector.

    """

    def __init__(self, x, y, bits, qe):
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
        s += f"Total Mbits per detector: {self.total_mbits:.1f}\n"
        return s

    def __str__(self):
        return self.__repr__()


class QE:
    def __init__(self, fname):
        self.df = pd.read_csv(fname)
        self.df = self.df.sort_values(by='waves')

    @property
    def waves(self):
        return self.df.waves.values * u.nm

    @property
    def qe(self):
        return self.df.qe.values * u.percent

    def plot(self):
        with quantity_support():
            plt.figure()
            plt.plot(self.waves, self.qe)
            plt.title('QE')


cmosis_qe = QE(
    "/Users/klay6683/Dropbox/Documents/proposals/2018/VDO/cmosis_mono_qe.csv")

# class
#     def __init__(self, x, y, bits, qe_)
