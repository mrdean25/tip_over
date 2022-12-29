from mpu6050 import mpu6050
import threading
import time

#Declaring accel as global
accel_data = []
start_timer= False
counter_timeout = False



def get_accel_task():
    
    while True:
        
        global accel_data
        accel_data = mpu.get_accel_data()

        accel_data['x'] = round (accel_data['x'], 4)
        accel_data['y'] = round (accel_data['y'], 4)
        accel_data['z'] = round (accel_data['z'], 4)

        #print('Accel: {} {} {}'.format(accel_data['x'], accel_data['y'],accel_data['z'] ))

        time.sleep(0.10)


def check_tip_over():

    global accel_data
    global start_timer
    global counter_timeout
    get_accel =[0, 0, 0, 0]

    while True:
    
        #read 4 values from accelerometer
        for x in range (0, 3):
            get_accel[x] = abs(accel_data['x']) 
            time.sleep(0.020)
        
        
        #sum and average
        average_accel = sum (get_accel) / 4
        print('The sum is {}'.format(average_accel))

        if average_accel >= 6:
            
            if counter_timeout == False:
                start_timer = True
            
            else:
                start_timer = False
                                                
        else:
            print('No Tip over')
            start_timer = False
            counter_timeout = False
    
        time.sleep(1)

def start_timer(timeout = 30):
    
    global start_timer
    global counter_timeout
    
    timer = time.time()
    counter_time = 1
    counter = 0
    print('------------------Timer started-----------------------')
    
    while True:
        #convert seconds to millis
        if (time.time() - timer) >= counter_time and start_timer == True:
           counter = counter + 1
           print('counter is {}'.format(counter))
           timer = time.time()

           if counter >= timeout:
                start_timer = False
                counter_timeout = True
                print('Tip over detected')
                counter = 0

        if start_timer == False:
           counter = 0

mpu = mpu6050(0x68)
print(mpu.get_temp())

#Create thread
t1 = threading.Thread(target=get_accel_task)
t2 = threading.Thread(target=check_tip_over)
t3 = threading.Thread(target=start_timer)

#start thread
t1.start()
t2.start()
t3.start()

#wait till thread ends and join in main thread
t1.join()
t2.join()
t3.join()