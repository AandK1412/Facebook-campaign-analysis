# Enhanced Attendance Management — Facial Recognition with K-NN

A web-based attendance system that marks attendance automatically using facial
recognition. Faces are detected with an OpenCV Haar cascade and identified with
a **K-Nearest Neighbours (K-NN)** classifier trained on registered users.
New users are enrolled through a simple Flask web UI, and attendance is logged
to a daily CSV file.

This project replaces manual roll calls and sign-in sheets, which are
time-consuming, error-prone, and easy to game through proxy attendance. It also
supports contactless, post-pandemic attendance workflows.

## Features

- **Web interface** (Flask + Bootstrap) to view today's attendance and register new users.
- **Face detection** using OpenCV's `haarcascade_frontalface_default.xml`.
- **Face recognition** using a K-NN classifier (`scikit-learn`).
- **Automatic model retraining** whenever a new user is added.
- **Data augmentation** during enrolment: histogram equalisation plus brightened
  and darkened variants of each capture, improving robustness to lighting.
- **Daily attendance logs** written to `Attendance/Attendance-MM_DD_YY.csv`.

## How it works

1. **Register a user** — enter a name and ID. The webcam captures ~10 faces
   (each saved as a normal, brightened, and darkened image). The K-NN model is
   retrained automatically.
2. **Take attendance** — the webcam stream is scanned, each detected face is
   resized to 50×50, flattened, and classified by the K-NN model. Recognised
   users are appended to today's CSV (no duplicates).
3. **View attendance** — the home page lists everyone marked present today and
   the total number of registered users.

User folders are named `Name_Roll` (e.g. `Harsh_52`), which is how the app
derives the name and roll number for each record.

## Project structure

```
facial-recognition-attendance/
├── app.py                      # Main application (Single-face K-NN) — supported version
├── templates/
│   └── home.html               # Web UI
├── static/
│   └── faces/                  # Registered users' captured faces (created at runtime)
├── Attendance/                 # Daily attendance CSV files (created at runtime)
├── experiments/                # Trial code explored during development
│   ├── multi_face_knn.py       # K-NN, marks every face in the frame each pass
│   ├── svm_classifier.py       # SVM attempt (see notes inside)
│   ├── cnn_tensorflow.py       # CNN/TensorFlow attempt (see notes inside)
│   └── README.md
├── requirements.txt
├── requirements-experiments.txt
├── .gitignore
└── LICENSE
```

## Installation

Requires Python 3.8+ and a working webcam.

```bash
git clone https://github.com/AandK1412/facial-recognition-attendance.git
cd facial-recognition-attendance

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

The Haar cascade ships with `opencv-python`, so no separate download is needed.

## Usage

```bash
python app.py
```

Then open <http://127.0.0.1:5000> in your browser.

- **Add New User** — register a face (a webcam window opens; press `Esc` to stop early).
- **Take Attendance** — start recognition (press `Esc` to close the webcam window).

> The OpenCV webcam windows open as native desktop windows, so run this on a
> machine with a display and camera attached (not a headless server).

## Experiments

The `experiments/` folder preserves alternative approaches evaluated during the
project (multi-face K-NN, SVM, and a CNN built with TensorFlow). They are kept
for reference and are **not** the supported path — see `experiments/README.md`
for details and known issues. The CNN variant additionally needs
`pip install -r requirements-experiments.txt`.

## Errors & limitations encountered

- **Failed wheel builds / import errors** — resolved by pinning dependencies and
  using an isolated virtual environment.
- **TensorFlow on i5 hardware** — performance bottlenecks and instruction-set
  incompatibilities made the CNN path impractical on the test machines.
- **Insufficient training data** — the small dataset caused the CNN to overfit
  and generalise poorly, which is part of why K-NN was chosen for the final build.
- **Recognition accuracy** is sensitive to lighting, pose, occlusion, and
  changes in appearance over time.

## Future scope

- Stronger recognition models (deep / transfer learning) robust to lighting,
  pose, and masks.
- Real-time analytics on attendance patterns.
- Multi-modal biometrics (e.g. fingerprint or iris alongside face).
- Integration with LMS / SIS and smart-campus systems.
- Cloud-based, scalable deployment.
- Privacy-by-design: encryption of biometric data, consent, and bias mitigation.

## References

1. A. Kumari Sirivarshitha, K. Sravani, K. S. Priya, and V. Bhavani, "An approach for face detection and face recognition using OpenCV and Face Recognition libraries in Python," *2023 9th International Conference on Advanced Computing and Communication Systems (ICACCS)*, Mar. 2023. doi:10.1109/icaccs57279.2023.10113066
2. X. Yin and X. Liu, "Multi-task convolutional neural network for pose-invariant face recognition," *IEEE Transactions on Image Processing*, vol. 27, no. 2, pp. 964–975, Feb. 2018. doi:10.1109/tip.2017.2765830
3. K.-Y. Chou and Y.-P. Chen, "Real-time and low-memory multi-faces detection system design with naive Bayes classifier implemented on FPGA," *IEEE Transactions on Circuits and Systems for Video Technology*, vol. 30, no. 11, pp. 4380–4389, Nov. 2020. doi:10.1109/tcsvt.2019.2955926
4. R. Ranjan, V. M. Patel, and R. Chellappa, "HyperFace: A deep multi-task learning framework for face detection, landmark localization, pose estimation, and gender recognition," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 41, no. 1, pp. 121–135, Jan. 2019. doi:10.1109/tpami.2017.2781233
5. B.-C. Chen, C.-S. Chen, and W. H. Hsu, "Face recognition and retrieval using cross-age reference coding with cross-age celebrity dataset," *IEEE Transactions on Multimedia*, vol. 17, no. 6, pp. 804–815, Jun. 2015. doi:10.1109/tmm.2015.2420374

## Authors

- Anrunya Patole (L046)
- Harsh Sahu (L052)
- Om Kapdoskar (L063)

NMIMS — Mukesh Patel School of Technology Management & Engineering (MPSTME)

## License

Released under the MIT License. See [LICENSE](LICENSE).
