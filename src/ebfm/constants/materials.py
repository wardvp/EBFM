# SPDX-FileCopyrightText: 2025 EBFM Authors
#
# SPDX-License-Identifier: BSD-3-Clause

from typing import Final
from dataclasses import dataclass


@dataclass
class Material:
    ALBEDO: Final[float]
    DENSITY: Final[float]


@dataclass
class Ice(Material):
    ALBEDO: Final[float] = 0.39
    DENSITY: Final[float] = 900.0


@dataclass
class FreshSnow(Material):
    ALBEDO: Final[float] = 0.83
    DENSITY: Final[float] = 350.0


@dataclass
class Firn(Material):
    ALBEDO: Final[float] = 0.52
    DENSITY: Final[float] = 500.0


@dataclass
class Water(Material):
    DENSITY: Final[float] = 1000.0
