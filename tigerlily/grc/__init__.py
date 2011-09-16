# __init__.py - Package meta file for tigerlily.grc
# Authors:
#   * Erich Blume <blume.erich@gmail.com>
#
# Copyright 2011 Erich Blume <blume.erich@gmail.com>
#
#   This file is part of Tiger Lily.
#
#   Tiger Lily is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Tiger Lily is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Tiger Lily.  If not, see <http://www.gnu.org/licenses/>.
#

"""tigerlily.grc - functions and extensions for common GRC-related tasks.

The members of this package generally interact with online or downloaded
resources from the members of the GRC (Genome Reference Consortium) and
other online resource entities such as NCBI, Sanger Institute, and the
UCSC Genome Browser.
"""

from tigerlily.grc.genome import (GRCGenome, ReferenceGenome, 
    SUPPORTED_ASSEMBLIES, DEFAULT_ASSEMBLY)

