# SPDX-FileCopyrightText: 2025 EBFM Authors
#
# SPDX-License-Identifier: BSD-3-Clause

from coupling.couplers import Coupler
from coupling.couplers.base import Grid, Dict, CouplingConfig

import logging

logger = logging.getLogger(__name__)


class DummyCoupler(Coupler):
    """
    A dummy coupler implementation that does nothing.
    This can be used when no coupling is required.
    """

    def __init__(self, coupling_config: CouplingConfig):
        super().__init__(coupling_config)

        # DummyCoupler couples to none of the available components
        self._coupled_components = dict()
        logger.debug(f"DummyCoupler created for component '{self.component_name}'.")

    def setup(self, grid: Grid, time: Dict[str, float]):
        """Setup the coupling interface (does nothing for DummyCoupler)

        Performs initialization operations after init and before entering the
        time loop

        @param[in] grid Grid used by EBFM where coupling happens
        @param[in] time dictionary with time parameters, e.g. {'tn': 12, 'dt': 0.125}
        """
        logger.debug("Setup coupling...")
        logger.debug("Do nothing for DummyCoupler.")

    def finalize(self):
        """Finalize the coupling interface (does nothing for DummyCoupler)"""
        logger.debug("Finalizing coupling...")
        logger.debug("No coupling to finalize for DummyCoupler.")
