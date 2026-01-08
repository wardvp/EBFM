# SPDX-FileCopyrightText: 2025 EBFM Authors
#
# SPDX-License-Identifier: BSD-3-Clause

from enum import Enum, auto


class Component(Enum):
    """
    Other components which this model can couple to
    """

    elmer_ice = auto()
    icon_atmo = auto()
