import detect_mask
import TemperatureSensor
import functions

def main():
    max_capacity = 2
    current_capacity = 0
    goodtemp = (False, 0)
    maskon = False

    mask = "Off"
    allow = "No"

    maskon = detect_mask.detectmask()
    if maskon == True:
        goodtemp = TemperatureSensor.tempsensor()
        mask = "On"

    if (maskon and goodtemp[1]):
        if (current_capacity==max_capacity):
            print ("Please wait for someone to leave before entering")
        else:
            print ("You are safe to enter")
            allow="Yes"
            current_capacity += 1
        maskon = False
        goodtemp[1] = False
    else:
        print ("You may not enter")
        maskon = False
        goodtemp[1] = False

    return current_capacity, mask, goodtemp[2], allow


