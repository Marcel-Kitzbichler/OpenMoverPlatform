import serial
import parsekml
import json

def process(port):
    kmlArray = parsekml.parse(input("KML file path? :"))
    kmlArray.insert(0,len(kmlArray)/2)
    speed = float(input("Speed? :"))
    range = float(input("Range? :"))
    kmlArray.insert(1,speed)
    kmlArray.insert(2,range)
    dataToSend = {"intent": 5, "coordinates": kmlArray}
    dataToSend = json.dumps(dataToSend)
    dataToSend = dataToSend.encode('utf-8')
    print("Data to send: ", dataToSend)
    port.write(dataToSend)
    print("Data sent")