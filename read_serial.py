import time, string
import serial
import numpy as np
import time
from scipy.signal import savgol_filter


ser = serial.Serial(
	port='/dev/cu.wchusbserialfa130',
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)



running = 1

value = ''

i = 0

time.sleep(2)

t = []
ecg = []
ppg = []


while i < 600 :
	value = ser.readline()
		  
	if len(value.split('\t')) == 3:
		t.append(float(value.split('\t')[0]))
		ecg.append(float(value.split('\t')[1]))
		ppg.append(float(value.split('\t')[2]))
      
		#print time, ecg, ppg
  	 
		i = i + 1
		
for k in range(0,i):
	print t[k], ecg[k], ppg[k]


t = t[100:len(ecg)]	
ecg = ecg[100:len(ecg)]
ppg = ppg[100:len(ppg)]


ppg = savgol_filter(ppg, 53, 5)

pos_ecg = []
pos_ppg = []
t_max_ecg = []
t_max_ppg = []
	
j=0
n=len(ecg)

prag_ecg = max(ecg) - 0.2 * (max(ecg)-min(ecg))
prag_ppg = max(ppg) - 0.5 * (max(ppg)-min(ppg))

print "max_ecg = ", max(ecg)
print "min_ecg = ", min(ecg)
print "prag_ecg = ", prag_ecg


for i in range(1,n-1):
	if ((ecg[i]>ecg[i-1]) and (ecg[i]>=ecg[i+1]) and (ecg[i] > prag_ecg)):
		pos_ecg.append(i)
		t_max_ecg.append(t[i])
		j=j+1
	
k = 0	
		
for i in range(1,n-1):
	if ((ppg[i]>ppg[i-1]) and (ppg[i]>=ppg[i+1]) and (ppg[i] > prag_ppg)):
		pos_ppg.append(i)
		t_max_ppg.append(t[i])
		if k==1:
			k=k+1
		else:
			if pos_ppg[k]-pos_ppg[k-1]>40:
				k=k+1
				
if pos_ppg[0] < pos_ecg[0]:
	pos_ppg = pos_ppg[1:len(pos_ppg)]

my_length = min(len(pos_ppg), len(pos_ecg))

pos_ppg = pos_ppg[0:my_length]
pos_ecg = pos_ecg[0:my_length]
				
		
print pos_ecg
print t_max_ecg

print pos_ppg
print t_max_ppg

		
mean_delta_t = 0

for i in range(1,j):
	delta_t = t_max_ecg[i]-t_max_ecg[i-1]
	mean_delta_t = mean_delta_t + delta_t
	
	
mean_delta_t = mean_delta_t / (j-1)

print("Perioada medie: " + str(mean_delta_t) + " ms")

puls = 60 * 1000 / mean_delta_t

print("Puls: " + str("%.2f" % puls))


ptt = []

for i in range(0,my_length):
	ptt.append(t[pos_ppg[i]] - t[pos_ecg[i]])


print ptt

ptt_mediu = np.mean(ptt)

print "PTT = " + str(ptt_mediu)  + " ms"


SYS = 8.0521 * (1000.0 / ptt_mediu ) + 47.888

print "SYS: " + str(SYS) + " mmHg"

DIA = -0.4594 * ptt_mediu + 144.3

print "DIA: " + str(DIA) + " mmHg"
  	
