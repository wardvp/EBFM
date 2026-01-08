# SPDX-FileCopyrightText: 2025 EBFM Authors
#
# SPDX-License-Identifier: BSD-3-Clause

from typing import Dict, Set

# from coupling import Field  # TODO: rather use generic Field from coupling
from coupling.components import Component

# TODO: Try to remove YAC specific imports from here
from coupling.couplers.yacField import Field
from coupling.couplers.yacField import Timestep, days_to_iso
import yac


def get_field_definitions(time: Dict[str, float]) -> Set[Field]:
    """
    Get field definitions for EBFM coupling.

    @param[in] time dictionary with time parameters, e.g. {'tn': 12, 'dt': 0.125}
    """

    timestep_value = days_to_iso(time["dt"])
    timestep = Timestep(value=timestep_value, format=yac.TimeUnit.ISO_FORMAT)

    return {
        Field(
            name="T_ice",
            coupled_component=Component.elmer_ice,
            timestep=timestep,
            metadata="Near surface temperature at Ice surface (in K)",
            exchange_type=yac.ExchangeType.SOURCE,
        ),
        Field(
            name="smb",
            coupled_component=Component.elmer_ice,
            timestep=timestep,
            metadata="??? (in ???)",
            exchange_type=yac.ExchangeType.SOURCE,
        ),
        Field(
            name="runoff",
            coupled_component=Component.elmer_ice,
            timestep=timestep,
            metadata="Runoff (in ???)",
            exchange_type=yac.ExchangeType.SOURCE,
        ),
        Field(
            name="h",
            coupled_component=Component.elmer_ice,
            timestep=timestep,
            metadata="Surface height (in m)",
            exchange_type=yac.ExchangeType.TARGET,
        ),
        # Field(
        #     name="dhdx",
        #     component=Component.elmer_ice,
        #     timestep=timestep,
        #     metadata="Surface slope in x direction",
        #     exchange_type=yac.ExchangeType.TARGET,
        # ),
        # Field(
        #     name="dhdy",
        #     component=Component.elmer_ice,
        #     timestep=timestep,
        #     metadata="Surface slope in y direction",
        #     exchange_type=yac.ExchangeType.TARGET,
        # ),
    }
