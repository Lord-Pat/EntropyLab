import cv2
import time

STREAM_URL = "http://192.168.32.207/video"

print("Conectando al stream...")
cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("Error: no se puede conectar al stream")
    exit()

print("Conectado. Capturando frames...")

frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error leyendo frame")
        break
    
    frame_count += 1
    elapsed = time.time() - start_time
    fps = frame_count / elapsed
    
    print(f"Frame {frame_count} | FPS: {fps:.2f} | Tamaño: {frame.shape}")
    
    # Paramos después de 20 frames para ver el resultado
    if frame_count >= 20:
        break

cap.release()
print(f"\nMedia final: {fps:.2f} FPS")
