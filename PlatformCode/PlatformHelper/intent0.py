import serial
import parsekml
import json

def process(port):
    kmlArray = parsekml.parse(input("KML file path? :"))
    kmlArray.insert(0,len(kmlArray))
    dataToSend = {"intent": 0, "coordinates": kmlArray}
    dataToSend = json.dumps(dataToSend)
    dataToSend = dataToSend.encode('utf-8')
    print("Data to send: ", dataToSend)
    port.write(dataToSend)
    print("Data sent")