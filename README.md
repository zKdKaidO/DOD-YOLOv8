# 📄 Document Layout Analysis with YOLOv8 & Streamlit

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![YOLOv8](https://img.shields.io/badge/Model-YOLOv8-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Introduction
This project is an **End-to-End AI Application** designed to automatically analyze and detect document layout structures. 

Built with **YOLOv8** (fine-tuned on the **DocLayNet** dataset) and **Streamlit**, the application allows users to upload document images and instantly identify 11 distinct layout elements such as Headers, Footers, Tables, and Figures.

The system is deployed and accessible via the web, featuring a user-friendly interface with multi-language support.

## 🚀 Live Demo
You can try the application directly here:
👉 **[CLICK HERE TO VIEW DEMO](https://document-image-detection.streamlit.app/)**

## ✨ Key Features
* **Object Detection:** Detects 11 document layout classes: `Caption`, `Footnote`, `Formula`, `List-item`, `Page-footer`, `Page-header`, `Picture`, `Section-header`, `Table`, `Text`, `Title`.
* **Interactive Interface:** Drag-and-drop image upload using Streamlit.
* **Result Visualization:** Draws bounding boxes with confidence scores.
* **Export Feature:** Download the processed image with detected layouts directly.
* **Statistics:** Displays a summary count of detected elements.

## 🛠️ Tech Stack
* **Core AI:** Python, Ultralytics YOLOv8 (Computer Vision).
* **Web Framework:** Streamlit.
* **Image Processing:** OpenCV, PIL (Pillow), NumPy.
* **Deployment:** Streamlit Community Cloud.

## 📸 Screenshots

![App Screenshot](demo.png)

> *Figure 1: The application interface detecting layout elements from a document.*

## ⚙️ Installation & Usage (Local)

If you want to run this project on your local machine, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/zKdKaidO/DOD-YOLOv8.git
cd YourRepoName
py -3.11 -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\activate
pip install streamlit ultralytics pillow opencv-python-headless
streamlit run app.py