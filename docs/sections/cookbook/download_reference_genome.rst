Downloading a Reference Genome
==============================

Reference genome assemblies are carefully compiled consensus sequences for
an *ideal* human genome. Often times, sequenced genetic material in the lab
comes fragmented and without any notion of where in the specimen's genome it
came from. Using a reference genome, you can hope to get a good idea of where
the sequence came from by searching the reference for similar sequences.

With **Tiger Lily**, downloading and using a reference genome is very simple.
To do this, we use the ``tigerlily.grc`` package to download reference genomes
provided by the `UCSC Genome Browser <http://genome.ucsc.edu/>`_.

First, let's download a genome and store it so that we can use it later.

    **Remember: while Tiger Lily makes it easy to download a reference genome,
    these files are often very large and are served at the public expense
    from the UCSC Genome Browser web page. Please do not download reference
    genomes too often, and please *do* store genomes that you have downloaded.**

>>> import tigerlily.grc as grc
>>> ref_genome = grc.GRCGenome.download('hg19',store=True,silent=False)
Downloading http://.../chromFa.tar.gz
05:26 | 05:26 : ============================== | 05:26 (926504K / 926501K)

The actual message printed may vary, but this should be close to what you see.
After the download is complete, the prompt may 'hang' for up to a few minutes
as the sequences are loaded from the downloaded archive.

Because we set ``store=True``, a file called ``hg19.assembly`` will have been
created.

>>> import os
>>> os.path.isfile('hg19.assembly')
True

Also, note that we can in the future load the file you just downloaded without
hitting the poor UCSC Genome Browser's web server. **(You *do not* need to run
this command now for this recipe - ``ref_genome`` is already correctly set after
downloading the genome from the UCSC Genome Browser.)**

>>> ref_genome = grc.GRCGenome.load('hg19.assembly')

Finally, we can extract the sequences into a ``MixedSequenceGroup`` object.

>>> sequences = ref_genome.sequences()

This object can then be manipulated in the way you would use any sequence group
object.



