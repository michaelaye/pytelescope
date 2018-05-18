import pandas as pd
import numpy as np

fname = "/Users/klay6683/Dropbox/Documents/VENUS/VDO/akatsuki_cameras.csv"
akatsuki_filters = pd.read_csv(fname, index_col=0)


class Filter:
    """Base Filter class

    Parameters
    ----------
    res : float
        Resolution of
    """

    def __init__(self, center, width, transmission, res=1):
        self.center = float(center)
        self.width = float(width)
        self.transmission = transmission
        self.resolution = res


class ConstantFilter(Filter):
    def response(self, wave1, wave2):
        wave1 = wave1.value
        wave2 = wave2.value
        leftside = self.center - self.width / 2
        rightside = self.center + self.width / 2
        waves = np.arange(wave1,
                          wave2+self.resolution,
                          self.resolution, dtype='float')
        response = np.zeros_like(waves)
        response[(waves > leftside) & (waves < rightside)] = self.transmission
        d = {}
        d['wavelength'] = waves
        d['response'] = response
        return d
