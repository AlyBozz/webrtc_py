# libcamera-webrtc-foxglove/libcamera-webrtc-foxglove/README.md

# libcamera WebRTC Streaming to Foxglove

This project provides a WebRTC video streaming solution using a Raspberry Pi camera with the libcamera library. The video stream can be connected to Foxglove for visualization and interaction.

## Project Structure

```
libcamera-webrtc-foxglove
├── src
│   ├── main.py        # Entry point of the application
│   ├── camera.py      # Camera interface with libcamera
│   └── webrtc.py      # WebRTC connection management
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Requirements

To run this project, you need the following:

- Raspberry Pi with a camera module
- Python 3.7 or higher
- Required Python packages listed in `requirements.txt`

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd libcamera-webrtc-foxglove
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. Ensure that the Raspberry Pi camera is enabled in the Raspberry Pi configuration settings.

## Usage

1. Run the application:

   ```
   python src/main.py
   ```

2. Open Foxglove and connect to the WebRTC stream provided by the Raspberry Pi.

## Notes

- Make sure to have the latest version of the libcamera library installed on your Raspberry Pi.
- Adjust the camera settings in `src/camera.py` as needed for your specific use case.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.