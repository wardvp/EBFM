# SPDX-FileCopyrightText: 2026 EBFM Authors
#
# SPDX-License-Identifier: BSD-3-Clause

from abc import ABC, abstractmethod
from typing import Set, Dict, TYPE_CHECKING


if TYPE_CHECKING:
    from coupling.couplers.yacField import Field


class Component(ABC):
    """
    Abstract base class for coupling components.
    Each component owns its fields as an instance attribute.
    """

    name: str  # name of this component

    def __init__(self):
        pass

    @abstractmethod
    def get_field_definitions(self, time: Dict[str, float]) -> Set["Field"]:
        """
        Get field definitions for this component.
        Subclasses must implement this method.

        @param[in] time dictionary with time parameters
        @returns Set of Field objects for this component
        """
        pass
