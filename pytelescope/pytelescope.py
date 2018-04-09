# -*- coding: utf-8 -*-

"""Main module."""

from astropy import constants as const
import numpy as np
import math
from planetpy.constants import mars, earth
from astropy import units as u


class Orbiter:
    """Base class for orbiting calculations.

    Parameters
    ----------
    M : astropy.units.[mass]
        Mass of central body
    R : astropy.units.[length]
        Radius of circular orbit around body with mass M

    Attributes
    ----------
    G : astropy.constansts.G
        Gravitational constant
    """
    G = const.G

    def __init__(self, M, R):
        self.M = M
        self.R = R
        self.alt = R - self.R_body

    @property
    def v(self):
        "Return orbital velocity."
        return np.sqrt(self.G * self.M / self.R).decompose()

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
        return self.v_surf * t

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
        Value for Orbital altitude above ground.

    Attributes
    ----------
    M : astropy.units.mass
        Mass of Mars
    R_body : astropy.units.length
        Radius of Mars
    """
    M = mars.mass * 1e24 * u.kg
    R_body = mars.diameter / 2 * u.km

    def __init__(self, alt):
        super().__init__(self.M, self.R_body + alt)


class EarthOrbiter(Orbiter):

    M = earth.mass * 1e24 * u.kg
    R_body = earth.diameter / 2 * u.km

    def __init__(self, d):
        super().__init__(self.M, self.R_body + d)
