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

# txt_file_index = 1
# while (os.path.isfile('testrun%i.txt'%(txt_file_index)) == True):
#     txt_file_index += 1

txt_file_name = input("Please input a txt file name (.txt is not needed):")

txt_label_arr = []

# startV = 0
# finalV = 0
# diff = 0
# delay_time = 0
vgs_startV = 0.0
vgs_finalV = 0.0
vgs_diff = 0.0
vds_value = 0.0
delay_time = 0.0

def vds_increment(arr,vgs_iteration,temp_iteration=0,voltage=0.0,startV=0.0,finalV=0.0,diff=0.0,delay_time=0.0):

    # voltage = current_vgs
    if (voltage >= 0.0):
        inst_33120A.write('APPL:DC DEF, DEF, +%s' %(str(voltage)))
        # print('APPL:DC DEF, DEF, +%s' %(str(voltage).ljust(9,'0')))
    else:
        inst_33120A.write('APPL:DC DEF, DEF, %s' %(str(voltage)))
        # print('APPL:DC DEF, DEF, %s' %(str(voltage)))

    steps = int((int(finalV) - int(startV))/float(diff) + 1)
    currentV = int(startV)
    vgs_steps = int((vgs_finalV - vgs_startV)/vgs_diff) + 1
    def delay(sec):
        dcSupply_inst.write('V1+%f' %(0.0))
        time.sleep(sec)
    for i in range(steps):
        if (currentV >= 0):
            dcSupply_inst.write('V1+%f' %(currentV/10.0)) # V1+0.1000 = 0.1x10^1 = 1V
        else:
            dcSupply_inst.write('V1%f' %(currentV/10.0)) # V1-0.1000 = -0.1x10^1 = -1V

        measure_inst.write('TRIG:SOUR IMM')
        measure_value = measure_inst.query('READ?')
        arr[i][0] = "%.2f" % currentV # can be improved to reduce repeated input
        arr[i][vgs_iteration+temp_iteration*vgs_steps+1] = str(measure_value).strip()
        x.append(currentV)
        y.append(float(measure_value))

        currentV = currentV + float(diff)
        if (delay_time != 0):
            delay(delay_time) # cool down the circuit

    dcSupply_inst.write('V1+%f' %(0.0)) # change back to 0V for safety

def fixed_vds(arr,temp_iteration=0,vgs_startV=0,vgs_finalV=0,vgs_diff=0,vds_value=0,delay_time=0):
    if (vgs_startV == 0 and vgs_finalV == 0 and vgs_diff == 0 and vds_value == 0 and delay_time == 0):
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

        measure_delay()
        measure_inst.write('TRIG:SOUR IMM')
        measure_value = measure_inst.query('READ?')
        arr[i][0] = "%.2f" % current_vgs
        arr[i][temp_iteration+1] = str(measure_value).strip()
        x.append(current_vgs)
        y.append(float(measure_value))
        
        current_vgs += vgs_diff
        if (delay_time != 0):
            delay(delay_time)

def vds_test_with_diff_vgs(arr,temp=-273,temp_iteration=0):
    vgs_iterations = int((vgs_finalV - vgs_startV)/vgs_diff + 1)
    current_vgs = vgs_startV
    for j in range(vgs_iterations):
        vds_increment(arr,vgs_iteration=j,temp_iteration=temp_iteration, voltage=current_vgs, startV=startV, finalV=finalV, diff=diff, delay_time=delay_time)
        global x,y
        if (temp == -273):
            plt.plot(x,y, label = 'Vgs = %iV'%(current_vgs))
            txt_label_arr.append("%fV"%(current_vgs))
        else:
            # plt.plot(x,y, label = 'Vgs = %iV with temp = %f'%(j,temp))
            plt.plot(x,y, label = '%iV, %f'%(current_vgs,temp))
            txt_label_arr.append("%.2fV,Temp=%i"%(current_vgs,temp))
        x = []
        y = []
        current_vgs += vgs_diff
    dcSupply_inst.write('V1+%f' %(0/10.0)) # V1+0.1000 = 0.1x10^1 = 1V
    inst_33120A.write('APPL:DC DEF, DEF, +%s' %(str(0.0))) # set back to zero
    plt.legend() # to show the label indicators

def vgs_test_with_fixed_vds(arr,temp=-273,temp_iteration=0,vgs_startV=0.0,vgs_finalV=0.0,vgs_diff=0.0,vds_value=0.0,delay_time=0.0):
    global x,y
    fixed_vds(arr=arr,temp_iteration=temp_iteration,vgs_startV=vgs_startV,vgs_finalV=vgs_finalV,vgs_diff=vgs_diff,vds_value=vds_value,delay_time=delay_time)
    if (temp != -273):
        txt_label_arr.append("Temp=%i"%(temp))
    plt.plot(x,y)
    dcSupply_inst.write('V1+%f' %(0/10.0)) # V1+0.1000 = 0.1x10^1 = 1V
    inst_33120A.write('APPL:DC DEF, DEF, +%s' %(str(0.0))) # set back to zero

def integrated_test_with_temp(arr,temp=20,test_choice=0,temp_iteration=0):
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
        vds_test_with_diff_vgs(arr,temp=temp,temp_iteration=temp_iteration)
    elif (test_choice == 1):
        print('starting vgs_test_with_fixed_vds')
        vgs_test_with_fixed_vds(arr,temp=temp,temp_iteration=temp_iteration,vgs_startV=vgs_startV,vgs_finalV=vgs_finalV,vgs_diff=vgs_diff,vds_value=vds_value,delay_time=delay_time)
        plt.plot(x,y, label = 'Temp = %f'%(temp))
    x = []
    y = []
    plt.legend()

choice = int(input('Please select a test below\nVds test with diff Vgs (0)\nVgs test with fixed Vds (1)\nTest with diff temp. (2)\ninput 0 or 1 or 2:'))
if (choice == 0):
    startV = float(input('Vds start voltage:'))
    finalV = float(input('Vds final voltage:'))
    diff = float(input('voltage difference in each step:'))

    row_of_array_for_txtfile = int((finalV-startV)/diff+1)
    
    delay_time = float(input('delay time in each for cooling down:'))

    vgs_startV = float(input('Vgs start voltage:'))
    vgs_finalV = float(input('Vgs final voltage:'))
    vgs_diff = float(input('Vgs voltage difference in each step:'))

    col_of_array_for_txtfile = int((vgs_finalV-vgs_startV)/vgs_diff+1)+1

    array_for_txtfile = [[0.0 for x in range(col_of_array_for_txtfile)] for y in range(row_of_array_for_txtfile)]

    vds_test_with_diff_vgs(arr=array_for_txtfile)
    plt.xlabel('VDS[V]')
elif (choice == 1):
    vgs_startV = float(input('Vgs start voltage:'))
    vgs_finalV = float(input('Vgs final voltage:'))
    vgs_diff = float(input('Vgs voltage difference in each step:'))

    row_of_array_for_txtfile = int((vgs_finalV-vgs_startV)/vgs_diff+1)
    col_of_array_for_txtfile = 2
    array_for_txtfile = [[0 for x in range(col_of_array_for_txtfile)] for y in range(row_of_array_for_txtfile)]

    vds_value = float(input('Vds voltage:'))
    delay_time = float(input('delay time in each step for cooling down:'))
    vgs_test_with_fixed_vds(arr=array_for_txtfile,vgs_startV=vgs_startV,vgs_finalV=vgs_finalV,vgs_diff=vgs_diff,vds_value=vds_value,delay_time=delay_time)
    plt.xlabel('VGS[V]')
elif (choice == 2):
    test_choice = int(input('Please select a test with temp below\nVds test with diff Vgs (0)\nVgs test with fixed Vds (1)\ninput 0 or 1:'))
    temps = input('Please input a series of temp that to be testing with space (format:80 50 20 -10):')
    temps_arr = temps.split()
    if (test_choice == 0):
        startV = float(input('Vds start voltage:'))
        finalV = float(input('Vds final voltage:'))
        diff = float(input('voltage difference in each step:'))

        row_of_array_for_txtfile = int((finalV-startV)/diff+1)

        delay_time = float(input('delay time in each for cooling down:'))

        vgs_startV = float(input('Vgs start voltage:'))
        vgs_finalV = float(input('Vgs final voltage:'))
        vgs_diff = float(input('Vgs voltage difference in each step:'))

        col_of_array_for_txtfile = int((vgs_finalV-vgs_startV)/vgs_diff+1)*len(temps_arr)+1

        array_for_txtfile = [[0 for x in range(col_of_array_for_txtfile)] for y in range(row_of_array_for_txtfile)]

        temp_iteration = 0
        for temp in temps_arr:
            integrated_test_with_temp(arr=array_for_txtfile,temp=float(temp),test_choice=test_choice,temp_iteration=temp_iteration)
            temp_iteration = temp_iteration + 1
        plt.xlabel('VDS[V]')
    elif (test_choice == 1):
        vgs_startV = float(input('Vgs start voltage:'))
        vgs_finalV = float(input('Vgs final voltage:'))
        vgs_diff = float(input('Vgs voltage difference in each step:'))

        row_of_array_for_txtfile = int((vgs_finalV-vgs_startV)/vgs_diff+1)

        col_of_array_for_txtfile = len(temps_arr)+1

        array_for_txtfile = [[0 for x in range(col_of_array_for_txtfile)] for y in range(row_of_array_for_txtfile)]

        vds_value = float(input('Vds voltage:'))
        delay_time = float(input('delay time in each step for cooling down:'))
        temp_iteration = 0
        for temp in temps_arr:
            integrated_test_with_temp(arr=array_for_txtfile,temp=float(temp),test_choice=test_choice,temp_iteration=temp_iteration)
            temp_iteration = temp_iteration + 1
        plt.xlabel('VGS[V]')
    else:
        print('incorrect input')
else:
    print('incorrect input')

with open('%s.txt'%(txt_file_name), 'a') as file:
    if (choice == 1 or (choice == 2 and test_choice == 1)):
        file.write('#VGS[V]\t')
    else:
        file.write('#VDS[V]\t')
    for i in range(len(txt_label_arr)):
        file.write("%s\t"%(txt_label_arr[i]))
    file.write('\n')
    for i in range(row_of_array_for_txtfile):
        for j in range(col_of_array_for_txtfile):
            file.write("%s\t"%(str(array_for_txtfile[i][j])))
        file.write('\n')

inst_33120A.write('APPL:DC DEF, DEpy F, +%s' %('0.0'))
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