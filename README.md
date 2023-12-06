# FOLSAT
A tool for checking satisfiability of FOL formulas that uses no external libraries.

## Instructions
The input has to be very specific. The first line of input file has to be SAT, PARSE or both in order to be understood by the tool. 
The tool checks the satisfiability of a formula by creating a first order tableau.
#### Important: The tableau stops creating a new constant after 10 variables and outputs a message stating satisfiability is undetermined.
#### Hence if you have more than 10 delta expansions, tool cannot determine whether formula is satisfiable or not.
