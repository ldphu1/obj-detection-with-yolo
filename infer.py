import cv2
from ultralytics import YOLO

def draw_fancy_bbox(frame, box, label, score, color):
    x1, y1, x2, y2 = box

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    text = f"{label} | {score:.2f}"
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 0.6
    thickness = 1

    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    if y1 - text_h - 10 < 0:
        back_y1, back_y2 = y1, y1 + text_h + 10
        text_y = y1 + text_h + 5
    else:
        back_y1, back_y2 = y1 - text_h - 10, y1
        text_y = y1 - 7

    cv2.rectangle(frame, (x1, back_y1), (x1 + text_w + 10, back_y2), color, -1)

    cv2.putText(frame, text, (x1 + 5, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

def process_video(model_path, video_path, output_path):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Lỗi: Không thể mở video tại đường dẫn '{video_path}'")
        return

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_path, fourcc, 24.0, (int(width), int(height)))

    while cap.isOpened():
        flag, frame = cap.read()
        if not flag:
            break
        result = model.track(frame, persist=True, verbose=False, conf=0.6)[0]
        annotated_frame = frame.copy()

        if result.boxes is not None and result.boxes.id is not None:
            boxes_xyxy = result.boxes.xyxy.cpu()
            scores = result.boxes.conf.cpu()
            classes = result.boxes.cls.cpu()

            #bbox
            for box_xy, score, cls in zip(boxes_xyxy, scores, classes):
                x1, y1, x2, y2 = map(int, box_xy)
                label = f"{model.names[int(cls)]}"
                draw_fancy_bbox(annotated_frame, (x1, y1, x2, y2), label, float(score), (0, 255, 0))

        out.write(annotated_frame)
        cv2.imshow("frame", annotated_frame)
        cv2.waitKey(1)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    MODEL_WEIGHTS = r"weights\best_Agu_1280.pt"
    INPUT_VIDEO = r"data\test.mp4"
    OUTPUT_VIDEO = "test.mp4"

    process_video(MODEL_WEIGHTS, INPUT_VIDEO, OUTPUT_VIDEO)
