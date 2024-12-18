# this is for setting the Vgs (33120A) alone
import pyvisa
import matplotlib.pyplot as plt
# import visa
rm = pyvisa.ResourceManager()
print(rm)
print(rm.list_resources())

inst = rm.open_resource('GPIB0::11::INSTR') # 33120A
inst.write('*RST')
inst.write('*CLS')
inst.write('OUTP:LOAD INF')
inst.write('APPL:DC DEF, DEF, 0')
voltage = float(input('voltage:'))
if (voltage >= 0):
    inst.write('APPL:DC DEF, DEF, +%s' %(str(voltage)))
    # print('APPL:DC DEF, DEF, +%s' %(str(voltage).ljust(9,'0')))
else:
    inst.write('APPL:DC DEF, DEF, %s' %(str(voltage)))
    print('APPL:DC DEF, DEF, %s' %(str(voltage)))