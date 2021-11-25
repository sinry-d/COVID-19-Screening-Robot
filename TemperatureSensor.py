import time
from gpiozero import LED
from smbus2 import SMBus
from mlx90614 import MLX90614 
from notify_run import Notify

#Set up notify run channel
notify = Notify(endpoint="https://notify.run/hPa9ESszlWgPxU2wGm3c")

bus = SMBus(1)
yellow = LED(14)
yellow.off()
sensor = MLX90614(bus, address=0x5A)
wristTemp = sensor.get_object_1()
#Retakes temperature if the temperature is not in a valid human range to a maximum of 100 times
#Note: Less than 26*C and greater than 43*C often results in death
counter = 100
print("Please move your wrist in front of the sensor\n")

while (wristTemp<26 or wristTemp>43) and counter>0:
    wristTemp = sensor.get_object_1()
    counter = counter-1 
    #delay each loop by 3 seconds
    time.sleep(1) 
print("")
#Round wrist temp and find time
wristTemp = round(wristTemp,2)
t = time.localtime()
timeNow = time.strftime("%H:%M:%S", t)
#After taking a reasonable temperature, checks to see if the person can enter
#And sends notifications to the notify-run channel
if(wristTemp<30):
    yellow.on() #Turns on LED
    print("Temperature too low: ", wristTemp, " *C \n")
    print("You may enter, but consider getting that checked out\n")
    notify.send('Temperature: '+str(wristTemp)+'*C '+timeNow+'EST')
elif(wristTemp>36):
    print("Your temperature is too high: ", wristTemp, " *C\n")
    print("Please stay where you are until someone comes to assist you\n")
    #If temperature is too high, notify the supervisor in the notify-run channel
    notify.send('TEMP ALERT: ADDRESS IMMEDIATELY: Temperature: '+str(wristTemp)+'*C '+timeNow+'EST')
else:
    yellow.on()
    print("Your temperature is: ", wristTemp," *C\n")
    print("Thanks for cooperating with us, you may enter\n")
    notify.send('Temperature: '+str(wristTemp)+'*C '+timeNow+'EST')
time.sleep(5) #Extend LED light-up time
bus.close()
