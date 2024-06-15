# Attacking 'Learning With Errors'

This repository contains the implementation and accompanying report for the COMP3697 Codes and Cryptography module at Durham University. The coursework involved designing and implementing attacks on the 'Learning With Errors' (LWE) problem.

## Overview

### Files

- `crack.py`: Python script implementing the attack algorithms on the LWE problem.
- `paper.pdf`: Report detailing the methodology, results, and analysis of the attacks on the LWE problem.

## Attack Methodology

### Learning Without Errors
The attack involves solving the LWE problem by setting the error distribution χ to 0, effectively reducing the problem to solving a system of linear equations. The LU decomposition method is used to find the secret key \( s \).

### Learning With A Few Errors
For the case where errors are minimal, the attack selects random subsets of the linear equations, hoping to find error-free equations. The most frequently occurring solution among the subsets is considered the secret key.

### Learning With Errors
The attack on the full LWE problem employs the method used for minimal errors but adapted to handle the low error rate typically present in the system of equations.
