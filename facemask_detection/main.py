import detect_mask
import TemperatureSensor
from termcolor import colored, cprint

max_capacity = 2
current_capacity = 0
goodtemp = False
maskon = False

while True:
    maskon = detect_mask.detectmask()
    if maskon == True:
        goodtemp = TemperatureSensor.tempsensor()
    print("")

    if (maskon and goodtemp):
        if (current_capacity==max_capacity):
            cprint("\n##           ##\n ##         ##\n  ##       ##\n   ##     ##\n    ##   ##\n     ## ##\n      ##\n     ## ##\n    ##   ##\n   ##     ##\n  ##       ##\n ##         ##\n##           ##", 'red')
            cprint("\nPlease wait for someone to leave before entering", 'red')
        else:
            cprint("                       ##\n                      ##\n                     ##\n                    ##\n                   ##\n                  ##\n                 ##\n                ##\n               ##\n ##           ##\n  ##         ##\n   ##       ##\n    ##     ##\n     ##   ## \n      ## ##\n       ##", 'green')
            cprint("\nYou are safe to enter", 'green')
            current_capacity += 1
        maskon = False
        goodtemp = False
    else:
        cprint("\n##           ##\n ##         ##\n  ##       ##\n   ##     ##\n    ##   ##\n     ## ##\n      ##\n     ## ##\n    ##   ##\n   ##     ##\n  ##       ##\n ##         ##\n##           ##", 'red')
        cprint("\nYou may not enter", 'red')
        maskon = False
        goodtemp = False

    print("\n")


