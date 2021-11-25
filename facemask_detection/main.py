import detect_mask
import TemperatureSensor

#detect_mask.detectmask()
goodtemp = TemperatureSensor.tempsensor()
maskon = detect_mask.detectmask()

print ("temp good:",goodtemp)
print ("mask good:", maskon)

