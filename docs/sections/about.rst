About Tiger Lily
===============

Tiger Lily is a package  written  for
`Python 3 <www.python.org>`_ which provides tools
commonly needed in bioinformatics. It does this by providing an easy-to-use
package called ``tigerlily``, which has modules written with the intention of
being high performance and specific in purpose while being pluggable to fit a
wide variety of purposes.

Priorities
----------

Tiger Lily aims to be the go-to tool for any bioinformatics application. This
means Tiger Lily should:

1. Be well documented.
2. Be well tested. 
3. Have *Batteries Included*, and provide tools for every common task.
4. Be extensible, allowing other packages to modify, extend, and enhance Tiger
   Lily with ease and grace.
5. Be pluggable, allowing applications to pick and choose what tools it will
   need and use them together in whatever order it pleases.
6. Be *fast*, and meet the often staggering needs of high-throughput sequencing.
7. Be *scalable* through parallelism and design, allowing the user to get the
   most out of her hardware.

Tiger Lily and Bioinformatics
-----------------------------

As of this early writing, Tiger Lily is still in its infancy. As we move closer
to the goals listed above we will expand the breadth and depth of Tiger Lily.

For now, Tiger Lily is mostly applicable towards aligning short reads against
a reference genome, as well as providing a flexible tool for converting between
common formats. While most of the early developmental focus will be expended on
short read sequence alignment, this is by no means the full scope of Tiger Lily.
(It just happens to be the domain of the main author's experience.)

Tiger Lily and Python
---------------------

Tiger Lily was specifically built for Python 3 with an eye towards current and
emerging standards. As much as possibly, Tiger Lily will incorporate existing
features in the standard py3k library.

What this means to you, the user, is that you should feel comfortable in knowing
that Tiger Lily (if we are doing our job) is staying current and relevant.

What about Biopython?
_________________________

As the reader may or may not be aware, there is already a similar project to 
Tiger Lily called `Biopython <http://biopython.org/wiki/Main_Page>`_.
Biopython supports a very wide range of sequence formats including coverage of
nearly all of the most commonly used web resources (NCBI, UCSC Genome Browser,
SwissProt, UniProt, Sanger Institute, etc.). It also has the benefit of having
a very wide international support base and is well respected.

We believe that Tiger Lily still has a place beside Biopython for the following reasons:

1. Tiger Lily is targeting Python 3, which Biopython does not currently support.
2. Tiger Lily is aimed at high speed computing for short read sequencing
   applications where biopython is aimed more at more traditional forms of
   bioinformatics, sometimes at the cost of performance.
3. Tiger Lily has a different 'flavor' that the authors find more palatable.

That being said, long-term it is very likely that the fruits of the Tiger Lily
project will end up being submitted to Biopython as a feature enhancement for
their consideration. Still, Tiger Lily will be developed as though
the goal were to eventually have Tiger Lily be the go-to resource for python
bioinformatics.

Why 'Tiger Lily'?
-----------------

The name wasn't chosen for any particular reason - a name was needed and the
original author felt that tiger lillies might make for a good logo some day.

