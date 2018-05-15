# -*- coding: utf-8 -*-

"""Orbiter module to put telescope on."""

import math

import numpy as np
import spiceypy as spice
from astropy import constants as const
from astropy import units as u

from spicer.kernels import load_generic_kernels

load_generic_kernels()


class Orbiter:
    """Base class for orbiting calculations.

    Parameters
    ----------
    body : str
        SPICE Body name (like earth, mars etc.)

    Attributes
    ----------
    GM : Product of G and M of body
        Rread from SPICE
    GM_unit : astropy.unit
    """
    GM_unit = (u.km) ** 3 / (u.s) ** 2

    def __init__(self, body, alt):
        self.body = body
        self.alt = alt

    @property
    def GM(self):
        return spice.bodvrd(self.body, "GM", 1)[1][0] * self.GM_unit

    @property
    def R_body(self):
        "Using mean radius here!"
        radii = spice.bodvrd(self.body, "RADII", 3)[1]
        return radii.mean()*u.km

    @property
    def R(self):
        return self.R_body + self.alt

    @property
    def v(self):
        "Return orbital velocity."
        return np.sqrt(self.GM / self.R).decompose()

    @property
    def surface_circumference(self):
        "Calculate circumference of circular central body."
        return math.tau * self.R_body

    @property
    def orbitpath(self):
        "Return circumference of circular orbit around central body."
        return math.tau * self.R

    @property
    def T(self):
        "Return orbital period time T."
        return (self.orbitpath / self.v).decompose()

    @property
    def v_surf(self):
        "Return surface footprint speed."
        return (self.surface_circumference / self.T).decompose()

    def ground_travel(self, t):
        "Return footprint travel distance in time `t`."
        return (self.v_surf * t).decompose()

    @property
    def slew_rate(self):
        "Return calculated slew rate in degrees/second for targeting one ground spot."
        gt = self.ground_travel(1 * u.s)
        return np.arctan(gt / self.alt).to(u.degree) / u.s


class MarsOrbiter(Orbiter):
    """Specialized Orbiter class for Mars.

    Parameters
    ----------
    alt : astropy.unit.length[km, m, etc]
        Value for Orbital height above ground (=altitude).
    """

    def __init__(self, alt):
        if not isinstance(alt, u.quantity.Quantity):
            print("Assuming kilometers as unit for input parameter.")
            alt = alt * u.km
        super().__init__('MARS', alt)


class VenusOrbiter(Orbiter):
    """Specialized Orbiter class for Mars.

    Parameters
    ----------
    alt : astropy.unit.length[km, m, etc]
        Value for Orbital height above ground (=altitude).
    """

    def __init__(self, alt):
        if not isinstance(alt, u.quantity.Quantity):
            print("Assuming kilometers as unit for input parameter.")
            alt = alt * u.km
        super().__init__('VENUS', alt)


class EarthOrbiter(Orbiter):
    def __init__(self, alt):
        if not isinstance(alt, u.quantity.Quantity):
            print("Assuming kilometers as unit for input parameter.")
            alt = alt * u.km
        super().__init__('EARTH', alt)
