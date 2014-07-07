import math

from database import LAMP
from database import SPEAKERS


### Stored Array Devices ###

TEST_LIST = [LAMP, SPEAKERS]
TEST_DEVICE_NAME = ['Lamp', 'Speakers']

### Import Sampled Devices ###

def run_main():

    # change the XXX.txt files within the convert_to_array to the desired devices to test
    # make sure to have the txt files within the same directory as the script
    # then run or press F5

    outfile = open('result.txt','w')
    device = convert_to_array('/home/pi/samp_data.txt') ## input sample


    for idx in range(len(TEST_LIST)):
        layer_1 = correlation_matching(TEST_LIST[idx], device)
        #print(layer_1)
        layer_2 = peak_matching(TEST_LIST[idx], device)
        #print(layer_2)
        layer_3 = point_matching(TEST_LIST[idx], device)
        #print(layer_3)
        #layer_4 = rise_time_matching(TEST_LIST[idx], device)
        #layer_5 = fall_time_matching(TEST_LIST[idx], device)

        weight = 0
        
        if layer_1 == 'PASS':
            weight = weight + 0.5
        if layer_2 == 'PASS':
            weight = weight + 0.1
        if layer_3 == 'PASS':
            weight = weight + 0.4
        if layer_1 or layer_2 or layer_3 == 'FAIL':
            weight = weight + 0

        #print(weight)
        
        if weight > 0.4:
            outfile.write(TEST_DEVICE_NAME[idx])
            outfile.close()
            
    

def convert_to_array(text):
    unknown = []
    text_file = open(text,"r")
    for line in text_file.readlines():
        for i in line.split():
            unknown.append(int(round(float(i))))
    return unknown

### QUICK CHECK FOR POINT DEVIATION ###
def point_matching(device:list, unknown:list) -> bool:
    """ if each point of device and unknown devices more than a
specific threshold, device != unknown ... False """
    deviation = [device - unknown for device, unknown in zip(device, unknown)]
    counter = 0
    for dev in deviation:
        if -1 <= dev <= 1:
            counter = counter + 1
    if counter/len(device) >= 0.7:
        check = 'PASS'
    else:
        check = 'FAIL'
    return check
    
### CALCULATE CROSS CORRELATION FUNCTION ###
def correlation_matching(device:list, unknown:list) -> bool:
    ''' initialize variables '''
    corr = []
    n = delay = len(unknown)

    ### Calculate Cross Correlation btw Device and Unknown ###
    mx = 0
    my = 0
    ''' calc the mean '''
    for i in range(n):
        mx = mx + device[i]
        my = my + unknown[i]

    mx = mx/n
    my = my/n

    ''' calc the den part '''
    dx = 0
    dy = 0
    for i in range(n):
        dx = dx + (device[i] - mx)*(device[i] - mx)
        dy = dy + (unknown[i] - my)*(unknown[i] - my)            
    den = math.sqrt(dx*dy)

    ''' calc the num part '''
    for delay in range(-n,1):
        nxy = 0
        for i in range(n):
            ''' (i - delay) '''
            j = i + delay 
            if j < 0:
                nxy = nxy + (device[i]-mx)*(-my)
            else:
                nxy = nxy + (device[i]-mx)*(unknown[j]-my)
        r = nxy/den
        #print('delay:', delay, 'r:', r)
        corr.append(r)

    result = corr
    #print(result)

     ### Checking Cross Correlation ###

    ''' list of correlation values above 0.9 '''
    check_result = [x for x in result if x >=0.9]
    #print(check_result)

    ''' check index or delay value where first correlation value is above 0.9 '''
    if len(check_result) > 0:
        check_delay = result.index(check_result[0])
        #print(check_delay)
        ''' if index or delay for correlation value above 0.9 is within the first 10% (threshold) of samples GOOD '''
        if check_delay >= 0.7*len(device):
            #print("Unknown = Device")
            check = 'PASS'
        else:
            #print("Unknown != Device")
            check = 'FAIL'
    else:
        #print("Unknown != Device")
        check = 'FAIL'

    return check
        

### PEAK VALUE AND TIME CHECK FUNCTION ###
def peak_matching(device:list, unknown:list) -> bool:
    
    ### Find/Check Peak Value ###

    ''' peak value of device 1 '''
    rnd_list_device = [round(n,3) for n in device]
    peak_value_device = max(rnd_list_device)

    ''' peak value of unknown device '''
    rnd_list_unknown = [round(n,3) for n in unknown]
    peak_value_unknown = max(rnd_list_unknown)

    ''' determine 10% range of peak value of device 1 '''
    hi_peak = peak_value_device*1.1
    low_peak = peak_value_device*0.9

    ''' Return True If Peak value of device 1 is within 10% of unknown '''
    if low_peak < peak_value_unknown < hi_peak:
        cond_peak_value = True
    else:
        cond_peak_value = False

    ### Find/Check Time at Peak Value ###

    index_peak_device = min(enumerate(rnd_list_device), key=lambda x: abs(x[1]-peak_value_device))
    index_peak_unknown = min(enumerate(rnd_list_unknown), key=lambda x: abs(x[1]-peak_value_unknown))

    #print(index_peak_device)
    #print(index_peak_unknown)
    
    hi_idx_peak = index_peak_device[0]*1.1
    low_idx_peak = index_peak_device[0]*0.9

    ''' Return True If Time at Peak value of device 1 is within 10% of unknown '''
    if low_idx_peak <= index_peak_unknown[0] <= hi_idx_peak:
        cond_peak_time = True
    else:
        cond_peak_time = False

    ### Check Device Using Peak Value and Time ###

    if cond_peak_value and cond_peak_time:
        #Return True
        #print("Unknown = Device")
        check = 'PASS'
    else:
        #Return False
        #print("Unknown != Device")
        check = 'FAIL'

    return check

print(run_main())

