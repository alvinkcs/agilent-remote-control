# print('hello world')
import pyvisa
import matplotlib.pyplot as plt
import time
import os
import pyserial.espec
# import visa
rm = pyvisa.ResourceManager()
print(rm)
print(rm.list_resources())

x = [] # saving x-values for plotting graph
y = [] # saving y-values for plotting graph
# z = [0,-1,-2,-3,-4,-5]

measure_inst = rm.open_resource('GPIB0::22::INSTR') # 34401
dcSupply_inst = rm.open_resource('GPIB0::10::INSTR') # 8200

measure_inst.write("*RST") # reset
measure_inst.write('*CLS') # clear
# measure_inst.write('CONF:CURR:DC DEF,DEF')
measure_value = measure_inst.query('MEAS:CURR:DC? DEF,DEF')

inst_33120A = rm.open_resource('GPIB0::11::INSTR') # 33120A
inst_33120A.write('*RST')
inst_33120A.write('*CLS')
inst_33120A.write('OUTP:LOAD INF')
inst_33120A.write('APPL:DC DEF, DEF, 0')

txt_file_index = 1
while (os.path.isfile('testrun%i.txt'%(txt_file_index)) == True):
    txt_file_index += 1

# startV = input('Vds start voltage:')
# finalV = input('Vds final voltage:')
# diff = float(input('voltage difference in each step:'))
# delay_time = float(input('delay time in each for cooling down:'))
startV = 0
finalV = 0
diff = 0
delay_time = 0

def run_measurement(voltage):

    # voltage = z[iteration]
    # voltage = current_vgs
    if (voltage >= 0):
        inst_33120A.write('APPL:DC DEF, DEF, +%s' %(str(voltage)))
        # print('APPL:DC DEF, DEF, +%s' %(str(voltage).ljust(9,'0')))
    else:
        inst_33120A.write('APPL:DC DEF, DEF, %s' %(str(voltage)))
        # print('APPL:DC DEF, DEF, %s' %(str(voltage)))

    steps = int((int(finalV) - int(startV))/float(diff) + 1)
    currentV = int(startV)
    def delay(sec):
        dcSupply_inst.write('V1+%f' %(0.0))
        time.sleep(sec)
    for i in range(steps):
        if (currentV >= 0):
            dcSupply_inst.write('V1+%f' %(currentV/10.0)) # V1+0.1000 = 0.1x10^1 = 1V
        else:
            dcSupply_inst.write('V1%f' %(currentV/10.0)) # V1-0.1000 = -0.1x10^1 = -1V

        # print('%f\t' %(currentV),measure_inst.query('MEAS?'))
        with open('testrun%i.txt'%(txt_file_index), 'a') as file:
            # measure_value = measure_inst.query('MEAS:CURR:DC? DEF,DEF')
            measure_inst.write('TRIG:SOUR IMM')
            measure_value = measure_inst.query('READ?')
            content = "%f\t%s" %(currentV,measure_value)
            file.write(content)
            x.append(currentV)
            y.append(float(measure_value))

        currentV = currentV + float(diff)
        # print(currentV)
        delay(delay_time) # cool down the circuit

    dcSupply_inst.write('V1+%f' %(0.0)) # change back to 0V for safety

def fixed_vds(vgs_startV=0,vgs_finalV=0,vgs_diff=0,vds_value=0,delay_time=0):
    if (vgs_startV == 0 and vgs_finalV == 0 and vgs_diff == 0 and vds_value ==0 and delay_time == 0):
        vgs_startV = float(input('Vgs start voltage:'))
        vgs_finalV = float(input('Vgs final voltage:'))
        vgs_diff = float(input('Vgs voltage difference in each step:'))
        vds_value = float(input('Vds DC supply:'))
        delay_time = float(input('cooling time in each step:'))
    vgs_iterations = int((vgs_finalV - vgs_startV)/vgs_diff + 1)
    current_vgs = vgs_startV
    def delay(sec):
        inst_33120A.write('APPL:DC DEF, DEF, +%s' %(str(0.0)))
        time.sleep(sec)
    def measure_delay():
        time.sleep(0.5)
    if (vds_value >= 0):
        dcSupply_inst.write('V1+%f' %(vds_value/10.0)) # V1+0.1000 = 0.1x10^1 = 1V
    else:
        dcSupply_inst.write('V1%f' %(vds_value/10.0)) # V1+0.1000 = 0.1x10^1 = 1V
    for i in range(vgs_iterations):
        inst_33120A.write('APPL:DC DEF, DEF, %s' %(str(current_vgs)))

        with open('testrun%i.txt'%(txt_file_index), 'a') as file:
            # measure_value = measure_inst.query('MEAS:CURR:DC? DEF,DEF')
            measure_delay()
            measure_inst.write('TRIG:SOUR IMM')
            measure_value = measure_inst.query('READ?')
            content = "%f\t%s" %(current_vgs,measure_value)
            file.write(content)
            x.append(current_vgs)
            y.append(float(measure_value))
        
        current_vgs += vgs_diff
        delay(delay_time)

def vds_test_with_diff_vgs():
    global startV, finalV, diff, delay_time
    startV = input('Vds start voltage:')
    finalV = input('Vds final voltage:')
    diff = float(input('voltage difference in each step:'))
    delay_time = float(input('delay time in each for cooling down:'))

    vgs_startV = float(input('Vgs start voltage:'))
    vgs_finalV = float(input('Vgs final voltage:'))
    vgs_diff = float(input('Vgs voltage difference in each step:'))
    vgs_iterations = int((vgs_finalV - vgs_startV)/vgs_diff + 1)
    current_vgs = vgs_startV
    for j in range(vgs_iterations):
        run_measurement(current_vgs)
        global x,y
        plt.plot(x,y, label = 'Vgs = %iV'%(j))
        x = []
        y = []
        current_vgs += vgs_diff

    plt.legend() # to show the label indicators

def vgs_test_with_fixed_vds():
    fixed_vds(vgs_startV=0,vgs_finalV=-5,vgs_diff=-0.1,vds_value=-5,delay_time=0.5)
    global x,y
    plt.plot(x,y)
    dcSupply_inst.write('V1+%f' %(0/10.0)) # V1+0.1000 = 0.1x10^1 = 1V

def integrated_test_with_temp(temp=20):
    pyserial.espec.run_test(temp)
    print('wait 1min')
    time.sleep(60)
    while (True):
        result = (pyserial.espec.temp_monitor())
        print(result)
        result_arr = result.split(',')
        if (abs(float(result_arr[0]) - float(result_arr[1])) <= 0.2):
            break
        else:
            print('wait 30sec')
            time.sleep(30)
    print('starting vgs_test_with_fixed_vds')
    vgs_test_with_fixed_vds()
    global x,y
    plt.plot(x,y, label = 'Temp = %f'%(temp))
    x = []
    y = []
    plt.legend()

choice = int(input('Please select a test below\nVds test with diff Vgs (0)\nVgs test with fixed Vds (1)\nTest with diff temp. (2)\ninput 0 or 1 or 2:'))
if (choice == 0):
    vds_test_with_diff_vgs()
elif (choice == 1):
    vgs_test_with_fixed_vds()
elif (choice == 2):
    integrated_test_with_temp(50)
    integrated_test_with_temp(20)
else:
    print('incorrect input')

inst_33120A.write('APPL:DC DEF, DEF, +%s' %('0.0'))
print('Done')
plt.xlabel('Voltage supply')
plt.ylabel('current measured')
plt.title('current against voltage measurement')
# plt.legend() # to show the label indicators
saving_picture = input('save the picture? (y/N):')
if (saving_picture == 'y'):
    picture_name = input('picture name:')
    picture_name += '.png'
    plt.savefig(picture_name)
plt.show()