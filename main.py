import pyvisa
import matplotlib.pyplot as plt
import time
import os
import pyserial.espec
rm = pyvisa.ResourceManager()
print(rm)
print(rm.list_resources())

x = [] # saving x-values for plotting graph
y = [] # saving y-values for plotting graph

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

# startV = 0
# finalV = 0
# diff = 0
# delay_time = 0
vgs_startV = 0.0
vgs_finalV = 0.0
vgs_diff = 0.0
vds_value = 0.0
delay_time = 0.0

def vds_increment(voltage=0.0,startV=0.0,finalV=0.0,diff=0.0,delay_time=0.0):

    # voltage = current_vgs
    if (voltage >= 0.0):
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

def vds_test_with_diff_vgs(temp=-273):
    vgs_iterations = int((vgs_finalV - vgs_startV)/vgs_diff + 1)
    current_vgs = vgs_startV
    for j in range(vgs_iterations):
        vds_increment(current_vgs, startV, finalV, diff, delay_time)
        global x,y
        if (temp == -273):
            plt.plot(x,y, label = 'Vgs = %iV'%(j))
        else:
            # plt.plot(x,y, label = 'Vgs = %iV with temp = %f'%(j,temp))
            plt.plot(x,y, label = '%iV, %f'%(j,temp))
        x = []
        y = []
        current_vgs += vgs_diff
    inst_33120A.write('APPL:DC DEF, DEF, +%s' %(str(0.0))) # set back to zero
    plt.legend() # to show the label indicators

def vgs_test_with_fixed_vds(vgs_startV=0.0,vgs_finalV=0.0,vgs_diff=0.0,vds_value=0.0,delay_time=0.0):
    global x,y
    fixed_vds(vgs_startV,vgs_finalV,vgs_diff,vds_value,delay_time)
    plt.plot(x,y)
    dcSupply_inst.write('V1+%f' %(0/10.0)) # V1+0.1000 = 0.1x10^1 = 1V

def integrated_test_with_temp(temp=20,test_choice=0):
    pyserial.espec.run_test(temp)
    print('wait 1min')
    time.sleep(60)
    while (True):
        result = (pyserial.espec.temp_monitor())
        print(result)
        result_arr = result.split(',')
        if (abs(float(result_arr[0]) - float(result_arr[1])) <= 0.205): # for dealing with truncation
            break
        else:
            print('wait 30sec')
            time.sleep(30)
    global x,y
    if (test_choice == 0):
        print('starting vds_test_with_diff_vgs')
        vds_test_with_diff_vgs()
    elif (test_choice == 1):
        print('starting vgs_test_with_fixed_vds')
        vgs_test_with_fixed_vds(vgs_startV,vgs_finalV,vgs_diff,vds_value,delay_time)
        plt.plot(x,y, label = 'Temp = %f'%(temp))
    x = []
    y = []
    plt.legend()

choice = int(input('Please select a test below\nVds test with diff Vgs (0)\nVgs test with fixed Vds (1)\nTest with diff temp. (2)\ninput 0 or 1 or 2:'))
if (choice == 0):
    startV = float(input('Vds start voltage:'))
    finalV = float(input('Vds final voltage:'))
    diff = float(input('voltage difference in each step:'))
    delay_time = float(input('delay time in each for cooling down:'))

    vgs_startV = float(input('Vgs start voltage:'))
    vgs_finalV = float(input('Vgs final voltage:'))
    vgs_diff = float(input('Vgs voltage difference in each step:'))
    vds_test_with_diff_vgs()
    plt.xlabel('VDS[V]')
elif (choice == 1):
    vgs_startV = float(input('Vgs start voltage:'))
    vgs_finalV = float(input('Vgs final voltage:'))
    vgs_diff = float(input('Vgs voltage difference in each step:'))
    vds_value = float(input('Vds voltage:'))
    delay_time = float(input('delay time in each step for cooling down:'))
    vgs_test_with_fixed_vds(vgs_startV,vgs_finalV,vgs_diff,vds_value,delay_time)
    plt.xlabel('VGS[V]')
elif (choice == 2):
    test_choice = int(input('Please select a test with temp below\nVds test with diff Vgs (0)\nVgs test with fixed Vds (1)\ninput 0 or 1:'))
    temps = input('Please input a series of temp that to be testing with space (format:80 50 20 -10):')
    temps_arr = temps.split()
    if (test_choice == 0):
        startV = float(input('Vds start voltage:'))
        finalV = float(input('Vds final voltage:'))
        diff = float(input('voltage difference in each step:'))
        delay_time = float(input('delay time in each for cooling down:'))

        vgs_startV = float(input('Vgs start voltage:'))
        vgs_finalV = float(input('Vgs final voltage:'))
        vgs_diff = float(input('Vgs voltage difference in each step:'))
        for temp in temps_arr:
            integrated_test_with_temp(float(temp),test_choice)
        # integrated_test_with_temp(80,test_choice)
        # integrated_test_with_temp(50,test_choice)
        # integrated_test_with_temp(20,test_choice)
        # integrated_test_with_temp(-10,test_choice)
        plt.xlabel('VDS[V]')
    elif (test_choice == 1):
        vgs_startV = float(input('Vgs start voltage:'))
        vgs_finalV = float(input('Vgs final voltage:'))
        vgs_diff = float(input('Vgs voltage difference in each step:'))
        vds_value = float(input('Vds voltage:'))
        delay_time = float(input('delay time in each step for cooling down:'))
        for temp in temps_arr:
            integrated_test_with_temp(float(temp),test_choice)
        # integrated_test_with_temp(80,test_choice)
        # integrated_test_with_temp(50,test_choice)
        # integrated_test_with_temp(20,test_choice)
        # integrated_test_with_temp(-10,test_choice)
        plt.xlabel('VGS[V]')
    else:
        print('incorrect input')
else:
    print('incorrect input')

inst_33120A.write('APPL:DC DEF, DEF, +%s' %('0.0'))
print('Done')
# plt.xlabel('VDS[V] or VGS[V]')
plt.ylabel('ID[A]')
plt.title('current against voltage measurement')
# plt.legend() # to show the label indicators
saving_picture = input('save the picture? (y/N):')
if (saving_picture.lower() == 'y'):
    picture_name = input('picture name:')
    picture_name += '.png'
    plt.savefig(picture_name)
plt.show()