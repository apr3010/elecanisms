import numpy as np
import matplotlib.pyplot as plt
import csv

# took data from print statement from blinkusb.py code
result = [12598, 12590, 12606, 12574, 12647, 12495, 12493, 12468, 12373, 12340, 12340, 12305, 12274, 12238, 12310, 12292, 12164, 12207, 11745, 8990, 6648, 6792, 9014, 12602, 14833, 16197, 16000, 14892, 12452, 9534, 6869, 5063, 4027, 3809, 2686, 652, 15908, 15772, 15892, 13, 1501, 2970, 3551, 3499, 3709, 5665, 7555, 8649, 9009, 9998, 12346, 13649, 14315, 14252, 14291, 13549, 11519, 9546, 7862, 7085, 7450, 9156, 10323, 10722, 10636, 10661, 12244, 13914, 14728, 14865, 14880, 14046, 11908, 9865, 8123, 7040, 6591, 6418, 5079, 2997, 1276, 435, 300, 474, 2016, 3405, 3955, 3973, 3936, 3746, 4440, 6751, 8369, 9126, 9171, 8960, 7048, 5003, 3695, 2690]
res = [0.00040788036926832946, 0.0003399887083237943, 0.0003399887083237943, 0.0003399887083237943, 0.0002720970473792639, 0.0003399887083237943, 0.0003399887083237943, 0.0002720970473792639, 0.0002720970473792639, 0.0003399887083237943, 0.0003399887083237943, 0.0003399887083237943, 0.0003399887083237943, 0.00040788036926832946, 0.0002720970473792639, 0.00040788036926832946, 0.00040788036926832946, 0.0003399887083237943, 0.0003399887083237943, 0.0002720970473792639, 0.0003399887083237943, 0.0002720970473792639, 0.0003399887083237943, 0.0003399887083237943, 0.00047577203021285984, 0.00047577203021285984, 0.0003399887083237943, 0.0003399887083237943, 0.0003399887083237943, 0.00020420538643472883, 0.00040788036926832946, 0.0003399887083237943, 0.00040788036926832946, 0.00040788036926832946, 0.00020420538643472883, 0.0003399887083237943, 0.0003399887083237943, 0.0003399887083237943, 0.00047577203021285984, 0.00047577203021285984, 0.00040788036926832946, 0.0003399887083237943, 0.00047577203021285984, 0.0003399887083237943, -0.00013525291828793727, 0.00040788036926832946, 0.00040788036926832946, 0.00040788036926832946, 0.00047577203021285984, 0.0003399887083237943, 0.0003399887083237943, 0.0003399887083237943, 0.0002720970473792639, 0.00040788036926832946, 0.0002720970473792639, 0.0003399887083237943, 5.304036011282303e-07, 0.0002720970473792639, 0.0002720970473792639, 0.0003399887083237943, 0.00040788036926832946, 0.00040788036926832946, 0.0003399887083237943, 0.00040788036926832946, 0.0003399887083237943, 0.00040788036926832946, 0.0003399887083237943, 0.0003399887083237943, 0.00040788036926832946, 0.0003399887083237943, 0.0003399887083237943, 0.0003399887083237943, 0.0003399887083237943, 0.0003399887083237943, 0.00040788036926832946, 0.00040788036926832946, 0.0003399887083237943, 0.00040788036926832946, 0.0003399887083237943, 0.00040788036926832946, 0.0003399887083237943, 0.0003399887083237943, 0.0003399887083237943, 0.00047577203021285984, 0.00040788036926832946, 0.0003399887083237943, 0.00047577203021285984, 0.0003399887083237943, 0.00040788036926832946, 0.00040788036926832946, 0.0003399887083237943, 0.0002720970473792639, 0.00040788036926832946, 0.0003399887083237943, 0.0003399887083237943, 0.0003399887083237943, 0.00040788036926832946, 0.00040788036926832946, 0.0002720970473792639, 0.0003399887083237943]
# result1 = []
# result2 = []

# created two separate lists of data to compile in excel
# for i in range (0, len(result)-1):
# 	if result[i]>30000:
# 		result1.append((i+1)*0.001)
# 		result2.append(result[i])

# print result1
plt.subplot(211)

# plot graph of data
for i in range (0,len(result)-1):
	plt.scatter(i,result[i])
	plt.plot(i,result[i])

# plt.xlabel('Time(ms)')
plt.ylabel('Position')
plt.title('Position/Torque vs. Time')
plt.figure(1)
plt.subplot(212)
plt.axis([-20, 120, 0,  0.0005])
for i in range (0,len(result)-1):
	plt.scatter(i,res[i])
	plt.plot(i,res[i])

plt.ylabel('Torque')
plt.xlabel('Time (ms)')
plt.show()
# code to output into excel file
with open("spring.csv",'wb') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerow(result)
    wr.writerow(res)