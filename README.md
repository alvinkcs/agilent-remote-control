<h3>py is used in this tutorial. But python works as well. Replace py with python if so.</h3>
<a href='https://www.keysight.com/zz/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html'>install agilent IO libraries suite and 82357 library suite</a>

Make sure you are in the correct directory. If not, use command cd to navigate the directory first.

The following code will work in either cmd or VSCode(bash command prompt)

1. install python packages 
```
py -m pip install pyvisa pyserial matplotlib
```
or
```
py -m pip install -r requirements.txt
```
If python is used, then use the following command:
```
pip install pyvisa pyserial matplotlib
```
or
```
pip install -r requirements.txt
```
2. choose the function by inputing integer
(fixed Vgs or fixed Vds)
```
py main.py
```
or 
```
python main.py
```
Please input parameters in the correct format. If there is mistake in inputing parameters, use Ctrl+C to exit the programe.

The txt file storing the numerical data will be saved with the name you chose.

Before the programe ends, it will ask if you want to save the picture plotted by data. 
