import os
import cv2
import random
from ultralytics import YOLO  # Assurez-vous que YOLOv11 est correctement installé

def extract_random_frames(input_folder, output_folder, model_path):
    images_folder = os.path.join(output_folder, "images")
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    
    labels_folder = os.path.join(output_folder, "labels")
    if not os.path.exists(labels_folder):
        os.makedirs(labels_folder)
    
    # Création du fichier classes.txt
    classes_file = os.path.join(output_folder, "classes.txt")
    with open(classes_file, "w") as f:
        f.write("pedestrians\nbikes\nbicyclists\ne-scooters\ne-scooterists\n")
    
    model = YOLO(model_path)  # Chargement du modèle YOLO
    video_files = [f for f in os.listdir(input_folder) if f.endswith(".mp4")]
    frame_count = 1
    
    for video_file in video_files:
        video_path = os.path.join(input_folder, video_file)
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"Erreur lors de l'ouverture de {video_file}")
            continue
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames == 0:
            print(f"Aucune frame trouvée dans {video_file}")
            cap.release()
            continue
        
        random_frame = random.randint(0, total_frames - 1)
        cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame)
        success, frame = cap.read()
        
        if success:
            frame_filename = f"frame_{frame_count:04d}.jpg"
            frame_path = os.path.join(images_folder, frame_filename)
            cv2.imwrite(frame_path, frame)
            print(f"Frame extraite : {frame_path}")
            
            # Détection avec YOLO
            results = model(frame)
            label_path = os.path.join(labels_folder, f"frame_{frame_count:04d}.txt")
            
            with open(label_path, "w") as f:
                for result in results:
                    for box in result.boxes:
                        class_id = int(box.cls[0])  # Classe détectée
                        x_center, y_center, width, height = box.xywhn[0].tolist()
                        f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
            
            frame_count += 1
        else:
            print(f"Échec de la lecture de la frame dans {video_file}")
        
        cap.release()
    
    print("Extraction et annotation terminées.")

# Exemple d'utilisation
# extract_random_frames("chemin/vers/videos", "chemin/vers/output", "algos/nom_du_modele.pt")
