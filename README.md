# RegEx2NFA
These programs will help you convert Regular Expressions to their equivalent NFAs and simulate the process of reading an input String by an NFA.  

## build.py  

Given a RegEx of a specific format described below,  
build.py builds an equivalent NFA and prints it  
in a specific format.  

RegEx has the following form:  
	(1) Union is marked by the symbol "|"  
	(2) Concatenation is defined by adjacency of RegExs  
	(3) Star is marked by "*"  
  
Also:  
	(4) Alphabet of the RegEx consists only of small Latin letters  
  (5) Except the symbols above, curved brackets can be used  
  (6) Emtpy string is marked by "()"  
Example:  

  (ab*c(0|1)*)*  

NFA is represented this way:  
  (Number of States) (Number of Accept States) (Number of Transitions)  
  Accept states seperated by Spaces  
  (Number of Transitions from State 0) (Symbol State) (Symbol State) ...  
  (Number of Transitions from State 1) (Symbol State) (Symbol State) ...  
  .  
  .  
  .  

For example, (ab*c(0|1)*)* would could have the ouput:  

  3 2 6  
  0 2  
  1 a 1  
  2 b 1 c 2  
  3 0 2 1 2 a 1  

## run.py  

Given an NFA in the format described above  
and an input string, this program simulates  
the reading of the string by the NFA.  
For each symbol read, if by the symbol  
NFA goes into an accept state "Y" is printed,  
if not - "N", accordingly.  

For example, for input:  

  aababacab  
  2 2 3  
  0 1  
  3 a 0 b 0 c 1  
  0  
  
the ouput is:  

  YYYYYYYNN  

Hope, this will be helpful!  
  
