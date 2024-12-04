<h3>py3 is used in this tutorial. But python might work as well. Replace py as python if so.</h3>
<a href='https://www.keysight.com/zz/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html'>install agilent IO libraries suite and 82357 library suite</a>

1. install python packages 
```
py -m pip install -r requirements.txt
```
If python is used, then use the following command:
```
pip install -r requirements.txt
```
2 (optinal). set the Vgs (33120A) only
```
py test8200.py
```
or
```
python test8200.py
```
3. choose the function u want before run (fixed Vgs or fixed Vds)
```
py main.py
```
or 
```
python main.py
```