#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pytelescope` package."""

import pytest

from pytelescope import orbiter


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/michaelaye/cookiecutter-pypackage-conda')


@pytest.fixture()
def mars_orbiter():
    orb = orbiter.MarsOrbiter(350)
    return orb


def test_mars_orbiter_orbital_period(mars_orbiter):
    assert mars_orbiter.T.to(u.hour).value == pytest.approx(1.933, abs=1e-2)


def test_mars_orbiter_slew_rate(mars_orbiter):
    assert mars_orbiter.slew_rate.value == pytest.approx(0.5019, abs=1e-2)


def test_mars_orbiter_altitude(mars_orbiter):
    assert mars_orbiter.alt.value == pytest.approx(350)


def test_mars_orbiter_orbital_velocity(mars_orbiter):
    assert mars_orbiter.v.value == pytest.approx(3384.208966304714)


def test_mars_orbiter_ground_track_speed(mars_orbiter):
    assert mars_orbiter.v_surf.value == pytest.approx(3067.464831608527)
