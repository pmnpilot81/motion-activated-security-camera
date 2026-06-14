import cv2
import time
import datetime
import os


class SecurityCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        self.body_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_fullbody.xml"
        )

        self.detection = False
        self.timer_started = False
        self.detection_stopped_time = None

        self.SECONDS_TO_RECORD_AFTER_DETECTION = 60

        os.makedirs("recordings", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        self.frame_size = (
            int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )

        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out = None

    def write_log(self, message):
        with open("logs/events.log", "a", encoding="utf-8") as log:
            timestamp = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            log.write(f"[{timestamp}] {message}\n")

    def start_recording(self):
        self.detection = True
        self.timer_started = False

        current_time = datetime.datetime.now().strftime(
            "%d-%m-%Y-%H-%M-%S"
        )

        filename = f"recordings/{current_time}.mp4"

        self.out = cv2.VideoWriter(
            filename,
            self.fourcc,
            20,
            self.frame_size
        )

        print(f"Recording started: {filename}")
        self.write_log(f"Recording started -> {filename}")

    def stop_recording(self):
        self.detection = False
        self.timer_started = False

        if self.out:
            self.out.release()
            self.out = None

        print("Recording stopped")
        self.write_log("Recording stopped")

    def run(self):

        while True:

            success, frame = self.cap.read()

            if not success:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5
            )

            bodies = self.body_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5
            )

            # Draw face boxes
            for (x, y, w, h) in faces:
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    "Face",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

            # Draw body boxes
            for (x, y, w, h) in bodies:
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (255, 0, 0),
                    2
                )

                cv2.putText(
                    frame,
                    "Body",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2
                )

            detections = len(faces) + len(bodies)

            if detections > 0:

                if not self.detection:
                    self.start_recording()

            else:

                if self.detection:

                    if not self.timer_started:
                        self.timer_started = True
                        self.detection_stopped_time = time.time()

                    elif (
                        time.time() -
                        self.detection_stopped_time
                    ) >= self.SECONDS_TO_RECORD_AFTER_DETECTION:

                        self.stop_recording()

            if self.detection and self.out:
                self.out.write(frame)

            status = (
                "RECORDING"
                if self.detection
                else "MONITORING"
            )

            cv2.putText(
                frame,
                status,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                f"Detections: {detections}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                "Motion Activated Security Camera",
                frame
            )

            if cv2.waitKey(1) == ord("q"):
                break

        self.cleanup()

    def cleanup(self):

        if self.out:
            self.out.release()

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    camera = SecurityCamera()
    camera.run()