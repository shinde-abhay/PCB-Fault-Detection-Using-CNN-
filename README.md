# 🛠️ PCB Defect Detection System

An AI-powered PCB defect detection application built using a YOLO deep learning model and a custom Tkinter GUI. It automatically identifies faults such as **short circuits**, highlights them on the image, and provides defect descriptions with recommended remedies.

---

## 📌 1. Project Title / Headline
**PCB Defect Detection – Deep Learning Based Fault Identification**

A real-time PCB defect detection interface that enables users to upload PCB images and instantly view detected defects with bounding boxes and confidence scores.

---

## 📌 2. Short Description / Purpose
This project is designed to detect surface-level PCB manufacturing defects using a trained YOLO model. The desktop application provides real-time visualization, defect classification, and actionable suggestions to support electronics engineers, QA teams, and manufacturing units.

---

## 📌 3. Tech Stack

The system is built using:

- 🧠 **YOLOv8 / Ultralytics** – Deep learning model for defect detection  
- 🐍 **Python** – Core development language  
- 🖼️ **Tkinter** – GUI for image uploading and visualization  
- 🧩 **Pillow (PIL)** – Image processing  
- 🔢 **NumPy** – Array manipulation  
- 🧱 **OpenCV** – (Optional) Preprocessing and annotation  
- 📁 **Model Format:** `.pt` (YOLO trained weights)  

---

## 📌 4. Dataset & Training

### **Dataset Used**
A collection of PCB images with defects such as:
- **Short circuits**
- (Optional: Missing holes, Mousebite, Over-etching, Spurious copper)**  
*(Your trained model currently works for "short" defects)*

### **Training Details**
- Model: YOLOv8  
- Epochs: 50–100 (depending on your final training run)  
- Image size: 640x640  
- Annotation tool: Roboflow / CVAT / LabelImg  
- Export: YOLO format  

---

## 📌 5. Features / Highlights

### 🔹 **Business Problem**
Manual PCB inspection is slow, inconsistent, and prone to human error.  
Industries struggle with:
- Detecting micro-defects  
- Maintaining inspection consistency  
- High labor cost for visual checks  
- Reducing PCB rejection rate  

### 🔹 **Goal of the Application**
To build a lightweight, automated, and accurate system that:
- Detects PCB defects in real-time  
- Visually highlights defect locations  
- Provides confidence levels  
- Displays explanation + remedy for each defect  
- Works offline using a desktop UI  

---

## 🔹 **Walkthrough of Key Features**

### **1. Upload Image Panel**
Users can upload any PCB image using the **Upload Image** button.  
The uploaded image is displayed clearly on the left side.

---

### **2. YOLO Detection Result (Right Image Panel)**
- Detected defects are shown with bounding boxes  
- Each box includes:
  - Defect name (e.g., *short*)  
  - Confidence score (e.g., *0.81*)  

---

### **3. Defect Analysis Sidebar**
For every detected defect, you see:
- Type: **short**  
- Confidence %  
- Description:  
  - “Unintended connection between two conductors.”  
- Remedy:  
  - “Cut the bridging material or use desoldering tools to separate.”  

---

### **4. Real-time Detection Status**
Status updates such as:
- *Image loaded. Detecting...*  
- *5 defect(s) detected.*  

---

### **5. Clear Button**
Resets the interface and prepares the app for new image processing.

---

## 📌 6. Business Impact & Insights

- ⏱ **Faster PCB Inspection:** Cuts inspection time drastically  
- 🎯 **Higher Accuracy:** Model-based detection reduces human error  
- 🧪 **Quality Assurance:** Ensures consistent PCB manufacturing quality  
- 💰 **Cost Savings:** Early detection reduces product rejection and rework  
- ⚙️ **Scalable:** Can be extended to detect multiple types of PCB defects  
- 🛠 **Useful for:** Electronics production units, PCB manufacturers, R&D labs, repair technicians  

---

## 📌 7. GUI Preview

### Application Screenshot
![PCB Defect Detection](PCB%20Defect%20Detection.png)

*(Place your project screenshot inside your GitHub repo as shown above.)*

---

## 📌 8. How to Run the Project

### **1. Install Dependencies**
```bash
pip install ultralytics pillow numpy opencv-python tkinter
