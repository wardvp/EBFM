# SPDX-FileCopyrightText: 2025 EBFM Authors
#
# SPDX-License-Identifier: BSD-3-Clause
"""Configuration for EBFM coupling options.

This file exposes a `EBFMCouplingConfig` dataclass.
"""

from dataclasses import dataclass


@dataclass
class EBFMCouplingConfig:
    """Coupling configuration.

    Keep this class intentionally small; add fields later as needed.
    """

    couple_with_icon_atmo: bool
    couple_with_elmer_ice: bool
