FC = mpif90
SOURCES = $(wildcard src/*.f90)
OBJECTS = $(SOURCES:.f90=.o)
EXECUTABLE = stats

$(EXECUTABLE): $(OBJECTS)
	$(FC) -o $(EXECUTABLE) $(OBJECTS) -J mod/

%.o: %.f90
	gfortran -c $< -o $@


