import time

from smbus2 import SMBus
from mlx90614 import MLX90614 

# from notifypy import Notify

#Default notification settings for texts to your phone
# notification = Notify(
#   default_notification_title="Covid-Robot Alert",
#   # default_application_name="Great Application",
#   # default_notification_icon="path/to/icon.png",
#   # default_notification_audio="path/to/sound.wav"
# )

bus = SMBus(1)
#Note: Address should be checked using $ sudo i2cdetect -y 1
sensor = MLX90614(bus, address=0x5A)
wristTemp = sensor.get_object_1()
#print (sensor.get_amb_temp()) #Prints environment temperature to the console
#print (sensor.get_object_1()) #Prints object temperature to the console
#Retakes temperature if the temperature is not in a valid human range to a maximum of 100 times
#Note: Less than 31*C and greater than 43*C often results in death
counter = 100
while (wristTemp<31 of wristTemp>43) and counter>0:
    print("Please move your wrist in front of the sensor\n")
    wristTemp = sensor.get_object_1()
    counter = counter-1 
    #delay each loop by 3 seconds
    time.sleep(1) 
#After taking a reasonable temperature, checks to see if the person can enter
if(wristTemp<36.1):
    print("Temperature too low: ", wristTemp, " *C \n")
    print("You may enter, but consider getting that checked out\n")
elif(wristTemp>37.8):
    print("Your temperature is too high: ", wristTemp, " *C\n")
    print("Please stay where you are until someone comes to assist you\n")
    #Gets current time
    t = time.localtime()
    timeNow = time.strftime("%H:%M:%S", t)
    #Alerts manager via phone notifications if the customer has a fever
    #notification.message = "Customer temperature too high, please address immediately ", timeNow," EST"
    #notification.send()
else:
    print("Your temperature is: ", wristTemp," *C\n")
    print("Thanks for cooperating with us, you may enter\n")

bus.close()
