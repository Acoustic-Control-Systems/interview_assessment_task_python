# Task: UDP Client-Server Application with OOP
## Server Implementation

Description: Implement a UDP server that generates and sends either JSON meta-information or binary modulated sine wave data upon request.

Server Requirements:

- Class-based implementation.
- JSON meta-information includes timestamp and some descriptive text.
- Binary data is a modulated sine wave.
- Listen for different requests from the client for JSON or binary data.

Server Classes:

- UDPServer: Handles receiving requests and sending responses.
- DataGenerator: Generates JSON meta-information and binary sine wave data.

## Client Implementation

Description: Implement a UDP client that requests and receives data from the server, serializes it into files, performs signal processing on binary data, and saves the processed data into PNG files.

Client Requirements:

- Class-based implementation.
- Serialize JSON data into a text file.
- Serialize binary data into a CSV or pickle file based on input parameters.
- Perform signal processing (band-filter and autocorrelation) on binary data.
- Save processed data into a PNG file with XY axes.

Client Classes:

- UDPClient: Handles sending requests and receiving responses from the server.
- FileSerializer: Serializes data into files (JSON, CSV, or pickle).
- SignalProcessor: Performs signal processing (band-filter and autocorrelation).
- Plotter: Saves processed data into PNG files.

## Instructions for the Candidate:

1. Implement the UDP server and client using the class-based structure provided above.
2. Test the server and client to ensure they communicate correctly and handle the requests as expected.
3. Ensure that the client can correctly serialize the received data and perform the required signal processing operations.
4. Submit your scripts along with any test files you used and the generated output files (e.g., meta_info.txt, binary_data.csv, processed_data.png).
5. Push your entire codebase to the provided GitHub repository. Make sure your commit messages are clear and descriptive.
