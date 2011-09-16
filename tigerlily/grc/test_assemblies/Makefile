TEST_ASSEMBLIES = test1.tar.gz


all: $(TEST_ASSEMBLIES)

%.tar.gz : %.txt
    ./txt2assembly < $< > $@
