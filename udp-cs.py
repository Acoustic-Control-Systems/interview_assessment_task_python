# -*- coding: utf-8 -*-

import threading
import time
import json
import csv
import pickle
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import socket
import logging

# DataGenerator class
class DataGenerator:
    def generate_json_meta(self):
        data = {
            "timestamp": time.time(),
            "description": "Meta-information. I am Bharath."
        }
        return json.dumps(data).encode('utf-8')

    def generate_binary_data(self):
        t = np.linspace(0, 1, 1000)
        sine_wave = np.sin(2 * np.pi * 100 * t)  # 100 Hz sine wave
        modulated_wave = sine_wave * np.exp(-5 * t)  # Exponential decay modulation
        return modulated_wave.astype(np.float32).tobytes()

# UDPServer class
class UDPServer:
    def __init__(self, host='localhost', port=12345):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.server_address)
        self.data_generator = DataGenerator()
        logging.basicConfig(level=logging.INFO)

    def start(self):
        logging.info(f"Server listening on {self.server_address}")
        while True:
            try:
                data, address = self.sock.recvfrom(4096)
                request = data.decode('utf-8')
                logging.info(f"Received request: {request} from {address}")

                if request == 'request_json':
                    response = self.data_generator.generate_json_meta()
                elif request == 'request_binary':
                    response = self.data_generator.generate_binary_data()
                else:
                    response = b"Invalid request"

                self.sock.sendto(response, address)
                logging.info(f"Sent response to {address}")

            except Exception as e:
                logging.error(f"Error: {e}")

# UDPClient class
class UDPClient:
    def __init__(self, server_host='localhost', server_port=12345):
        self.server_address = (server_host, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def request_data(self, request_type):
        self.sock.sendto(request_type.encode('utf-8'), self.server_address)
        data, _ = self.sock.recvfrom(4096)  # Increase buffer size to 4096 bytes
        return data

# FileSerializer class
class FileSerializer:
    @staticmethod
    def serialize_json(data, filename):
        with open(filename, 'w') as f:
            f.write(data)

    @staticmethod
    def serialize_binary_csv(data, filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['value'])
            for value in data:
                writer.writerow([value])

    @staticmethod
    def serialize_binary_pickle(data, filename):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

# SignalProcessor class
class SignalProcessor:
    @staticmethod
    def bandpass_filter(data, lowcut, highcut, fs, order=5):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        y = filtfilt(b, a, data)
        return y

    @staticmethod
    def autocorrelation(data):
        return np.correlate(data, data, mode='full')

# Plotter class
class Plotter:
    @staticmethod
    def save_plot(data, filename):
        plt.figure()
        plt.plot(data)
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.savefig(filename)
        plt.close()

# Function to run the server
def run_server():
    server = UDPServer()
    server.start()

# Start the server in a separate thread
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

# Give the server a moment to start
time.sleep(1)

# Initialize the client
client = UDPClient()

# Request JSON data
json_data = client.request_data('request_json')
print("Received JSON Data:", json_data.decode('utf-8'))

# Request binary data
binary_data = client.request_data('request_binary')
binary_values = np.frombuffer(binary_data, dtype=np.float32)

# Serialize data
FileSerializer.serialize_json(json_data.decode('utf-8'), 'meta_info.txt')
FileSerializer.serialize_binary_csv(binary_values, 'binary_data.csv')
FileSerializer.serialize_binary_pickle(binary_values, 'binary_data.pkl')

# Process data
filtered_data = SignalProcessor.bandpass_filter(binary_values, 10, 100, 500)
autocorr_data = SignalProcessor.autocorrelation(filtered_data)

# Plot data
Plotter.save_plot(filtered_data, 'filtered_data.png')
Plotter.save_plot(autocorr_data, 'autocorr_data.png')
