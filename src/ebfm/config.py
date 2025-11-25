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

    component_name: str  # Name of this component
    couple_to_icon_atmo: bool  # Whether to couple this component to ICON atmosphere
    couple_to_elmer_ice: bool  # Whether to couple this component to Elmer/Ice

    def defines_coupling(self) -> bool:
        """Check if any coupling is defined in this configuration.

        @returns True if coupling to any component is enabled, False otherwise
        """
        return self.couple_to_icon_atmo or self.couple_to_elmer_ice
