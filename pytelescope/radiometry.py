import math

import astropy.units as u
import numpy as np
import pandas as pd
from astropy.constants import c, h
from scipy.interpolate import InterpolatedUnivariateSpline

from planetpy.constants import earth, mars
from pyspectral.solar import (TOTAL_IRRADIANCE_SPECTRUM_2000ASTM,
                              SolarIrradianceSpectrum)

dic = {
    'A_t': 5e-3 * u.m*u.m,
    'A_p': 1.69e-10 * u.m*u.m,
    'f': 1.3 * u.m,
    'T_M1': 0.92,
    'T_M2': 0.92,
    'T_s': 0.94,
}


class Response:


class Radiometry:
    E_w_unit_in = u.Watt/u.m/u.m/u.micron
    E_w_unit_out = u.Watt/u.m/u.m/u.nm
    E_ph_unit = 1/(u.s*u.m*u.m*u.nm)
    lw = 0.75
    rootpath = Path("/Users/klay6683/Documents/proposals/2018/MAPSE/")

    def __init__(self, wave1=200*u.nm, wave2=1200*u.nm, dlambda=1*u.nm,
                 i=75*u.deg, d=1.5):
        self.wave1 = wave1
        self.wave2 = wave2
        self.dlambda = dlambda
        self.i = i  # incidence angle
        self.d = d  # Mars distance in AU (scaling the solar flux)
        sol = SolarIrradianceSpectrum(TOTAL_IRRADIANCE_SPECTRUM_2000ASTM)
        sol.interpolate(dlambda=dlambda.to(u.micron).value,
                        ival_wavelength=(wave1.to(u.micron).value,
                                         wave2.to(u.micron).value))
        self.waves = (sol.ipol_wavelength*u.micron).to(u.nm)
        self.E_w = (sol.ipol_irradiance*self.E_w_unit_in).to(self.E_w_unit_out)

        self.read_reflectance()
        self.read_QE()
        for k, v in dic.items():
            setattr(self, k, v)

    def read_reflectance(self):
        df = pd.read_csv(self.rootpath / 'giza_crism_blue_halos.csv')
        df = df.sort_values(by='Wavelength[nm]')
        pre_data = pd.DataFrame([[200, 0.02]], columns=df.columns)
        self.reflectance = pd.concat([pre_data, df])

    def read_QE(self):
        df = pd.read_csv(self.rootpath / 'midband_coated_QE.csv')
        df = df.sort_values(by='Wavelength[nm]')
        pre_data = pd.DataFrame([[225, 0.0]], columns=df.columns)
        post_data = pd.DataFrame([[1100, 0.0]], columns=df.columns)
        self.QE = pd.concat([pre_data, df, post_data])

    @property
    def QE_rsr(self):
        d = {}
        d['wavelength'] = self.QE.iloc[:, 0]
        d['response'] = self.QE.iloc[:, 1]/100.0
        return d

    @property
    def rsr(self):
        d = {}
        d['wavelength'] = self.reflectance.iloc[:, 0]
        d['response'] = self.reflectance.iloc[:, 1]
        return d

    @property
    def refl_ipol(self):
        ius = InterpolatedUnivariateSpline(self.rsr['wavelength'],
                                           self.rsr['response'],
                                           k=1)
        return ius(self.waves.value)

    def plot_E_w(self, ax=None):
        xlim = [self.wave1.value, self.wave2.value]

        if ax is None:
            _, ax = plt.subplots(figsize=(8, 4))

        ax.plot(self.waves, self.E_w, lw=self.lw)
        ax.set_xlim(xlim)
        ax.set_ylim(0, 2.5)
        ax.grid(True)
        ax.set_xlabel(f"Wavelength [{self.waves.unit}]")
        ax.set_ylabel(f"Spectral irradiance [{self.E_w.unit}]")
        ax.set_title("E490 Spectral irradiance ($E_w$)")

    @property
    def ph_per_energy(self):
        return self.waves/(h*c)

    @property
    def E_ph(self):
        return (self.E_w * self.ph_per_energy).to(self.E_ph_unit)

    def plot_E_ph(self, ax=None):
        xlim = [self.wave1.value, self.wave2.value]

        if ax is None:
            _, ax = plt.subplots(figsize=(8, 4))

        ax.plot(self.waves, self.E_ph, lw=self.lw)
        ax.set_xlim(xlim)
        ax.set_ylim(ymin=0, ymax=6e18)
        ax.grid(True)
        ax.set_xlabel(f"Wavelength [{self.waves.unit}]")
        ax.set_ylabel(f"Spectral irradiance [{self.E_ph.unit}]")
        ax.set_title("E490 Spectral irradiance ($E_{ph}$)")

    @property
    def resp_ipol(self):
        ius = InterpolatedUnivariateSpline(self.rsr['wavelength'],
                                           self.rsr['response'],
                                           k=1)
        return ius(self.waves.value)

    @property
    def QE_ipol(self):
        ius = InterpolatedUnivariateSpline(self.QE_rsr['wavelength'],
                                           self.QE_rsr['response'],
                                           k=1)
        return ius(self.waves.value)

    @property
    def L_surf(self):
        term1 = self.E_ph/self.d**2
        term2 = math.cos(self.i.to(u.rad).value) / math.pi
        term3 = self.resp_ipol
        return term1*term2*term3

    @property
    def CR(self):
        term1 = self.L_surf * self.A_t * self.A_p
        term2 = self.T_M1 * self.T_M2 * self.T_s * self.QE_ipol
        return term1*term2/(self.f**2)

    @property
    def signal_rate(self):
        return self.CR.sum()

    def SNR(self, exp=0.01):
        return math.sqrt(self.signal_rate.value * exp)
