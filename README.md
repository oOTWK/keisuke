# Keisuke logic puzzle in Constraint Satisfaction Problem (CSP) model


The keisuke CSP model is in keisuke.py. The keisuke_csp function sets up Keisuke as a CSP.
The random puzzle generators are in keisuke_sample_test.py.

In order to run the code, run the keisuke_sample_run.py file. There are two types of puzzle 
generators, one that will solve a randomly generated Keisuke puzzle and one that will solve 
a more difficult Keisuke puzzle.

The first function is run_puzzle(n) where n is the size of the puzzle. If you want to run
a Keisuke puzzle of size 5, put the line run_puzzle(5) in main. Run the file with

    python keisuke_sample_run.py

You can change the n in order to test puzzles of other sizes.

Similarly, the second function, run_hard_puzzle(n, m) takes a board size (n) and a subsection
size (m). It generates a more difficult puzzle by trying to create a puzzle that maximizes
the amount of subsections of size m in the puzzle. Uncomment the line run_hard_puzzle(5, 2)
and adjust the numbers if needed. Run the file with

    python keisuke_sample_run.py


See [report.pdf](/report.pdf) for more details.
