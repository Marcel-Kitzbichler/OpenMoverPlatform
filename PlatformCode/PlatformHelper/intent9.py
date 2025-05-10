import serial
import parsekml
import json
import sys

def process(port):
    #send intent 9 to the bot every 1 second and log the data received from the bot into a json file after the user stops the logging without timestamp
    #get the file name from the user
    file_name = input("File name? :")
    #open the file in write mode
    dataReceived = []
    while True:
        #send intent 9 to the bot
        dataToSend = {"intent": 9}
        dataToSend = json.dumps(dataToSend)
        dataToSend = dataToSend.encode('utf-8')
        port.write(dataToSend)
        #read the data from the bot
        data = port.readline()
        #decode the data
        data = data.decode('utf-8')
        #parse json from data
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print("Error decoding JSON")
            continue
        #check if the data is not empty
        if data:
            #append the data to the list
            dataReceived.append(data)
            #print the data
            print(data)
        #turn the data into a json object string and write it to the file
        dataJson = json.dumps(dataReceived)
        #write the data to the file
        with open(file_name, 'w') as f:
            f.write(dataJson)

