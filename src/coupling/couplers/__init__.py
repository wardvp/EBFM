# SPDX-FileCopyrightText: 2025 EBFM Authors
#
# SPDX-License-Identifier: BSD-3-Clause

from coupling.couplers.base import Coupler  # noqa: F401
from coupling.couplers.dummyCoupler import DummyCoupler  # noqa: F401

coupling_supported: bool
coupling_supported_import_error: Exception = None

try:
    from coupling.couplers.yacCoupler import YACCoupler  # noqa: F401
    from coupling.couplers.oasisCoupler import OASISCoupler  # noqa: F401

    coupling_supported = True
except ImportError as e:
    coupling_supported = False
    coupling_supported_import_error = e
