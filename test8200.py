# import socket
# import time
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('localhost', 8200))
# while True:
#     time.sleep(5)
#     data = client_socket.recv(512)
#     if data.lower() == 'q':
#         client_socket.close()
#         break
#     print('RECEIVED: %s' %data)
#     data = input('SEND( TYPE q or Q to quit):')
#     client_socket.send(data)
#     if data.lower() == 'q':
#         client_socket.close()
#         break

# import time
# def func():
#     print('hello')
# def timer(delay, fun):
#     time.sleep(delay)
#     fun()

# timer(3,func)

# import os
# print(os.path.isfile('testrun.txt'))
import matplotlib.pyplot as plt
x = []
y = []
count = 0
vgs = 0
with open('testrun5.txt', 'r') as file:
    for line in file:
        data_list = line.split('\t')
        # print(line.strip())
        x.append(float(data_list[0]))
        y.append(float(data_list[1]))
        if (count == 50):
            plt.plot(x,y, label='Vgs = 0s -%iV'%(vgs))
            x = []
            y = []
            count = 0
            vgs += 1
        else:
            count +=1
x = []
y = []
count = 0
vgs = 0
with open('testrun6.txt', 'r') as file:
    for line in file:
        data_list = line.split('\t')
        # print(line.strip())
        x.append(float(data_list[0]))
        y.append(float(data_list[1]))
        if (count == 50):
            plt.plot(x,y, label='Vgs = 3s -%iV'%(vgs))
            x = []
            y = []
            count = 0
            vgs += 1
        else:
            count +=1

plt.xlabel('Voltage supply')
plt.ylabel('current measured')
plt.title('current against voltage measurement')
plt.legend()
plt.savefig('comparison of 0s vs 3s cool down')
plt.show()