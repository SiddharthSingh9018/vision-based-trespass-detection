
# Vision-Based Trespass Detection System

## Overview

This project implements a real-time **vision-based trespass detection system** using computer vision and deep learning.
It processes live video streams, detects motion to reduce unnecessary computation, and applies a human detection model to identify potential trespassing events. When a human presence is detected under defined conditions, the system triggers an alert.

The design emphasizes **modularity, configurability, and runtime efficiency**, rather than end-to-end automation or enterprise deployment.

---

## System Architecture

The pipeline follows a motion-gated detection approach:

```
Video Stream → Motion Detection → Human Detection → Alerting → Display
```

Each stage is implemented as an independent module to enable testing, refactoring, and future extension.

---

## Components Used

* **OpenCV**

  * Video capture
  * Background subtraction (motion detection)
  * Frame annotation and visualization

* **YOLOv8 (Ultralytics)**

  * Lightweight deep-learning model for real-time human detection

* **SMTP (Email Alerts)**

  * Notification mechanism for detected trespassing events

* **Kivy (Optional GUI Tool)**

  * Auxiliary GUI for generating camera configuration files
  * Not part of the detection runtime

---

## Repository Structure

```
vision-based-trespass-detection/
├── src/
│   ├── main.py                # Orchestrates the system
│   ├── config.py              # Centralized configuration
│   ├── detectors/
│   │   ├── motion.py          # Motion detection logic
│   │   └── human.py           # YOLO-based human detection
│   ├── alerts/
│   │   └── email.py           # Email alerting
│   └── utils/
│       └── display.py         # Frame visualization utilities
│
├── scripts/
│   └── gui/
│       └── config_gui.py      # GUI tool for generating camera configs
│
├── data/
│   ├── raw/                   # Runtime camera configuration (ignored)
│   └── data.example.json      # Example configuration
│
├── tests/
│   └── test_motion.py         # Basic test harness
│
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/vision-based-trespass-detection.git
cd vision-based-trespass-detection
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

### Camera Configuration

Runtime camera configuration is read from:

```
data/raw/data.json
```

This file is **not committed**.
Use the provided example as a template:

```
data/data.example.json
```

Or generate it using the GUI tool:

```bash
python scripts/gui/config_gui.py
```

---

## Execution

Run the detection system:

```bash
python src/main.py
```

Press **`q`** to exit the application.

---

## Detection Logic

### 1. Motion Detection

* Background subtraction is used to identify candidate regions
* Motion gating reduces unnecessary deep-learning inference

### 2. Human Detection

* YOLOv8 detects human presence in motion-triggered frames
* Detection thresholds are configurable

### 3. Alerting

* Alerts are rate-limited to avoid repeated notifications
* Email credentials are loaded via environment variables

---

## Design Principles

* **Separation of concerns**
* **Explicit configuration**
* **No hardcoded secrets**
* **Behavior-preserving refactors**
* **Testable components**

---

## Non-Goals

* General-purpose intrusion detection
* Identity recognition or tracking
* Adversarial robustness
* Enterprise-scale deployment

---

## Resource Requirements

* **Memory**: ~200–300 MB (depending on model and stream count)
* **Compute**: Real-time performance on CPU for limited streams; GPU recommended for scale

---

## Status

Stable prototype with modular architecture.
Suitable for systems-oriented evaluation, coursework, or portfolio demonstration.

---
