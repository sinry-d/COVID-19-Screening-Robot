import detect_mask
import TemperatureSensor

max_capacity = 2
current_capacity = 0
goodtemp = False
maskon = False

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n------------------------")
print("COVID ROBOT:")
print("------------------------")


while True:
    maskon = detect_mask.detectmask()
    if maskon == True:
        goodtemp = TemperatureSensor.tempsensor()

    if (maskon and goodtemp):
        if (current_capacity==max_capacity):
            print ("Please wait for someone to leave before entering")
        else:
            print ("You are safe to enter")
            current_capacity += 1
        maskon = False
        goodtemp = False
    else:
        print ("You may not enter")
        maskon = False
        goodtemp = False

    print("\n\n\n")


