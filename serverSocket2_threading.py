from speedOfSoundCalculator import CalculateSpeedOfSound
import socketserver
import threading
import math
import json
import csv

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        parsed_data = self.request.recv(1024).decode('utf-8')
        data = json.loads(parsed_data)
        if data is not None:
            if "GET" in data:
                actionOnLeds = self.server.decideOverDistance()
                response = str(actionOnLeds).encode('utf-8') + b'\n'
                self.request.sendall(response)
            elif "TEST" in data:
                self.server.startRecordingData = 1
                self.server.shouldBeThisDistance = data['distance']
                
            elif "GETD" in data:
                computedDistance = self.server.computeDistance()
                response = str(computedDistance).encode('utf-8') + b'\n'
                with open("recorded_distances.csv", "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([computedDistance, "Distancia a la que se prende el led de este rango"])
            elif "SET" in data:
                self.server.elapsed_time = data['time']
                if data['temperature'] is not None:
                    self.server.temperature = data['temperature']
                else:
                    self.server.temperature = 20
                if data['humidity'] is not None:
                    self.server.humidity = data['humidity']
                else:
                    self.server.humidity = 0
                if(self.server.startRecordingData == 1):
                    self.server.recordData()         
                    
class MyServer(socketserver.ThreadingTCPServer):
    def __init__(self, server_address, handler_class):
        super().__init__(server_address, handler_class)
        self.elapsed_time = 0
        self.temperature = 0
        self.humidity = 0
        self.numberOfLeds = 6
        self.startRecordingData = 0
        self.desiredAmountOfRecordedData = 10
        self.recordedData = {}
        self.recordCounter = 0
        self.shouldBeThisDistance = 0
        self.recordedDistances = []
    def computeDistance(self):
        computer = CalculateSpeedOfSound(self.temperature, self.humidity)
        computedSpeedOfSound = computer.calculate_speed_of_sound()
        distance = computedSpeedOfSound * self.elapsed_time * 0.0001 * 0.5
        return distance
    def decideOverDistance(self):
        distance = self.computeDistance()
        thresholds = [30, 25, 20, 15, 10, 5, 0]
        for i in range(len(thresholds)):
            if distance > thresholds[i]:
                return "0" * (6 - i) + "1" * i
        return "111111"
    def recordData(self):
        if(self.recordCounter < self.desiredAmountOfRecordedData):
            self.recordCounter = self.recordCounter + 1
            self.recordedDistances.append([self.computeDistance(), self.shouldBeThisDistance])
        elif (self.recordCounter == self.desiredAmountOfRecordedData):
            self.startRecordingData = 0
            self.recordCounter = 0
            with open("recorded_distances.csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                for i in range(len(self.recordedDistances)):
                    writer.writerow(self.recordedDistances[i])
            self.recordedDistances = []

if __name__ == "__main__":
    SERVER_ADDRESS = "192.168.123.247"
    SERVER_PORT = 1000
    server = MyServer((SERVER_ADDRESS, SERVER_PORT), MyTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True 
    server_thread.start()
    try:
        while True:
            pass 
    except KeyboardInterrupt:
        print("Se cerró el server.")
        server.shutdown()