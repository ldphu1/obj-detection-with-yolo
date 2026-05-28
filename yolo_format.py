import cv2
import os
import glob
import random

def write_frame(video_path, image_folder_path):
    os.makedirs(image_folder_path, exist_ok=True)
    frame_count = 0
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        flag, frame = cap.read()
        if not flag:
            break
        if frame_count % 10 == 0:
            cv2.imwrite(os.path.join(image_folder_path, f"frame{frame_count}.jpg"), frame)
        frame_count += 1

def write_txt(txt_path, label_folder_path, WIDTH, HEIGHT):
    os.makedirs(label_folder_path, exist_ok=True)

    with open(txt_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(" ")
            line = list(map(int, line))

            obj = line[7]
            obj = 1 if obj == 4 else obj
            obj = 3 if obj == 5 else obj

            obj -= 1

            x_top, y_top, box_width, box_height = line[3:7]
            x_center = x_top + box_width / 2.0
            y_center = y_top + box_height / 2.0

            x_center_norm = x_center / WIDTH
            y_center_norm = y_center / HEIGHT
            width_norm = box_width / WIDTH
            height_norm = box_height / HEIGHT

            x_center_norm = min(max(x_center_norm, 0), 1)
            y_center_norm = min(max(y_center_norm, 0), 1)
            width_norm = min(max(width_norm, 0), 1)
            height_norm = min(max(height_norm, 0), 1)

            frame = line[2]

            if frame % 10 == 0:
                output_txt_path = os.path.join(label_folder_path, f"frame{frame}.txt")
                with open(output_txt_path, "a") as f:
                    f.write(f"{obj} {x_center_norm:.6f} {y_center_norm:.6f} {width_norm:.6f} {height_norm:.6f}\n")

def virat(root, output_path, split_ratio, WIDTH, HEIGHT):
    print("extracting")

    output_dirs = [
        os.path.join(output_path, "images", "train"),
        os.path.join(output_path, "images", "val"),
        os.path.join(output_path, "labels", "train"),
        os.path.join(output_path, "labels", "val"),
    ]

    for dir in output_dirs:
        os.makedirs(dir, exist_ok=True)

    txt_files = glob.glob(os.path.join(root, "annotations", "*.objects.txt"))
    random.seed(42)
    random.shuffle(txt_files)

    train_size = int(len(txt_files) * split_ratio)
    subset = {
        "train": txt_files[:train_size],
        "val": txt_files[train_size:]
    }

    for subset_name, subset_file in subset.items():
        for txt_file in subset_file:
            video_name = os.path.splitext(os.path.basename(txt_file))[0].split(".")[0]

            image_folder_path = os.path.join(output_path, "images", subset_name, video_name)
            label_folder_path = os.path.join(output_path, "labels", subset_name, video_name)

            video_path = os.path.join(root, "video_original", f"{video_name}.mp4")
            write_frame(video_path, image_folder_path)

            write_txt(txt_file, label_folder_path, WIDTH, HEIGHT)

if __name__ == "__main__":
    output = r"virat"
    virat(r"VIRAT_Ground_Dataset", output, split_ratio=0.8, WIDTH=1920.0, HEIGHT=1080.0)
    print("done")