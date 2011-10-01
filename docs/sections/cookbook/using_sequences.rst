Using Sequences
===============

In bioinformatics, it is common to want to work on sequences of characters that
represent either neucleotides or amino acids in order to represent genetic and
proteomic units. The Tiger Lily package ``tigerlily.sequences`` provides
support for these operations.

It's important to note that in Tiger Lily, all sequences descend from the common
base class ``tigerlily.sequences.PolymerSequence``, but you will generally never
use that class directly. Also, some sequences are purely scientific abstractions
(like ``tigerlily.sequences.NucleicSequence``) while others are tightly related
to a representation (like ``tigerlily.sequences.FASTASequence``). This second
class of sequences (that map to a format) all inherit from a the base class
``tigerlily.sequences.FormattedSequence``, which are themselves just
``PolymerSequence`` objects that support a ``format()`` method and a ``write``
method.

Background aside, let's dive in to some examples of using Tiger Lily sequences.

Creating Sequences
------------------

For this example, lets pretend we have a *flat* text file of sequences. In other
words, we have a text file which has one sequence per line, with nothing else
at all in the file (except possibly empty lines). In Tiger Lily terms, this is
called a Raw File, and it is supported with the classes and functions in
``tigerlily.sequences.raw``, namely ``Raw`` and ``parseRaw``, a class and a 
function respectively.

First, lets create a 'fake' file using the multi-line string syntax of Python.

>>> raw_reads = """CATGGCTTTGTGACTGAGTCCAGTAC
... ACTTGGATTATTCGATCGTAGCTATTATCGAC
... CACATTTAGGGAGGAGGAGACGATGCTAGCTAGCTGATTGTTATTATTATTATAGCGGGGCGCATGACT
... AAGAGAAAAAAAAAAACGATACGACTACG
... ACGGCTAGCGTACGCTAGCCAAAACCACACATTTCATCATCA
... """

Keep in mind that as far as the RAW sequence format is concerned, sequences
can be absolutely any string of characters except for the newline character -
we are using only A, T, G, and C so that we can convert these reads in to
``NucleicSequence`` objects later.

Next, let's read these sequences in.

>>> from tigerlily.sequences import parseRaw
>>> seqs = [s for s in parseRaw(data=raw_reads)]
>>> len(seqs)
5

We can access the ``sequence`` attribute of each ``RawSequence`` object in the
list thusly:

>>> seqs[0].sequence
'CATGGCTTTGTGACTGAGTCCAGTAC'

Additionally, the ``Raw`` class pre-loaded each sequence with an ``identifier``
attribute by using the line number of each sequence.

>>> seqs[2].identifier
'RawSeq_Line3'
>>> seqs[3].identifier
'RawSeq_Line4'


Converting Sequences
--------------------

Now that we have our sequences as a bunch of ``RawSequence`` objects, we might
wonder what we can do with that beyond having a somewhat indirect method of
accessing each individual sequence as a string? Well, let's say that each
sequence is the **coding sequence** of a protein subunit. We then might want
to translate each sequence using the genetic code. With Tiger Lily, it's easy!

First, convert each ``RawSequence`` object to a ``NucleicSequence`` object:

>>> nucleic_seqs = [s.convert(NucleicSequence) for s in seqs]

*Note: if any of the sequences didn't have just A, T, G, or C in it, that would
have raised an error.*

Manipulating ``NucleicSequence`` objects
----------------------------------------

Now, let's use the ``translate`` method of ``NucleicSequence`` objects to get
the first coding frame translation of the first nucleic sequence:

>>> subunit = nucleic_seqs[0].translate()
>>> subunit.sequence
'HGVTESS'
>>> type(subunit)
<class 'tigerlily.sequences.genomic.AminoSequence'>

Translation
~~~~~~~~~~~

As you can see, the ``translate`` method changed our ``NucleicSequence`` object
in to an ``AminoSequence`` object. In fact we can also go in the reverse
direction, although due to the highly redundant nature of the genetic code,
reverse translation produces many possible translations of amino acid sequences
in to their corresponding nucleic sequences.

>>> len([t for t in subunit.translations()])
18432

We can also specify different *reading frames* of the nucleic sequence to get
different translations:

>>> subunit = nucleic_seqs[0].translate(reading_frame=2)
>>> subunit.sequence
'MAL*LSPV'

We can even tell the translation function to honor control codes (START and
STOP codons):

>>> subunit = nucleic_seqs[0].translate(reading_frame=2,use_control_codes=True)
>>> subunit.sequence
'AL'

Reverse and Complement
~~~~~~~~~~~~~~~~~~~~~~

Another common task with ``NucleicSequence`` objects is to convert the sequence
in to an equivalent sequence on the opposing strand and/or in the opposite
direction. This is also simple to do in Tiger Lily:

>>> seq3 = nucleic_seqs[3]
>>> seq3.sequence
'AAGAGAAAAAAAAAAACGATACGACTACG'
>>> seq3.reverse().sequence
'GCATCAGCATAGCAAAAAAAAAAAGAGAA'
>>> seq3.complement().sequence
'TTCTCTTTTTTTTTTTGCTATGCTGATGC'
>>> seq3.reverse_complement().sequence
'CGTAGTCGTATCGTTTTTTTTTTTCTCTT'

*Note that each command is generating an entirely new ``NucleicSequence``
object.*

Writing in Another Format
-------------------------

Let's say we want to take the original raw sequences we created earlier (in
``seqs``) and write them in the FASTA file format. But that's not all - we first
want to find each of their reverse complements. You guessed it - all very
simple!

First a little bit of setup: 

>>> from tigerlily.sequences import writeFASTA
>>> from io import StringIO
>>> output = StringIO()

And now the business end of the operation:

>>> conv_seqs=[s.convert(NucleicSequence).reverse_complement() for s in seqs]
>>> writeFASTA(output,*conv_seqs)

If you examine the output, you should see:

>>> print(output.getvalue())
>RawSeq_Line1
GTACTGGACTCAGTCACAAAGCCATG
>RawSeq_Line2
GTCGATAATAGCTACGATCGAATAATCCAAGT
>RawSeq_Line3
AGTCATGCGCCCCGCTATAATAATAATAACAATCAGCTAGCTAGCATCGTCTCCTCCTCCCTAAATGTG
>RawSeq_Line4
CGTAGTCGTATCGTTTTTTTTTTTCTCTT
>RawSeq_Line5
TGATGATGAAATGTGTGGTTTTGGCTAGCGTACGCTAGCCGT

