Christian Miljkovic  Operating System's Demand Paging Lab


COMPILE
to compile, navigate to the directory that holds all java files and random-ints.txt and run the following command
javac *.java


RUN
to run, run the following command with 5 command line arguments: machine size, page size, process size, job mix, number of references, and replacement algorithm (in that order).
java DemandPaging MACHINE_SIZE PAGE_SIZE PROCESS_SIZE JOB_MIX NUMBER_OF_REFERENCES REPLACEMENT_ALGORITHM


EXAMPLE
javac *.java
java DemandPaging 10 10 20 1 10 lru 0
