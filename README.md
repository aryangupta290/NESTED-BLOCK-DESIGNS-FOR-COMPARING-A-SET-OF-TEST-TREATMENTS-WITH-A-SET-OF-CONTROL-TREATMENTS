# BTP-2

This repository contains the codes for Nested Block Designs for comparing the set of test treatments with a set of control treatments. Namely, six methods have been described. The user needs to input nested balanced incomplete block (NBIB), balanced incomplete block (BIB), or balanced bipartite block (BBPB) design as input (depending on the method) in a csv file format and number of control treatments. If a valid construction will be possible, the code will output the nested balanced bipartite block (NBBPB) design along with its A-efficiency.

- User must indicate control treatments as upper treatments, that is if there are 3 test treatments and 2 control treatments, then the user must indicate the control treatments as 4 and 5 in the input design.

# SETUP

```bash
$ pip install -r requirements.txt
```

This will install all required packages for the code to run.

# Input

For all methods, the user should provide the input design in a csv file format.
More specifically,

- NBIB design - Methods 1,2,4
  ex: NBIB design with parameters (v=7, b1=7, b2=14, r=6, k1=6, k2=3, λ1=5, λ2=2)

  ![Alt text](/nbib_test.png?raw=true "Optional Title")

- BIB design - Methods 3, 5, 6
  ex: BIB design with parameters (v=7, b=7, r=3, k=3, λ=1)

  ![Alt text](/bib_test.png?raw=true "Optional Title")

- BBPB design - Method 4
  ex: BBPB design with parameters (v1=4, v2=2, b=4, r1=3, r2=4, k=5, λ11=2, λ12=3, λ22=4)

  ![Alt text](/bbpb_test.png?raw=true "Optional Title")

  Apart from the input design, the following parameters are required for the code to run:
  - Method 1: 
    * Sub-block size of NBIB design. 
    * Number of control treatments.
  - Method 2: 
    * Sub-block size of NBIB design.
    * Alpha value  
    * Number of control treatments.
  - Method 3:
    * Number of control treatments.
  - Method 4:
    * Sub-block size of NBIB design.
  - Method 5:
    * Number of control treatments.
  - Method 6:
    * Number of control treatments.

# Running Code

To run the code, user should run the following command in the terminal:

```bash
$ python3 methodx.py
```
    
    where x is the method number.

Now, they will be prompted to enter the input file name and the parameters required for the method.
ex: For method1, the user will be prompted to enter the sub-block size and number of control treatments.

  ![Alt text](/construction_code_running.png?raw=true "Optional Title")

  # Output 

If the design is valid and the construction is possible, the code will output the nested balanced bipartite block (NBBPB) design along with its parameters and block, sub-block efficiency.

  ![Alt text](/method1_output.png?raw=true "Optional Title")

If the design is invalid, the code will output the reason for the invalidity.