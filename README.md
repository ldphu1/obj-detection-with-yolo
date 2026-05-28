# Object Detection với YOLOv8 - VIRAT Video Dataset

Tổng quan:
* Bài toán: Nhận diện 3 lớp đối tượng: person, bike, car.

* Dataset: Subset của VIRAT Video Dataset (Góc camera an ninh, đối tượng nhỏ, bối cảnh tĩnh).

* Model: YOLOv8n.

# Setup
Đảm bảo bạn đã cài đặt Python 3.8+ và các thư viện cần thiết:
```
Bash
pip install -r requirements.txt
```

# Hướng dẫn Sử dụng
Bước 1: Chuẩn bị Dữ liệu (Data Preparation)

Script yolo_format.py chịu trách nhiệm đọc video gốc và file annotation (.objects.txt) từ bộ VIRAT, sau đó chuyển đổi sang định dạng YOLO chuẩn.

```
Bash
python yolo_format.py
```
Lưu ý: Thay đổi đường dẫn root và output_path trong hàm main cho phù hợp với máy của bạn.


Bước 2: Huấn luyện Mô hình (Training)

Dự án tiến hành thử nghiệm 3 cấu hình khác nhau để tìm ra phương án tối ưu nhất cho bài toán đối tượng nhỏ. Chạy các lệnh sau trong terminal (hoặc Kaggle/Colab):

1. Baseline_640 (Cơ bản):
Kích thước ảnh 640, thông số mặc định để lấy mốc so sánh.
```
Bash
yolo task=detect mode=train model=yolov8n.pt data=/kaggle/working/data_kaggle.yaml epochs=50 imgsz=640 batch=16 patience=30 hsv_h=0.0 hsv_s=0.0 hsv_v=0.0 device=[0, 1] name=Baseline_640
```

2. HighRes_1280 (Độ phân giải cao):
   
Tăng kích thước ảnh lên 1280 để mô hình không bỏ sót các đối tượng (person, bike) ở quá xa.

```
Bash
yolo task=detect mode=train model=yolov8n.pt data=/kaggle/working/data_kaggle.yaml epochs=50 imgsz=1280 batch=16 patience=30 hsv_h=0.0 hsv_s=0.0 hsv_v=0.0 device=[0, 1] name=HighRes_1280A
```
3. Augmentation_1280 (Tối ưu - Khuyên dùng):
   
Kết hợp kích thước 1280 với Augmentation cực mạnh (Mosaic, Mixup, thay đổi màu sắc) để chống hiện tượng mô hình "học vẹt" bối cảnh tĩnh của camera.

```
Bash
yolo task=detect mode=train model=yolov8n.pt data=/kaggle/working/data_kaggle.yaml epochs=50 imgsz=1280 batch=16 patience=30 device=[0, 1] mosaic=1.0 mixup=0.2 degrees=10.0 hsv_h=0.015 hsv_s=0.4 hsv_v=0.4 name=Augmentation_1280
```
Bước 3: Inference & Tracking

Script infer.py sử dụng trọng số mô hình tốt nhất để nhận diện và theo dõi đối tượng trên video mới. 

```
Bash
python infer.py
📊 Kết quả Đánh giá (Results Summary)
Qua quá trình huấn luyện và phân tích, cấu hình Augmentation_1280 cho kết quả tối ưu nhất với sự cân bằng giữa Precision và Recall, đặc biệt khắc phục được lỗi bỏ sót người ở xa (False Negative) và lỗi nhận diện nhầm bóng đổ/cái cây thành người (False Positive) nhờ kỹ thuật trộn ảnh Mosaic.

Best Model: Augmentation_1280

mAP@50: ~90.65%

Recall: Cao nhất trong 3 cấu hình (đạt 88.21%)
