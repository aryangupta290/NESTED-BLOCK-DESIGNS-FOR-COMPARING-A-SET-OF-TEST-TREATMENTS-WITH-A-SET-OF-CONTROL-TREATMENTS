# BTP-2
This repository contains the codes for Nested Block Designs for comparing the set of test treatments with a set of control treatments. Namely, six methods have been described. The user needs to input NBIB, BIB, or BBPD design as input (depending on the method) in a csv file format and number of control treatment. If a valid construction will be possible, the code will output the NBBPB design along with its accuracy. 

* User must indicate control treatments as upper treatments, that is if there are 3 test treatments and 2 control treatments, then the user must indicate the control treatments as 4 and 5 in the input design. 

# SETUP

```bash
$ pip install -r requirements.txt
```
This will install all required packages for the code to run.

# USAGE

```bash
$ python3 methodx.py
```
where x is the method number.
