<a href='https://github.com/alvinkcs/agilent-remote-control'>Github reference</a>

<h3>Both py or python work.</h3>
<a href='https://www.keysight.com/zz/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html'>install agilent IO libraries suite and 82357 library suite</a>

<b>Make sure you are in the correct directory. If not, use command cd to navigate the directory first.</b>
```
cd C:\Users\fillab\Desktop\agilent-remote-control-main\agilent-remote-control-main
```

Go to <b>Device Manager</b> and search the port number your USB is connected to. If it's <b>COM3</b>, change the line 3 of espec.py from pyserial folder as follows:

ser = serial.Serial(port='COM3'

The following code will work in either cmd or VSCode(bash command prompt)

1. install python packages
```
pip install pyvisa pyserial matplotlib
```
```
py -m pip install pyvisa pyserial matplotlib
```
or
```
pip install -r requirements.txt
```
```
py -m pip install -r requirements.txt
```
2. choose the function by inputing integer
(fixed Vgs or fixed Vds)
```
python main.py
```
or 
```
py main.py
```
Please input parameters in the correct format. If there is mistake in inputing parameters, use Ctrl+C to exit the programe.

The txt file storing the numerical data will be saved with the name you chose.

Before the programe ends, it will ask if you want to save the picture plotted by data. 
