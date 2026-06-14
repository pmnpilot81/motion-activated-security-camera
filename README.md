# Motion Activated Security Camera

A real-time security camera system built with Python and OpenCV.

The application automatically detects faces and human bodies from a webcam feed and records video whenever motion is detected.

## Features

- Real-time face detection
- Full-body detection
- Automatic video recording
- Motion-triggered recording
- Recording timeout system
- Event logging
- MP4 video export
- Bounding boxes around detected objects
- Live monitoring dashboard

## Technologies

- Python
- OpenCV
- Haar Cascade Classifiers

## Project Structure

```text
project/
│
├── security_camera.py
├── recordings/
├── logs/
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python security_camera.py
```

## Output

Detected events are:

- Saved as MP4 files inside recordings/
- Logged inside logs/events.log

## Future Improvements

- YOLOv8 object detection
- Email alerts
- Telegram notifications
- Cloud storage integration
- Multi-camera support
- Motion heatmaps

## Author

Peyman