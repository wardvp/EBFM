# SPDX-FileCopyrightText: 2025 EBFM Authors
#
# SPDX-License-Identifier: BSD-3-Clause

from typing import Dict, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from coupling.couplers.base import Coupler

from coupling.components.base import Component

# from coupling import Field  # TODO: rather use generic Field from coupling
# TODO: Try to remove YAC specific imports from here
from coupling.couplers.yacField import Field
from coupling.couplers.yacField import Timestep, days_to_iso
import yac


class ElmerIce(Component):
    """
    Component class for Elmer/Ice model coupling.
    """

    name = "elmer_ice"

    def __init__(self, coupler: "Coupler"):
        super().__init__(coupler)

    def get_field_definitions(self, time: Dict[str, float]) -> Set[Field]:
        """
        Get field definitions for EBFM coupling.

        @param[in] time dictionary with time parameters, e.g. {'tn': 12, 'dt': 0.125}
        """

        timestep_value = days_to_iso(time["dt"])
        timestep = Timestep(value=timestep_value, format=yac.TimeUnit.ISO_FORMAT)

        return {
            Field(
                name="T_ice",
                coupled_component=self,
                timestep=timestep,
                metadata="Near surface temperature at Ice surface (in K)",
                exchange_type=yac.ExchangeType.SOURCE,
            ),
            Field(
                name="smb",
                coupled_component=self,
                timestep=timestep,
                metadata="??? (in ???)",
                exchange_type=yac.ExchangeType.SOURCE,
            ),
            Field(
                name="runoff",
                coupled_component=self,
                timestep=timestep,
                metadata="Runoff (in ???)",
                exchange_type=yac.ExchangeType.SOURCE,
            ),
            Field(
                name="h",
                coupled_component=self,
                timestep=timestep,
                metadata="Surface height (in m)",
                exchange_type=yac.ExchangeType.TARGET,
            ),
            # Field(
            #     name="dhdx",
            #     coupled_component=self,
            #     timestep=timestep,
            #     metadata="Surface slope in x direction",
            #     exchange_type=yac.ExchangeType.TARGET,
            # ),
            # Field(
            #     name="dhdy",
            #     coupled_component=self,
            #     timestep=timestep,
            #     metadata="Surface slope in y direction",
            #     exchange_type=yac.ExchangeType.TARGET,
            # ),
        }
