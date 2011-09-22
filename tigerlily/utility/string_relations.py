# string_relations.py - Calculations for string relatedness
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

def hamming_distance(s1,s2):
    """Return the Hamming edit distance between s1 and s2.

    The Hamming edit distance is defined as the number of individual alterations
    performed on characters in one string in order to turn it in to another
    string of the same length.

    If s1 and s2 are not the same length, ValueError will be raised.

    >>> hamming_distance('party','party')
    0
    >>> hamming_distance('zebra','cobra')
    2
    >>> hamming_distance('one','three')
    Traceback (most recent call last):
        ...
    ValueError: Cannot compute Hamming distance of strings of unequal length

    With apologies to the fine editors of wikipedia.com for kernel of this
    code.

    """
    if len(s1) != len(s2):
        raise ValueError('Cannot compute Hamming distance of strings of '
                         'unequal length')
    return sum(ch1 != ch2 for ch1,ch2 in zip(s1,s2))
        

def greatest_common_prefix(s1,s2):
    """Return the length of the longest common prefix between s1 and s2.

    >>> greatest_common_prefix('banana','bandit')
    3
    >>> greatest_common_prefix('apple','sour apple')
    0
    >>> greatest_common_prefix('tree','tree')
    4

    """
    ls1 = len(s1)
    ls2 = len(s2)
    smaller_length = ls1 if ls1 < ls2 else ls2


    for i in range(smaller_length):
        if s1[i] != s2[i]:
            return i

    return smaller_length

def levenshtein_distance(s1,s2):
    """Return the Levenshtein edit distance (integer) between s1 and s2.

    The Levenshtein is defined as the minimum number of substitutions,
    additions, and deletions needed to transform s1 in to s2.

    >>> levenshtein_distance('kitten','sitten')
    1
    >>> levenshtein_distance('sitten','sittin')
    1
    >>> levenshtein_distance('sittin','sitting')
    1
    >>> levenshtein_distance('Alabama','Hell') # Surprisingly, not 0!
    7

    Thanks to hetland.org for this code:
    hetland.org/coding/python/levenshtein.py
    (no copyright information was found)
    """
    
    n, m = len(s1), len(s2)
    if n > m:
        # make sure n <= m, to use O(min(n,m)) space
        s1,s2 = s2,s1
        n,m = m,n
    
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if s1[j-1] != s2[i-1]:
                change = change + 1
            current[j] = min(add,delete,change)

    return current[n]

    
    
