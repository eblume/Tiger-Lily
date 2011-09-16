TEST_ASSEMBLIES = test1.tar.gz


all: $(TEST_ASSEMBLIES)

clean:
	-rm $(TEST_ASSEMBLIES)

%.tar.gz : %.txt
	echo Creating $@
	./txt2assembly < $< > $@
