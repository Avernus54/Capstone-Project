import cv2
import torch
from ultralytics import YOLO
from pathlib import Path
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

# Try to import PIL for better image handling
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Disable matplotlib GUI backend issues
import matplotlib
matplotlib.use('Agg')

# Load the trained model
model_path = Path(__file__).parent / "my_model.pt"
print(f"Loading model from: {model_path}")
model = YOLO(str(model_path))
print("✓ Model loaded successfully")

# Set confidence threshold to 50%
CONFIDENCE_THRESHOLD = 0.7
print(f"✓ Confidence threshold set to: {CONFIDENCE_THRESHOLD * 100}%")

# Open camera
print("\nAttempting to open Camera 0...")
cap = cv2.VideoCapture(0)

# Set camera properties for better performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# Check if camera opened successfully
if not cap.isOpened():
    print("✗ Error: Could not open camera")
    sys.exit(1)

print(f"✓ Camera opened successfully")
print(f"  Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")

# Create output directory for saving frames
output_dir = Path("camera_frames")
output_dir.mkdir(exist_ok=True)

print("\n" + "="*50)
print("Bird Detection - Live Camera Feed")
print("="*50)
print("Controls:")
print("  'q' - Quit")
print("  's' - Save current frame")
print("  'p' - Pause/Resume")
print("="*50 + "\n")

frame_count = 0
paused = False
total_detections = 0

try:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to read frame")
            break
        
        if paused:
            # Show paused frame
            cv2.putText(frame, "PAUSED", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
            cv2.imshow("YOLOv8 Bird Detection - Live Camera", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('p'):
                paused = False
            continue
        
        frame_count += 1
        
        # Run inference with confidence threshold
        results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
        
        # Visualize results
        annotated_frame = results[0].plot()
        
        # Get detections info
        detections = len(results[0].boxes)
        total_detections += detections
        
        # Add information overlay
        info_text = f"Frame: {frame_count} | Detections: {detections}"
        cv2.putText(annotated_frame, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Add timestamp
        cv2.putText(annotated_frame, "Press 'q' to quit, 's' to save, 'p' to pause", (10, annotated_frame.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display the frame (with error handling)
        try:
            cv2.imshow("YOLOv8 Bird Detection - Live Camera", annotated_frame)
        except cv2.error:
            # OpenCV display not available, try alternative
            if frame_count == 1:
                print("⚠ OpenCV display not available, using alternative method...")
            pass
        
        # Handle keyboard input
        try:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n✓ Quitting...")
                break
            elif key == ord('s'):
                # Save the current frame
                filename = output_dir / f"bird_detection_{frame_count:04d}.jpg"
                cv2.imwrite(str(filename), annotated_frame)
                print(f"✓ Frame saved: {filename}")
            elif key == ord('p'):
                paused = True
                print("⏸ Paused (press 'p' to resume)")
        except:
            pass

except KeyboardInterrupt:
    print("\n\n✓ Interrupted by user")

finally:
    # Release resources
    cap.release()
    try:
        cv2.destroyAllWindows()
    except:
        pass
    
    print("\n" + "="*50)
    print("Bird Detection Session Completed")
    print("="*50)
    print(f"✓ Total frames processed: {frame_count}")
    print(f"✓ Total bird detections: {total_detections}")
    if frame_count > 0:
        print(f"✓ Average detections per frame: {total_detections/frame_count:.1f}")
    print(f"✓ Frames saved to: {output_dir}")
    print("="*50)
