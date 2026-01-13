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


class IconAtmo(Component):
    """
    Component class for ICON atmosphere model coupling.
    """

    name = "icon_atmo"

    def __init__(self, coupler: "Coupler"):
        super().__init__(coupler)

    def _yac_field_definitions(self, time: Dict[str, float]) -> Set[Field]:
        """
        Get field definitions for EBFM coupling to IconAtmo using YAC coupler.
        """

        timestep_value = days_to_iso(time["dt"])
        timestep = Timestep(value=timestep_value, format=yac.TimeUnit.ISO_FORMAT)

        return {
            # Field(
            #     name="albedo",
            #     coupled_component=self,
            #     timestep=timestep,
            #     metadata="Albedo of the ice surface (in ???)",
            #     exchange_type=yac.ExchangeType.SOURCE,
            # ),
            Field(
                name="pr",
                coupled_component=self,
                timestep=timestep,
                metadata="Precipitation rate (in kg m-2 s-1)",
                exchange_type=yac.ExchangeType.TARGET,
            ),
            Field(
                name="pr_snow",
                coupled_component=self,
                timestep=timestep,
                metadata="Precipitation rate of snow (in kg m-2 s-1)",
                exchange_type=yac.ExchangeType.TARGET,
            ),
            Field(
                name="rsds",
                coupled_component=self,
                timestep=timestep,
                metadata="Downward shortwave radiation flux (in W m-2)",
                exchange_type=yac.ExchangeType.TARGET,
            ),
            Field(
                name="rlds",
                coupled_component=self,
                timestep=timestep,
                metadata="Downward longwave radiation flux (in W m-2)",
                exchange_type=yac.ExchangeType.TARGET,
            ),
            Field(
                name="sfcwind",
                coupled_component=self,
                timestep=timestep,
                metadata="Wind speed at surface (in m s-1)",
                exchange_type=yac.ExchangeType.TARGET,
            ),
            Field(
                name="clt",
                coupled_component=self,
                timestep=timestep,
                metadata="Cloud cover (in fraction)",
                exchange_type=yac.ExchangeType.TARGET,
            ),
            Field(
                name="tas",
                coupled_component=self,
                timestep=timestep,
                metadata="Temperature at surface (in K)",
                exchange_type=yac.ExchangeType.TARGET,
            ),
            # Field(
            #     name="huss",
            #     component=self,
            #     timestep=timestep,
            #     metadata="Specific humidity at surface (in kg kg-1)"
            #     exchange_type=yac.ExchangeType.TARGET,
            # ),
            # Field(
            #     name="sfcPressure",
            #     component=self,
            #     timestep=timestep,
            #     metadata="Surface pressure (in Pa)"
            #     exchange_type=yac.ExchangeType.TARGET,
            # ),
        }

    def get_field_definitions(self, time: Dict[str, float]) -> Set[Field]:
        """
        Get field definitions for EBFM coupling.

        @param[in] time dictionary with time parameters, e.g. {'tn': 12, 'dt': 0.125}
        """

        if self._uses_coupler("YACCoupler"):
            return self._yac_field_definitions(time)
        else:
            raise NotImplementedError(
                f"The component {self.name} was configured with the unsupported coupler {type(self._coupler)}."
                "Note: ElmerIce component only supports YACCoupler at the moment. "
            )
