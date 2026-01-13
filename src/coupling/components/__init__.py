# SPDX-FileCopyrightText: 2025 EBFM Authors
#
# SPDX-License-Identifier: BSD-3-Clause

from coupling.components.base import Component  # noqa: F401
from coupling.helpers import check_coupling_support

# TODO: should not be necessary if ElmerIce etc. use a generic Field instead of (YAC)Field
coupling_supported: bool
try:
    check_coupling_support()
    coupling_supported = True
except ImportError:
    coupling_supported = False

if coupling_supported:
    from coupling.components.icon_atmo import IconAtmo  # noqa: F401
    from coupling.components.elmer_ice import ElmerIce  # noqa: F401
