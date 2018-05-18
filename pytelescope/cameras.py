class Camera(object):
    def __init__(self, compression=5, fov=60,
                 n_bandpasses=4, **kwargs):

        self.compression = compression
        self.fov = fov
        self.n_bandpasses = n_bandpasses
        self.ccd = CCD(**kwargs)

    def __getattr__(self, attr):
        return getattr(self.ccd, attr)

    @property
    def ifov(self):
        ifovx = np.deg2rad(self.fov / self.ccd.x)
        ifovy = np.deg2rad(self.fov / self.ccd.y)
        return ifovx, ifovy

    @property
    def ifov_mrad(self):
        return self.ifov[0] * 1000, self.ifov[1] * 1000

    @property
    def img_compressed_size(self):
        return self.ccd.total_mbits / self.compression

    @property
    def img_set_size(self):
        return self.n_bandpasses * self.img_compressed_size

    def __repr__(self):
        s = self.ccd.__str__()
        s += "Compression: {}\n".format(self.compression)
        s += "Compressed per image: {} Mbits\n".format(
            self.img_compressed_size)
        s += "Bands: {}\n".format(self.n_bandpasses)
        s += "Set size compressed: {} Mbits\n".format(self.img_set_size)
        s += "IFOV_x/y [mrad]: {:.2f}/{:.2f}\n"\
            .format(self.ifov[0] * 1000, self.ifov[1] * 1000)
        return s


class VMC(Camera):


class SolarIrradiance:
    def __init__(self, wave1=200 * u.nm, wave2=1200 * u.nm, dlambda=1 * u.nm):
        self.wave1 = wave1
        self.wave2 = wave2
        self.dlambda = dlambda
        sol = SolarIrradianceSpectrum(TOTAL_IRRADIANCE_SPECTRUM_2000ASTM)
        sol.interpolate(dlambda=dlambda.to(u.micron).value,
                        ival_wavelength=(wave1.to(u.micron).value,
                                         wave2.to(u.micron).value))
        self.waves = sol.ipol_wavelength * u.micron  # b/c pyspectral works in micron
