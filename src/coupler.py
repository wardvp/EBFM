# SPDX-FileCopyrightText: 2025 EBFM Authors
#
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path
from typing import Dict

from elmer.mesh import Mesh as Grid  # for now use an alias

# from ebfm.geometry import Grid  # TODO: consider introducing a new data structure native to EBFM?
from ebfm.config import EBFMCouplingConfig

import logging

logger = logging.getLogger(__name__)


class Coupler:
    component_name: str  # name of this component in the coupler configuration

    couple_to_elmer_ice: bool  # whether to couple with Elmer/Ice
    couple_to_icon_atmo: bool  # whether to couple with ICON atmosphere

    @property
    def has_coupling(self) -> bool:
        return_value = self.couple_to_elmer_ice or self.couple_to_icon_atmo
        logger.debug(f"Component {self.component_name} has_coupling={return_value}")
        return return_value

    def __init__(self, component_name: str, coupler_config: Path, component_coupling_config: EBFMCouplingConfig):
        """
        Create Coupler object

        @param[in] component_name name of this component in the coupler configuration
        @param[in] coupler_config path to the coupler configuration file
        """
        raise NotImplementedError("Coupler is an abstract base class and cannot be instantiated directly.")

    def setup(self, grid: Grid, time: Dict[str, float]):
        """
        Setup the coupling interface

        Performs initialization operations after init and before entering the
        time loop

        @param[in] grid Grid used by EBFM where coupling happens
        @param[in] time dictionary with time parameters, e.g. {'tn': 12, 'dt': 0.125}
        """
        raise NotImplementedError("setup method must be implemented in subclasses.")

    def add_grid(self, grid_name: str, grid: Grid):
        """
        Add grid to the Coupler interface
        """
        raise NotImplementedError("add_grid method must be implemented in subclasses.")

    def add_couples(self, time: Dict[str, float]):
        """
        Add coupling definitions to the Coupler interface
        """
        raise NotImplementedError("add_couples method must be implemented in subclasses.")

    def finalize(self):
        """
        Finalize the coupling interface
        """
        raise NotImplementedError("finalize method must be implemented in subclasses.")
