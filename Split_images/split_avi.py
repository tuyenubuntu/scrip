import sys
import cv2
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QMessageBox, QProgressBar, QLineEdit

class ImageSplitterApp(QWidget):
    def __init__(self):
        super().__init__()

        # Thiết lập giao diện
        self.setWindowTitle('Image Splitter from Video')
        self.setGeometry(100, 100, 400, 350)

        self.layout = QVBoxLayout()

        self.label = QLabel('Select the video you want to export as images:')
        self.layout.addWidget(self.label)

        self.button_select_video = QPushButton('Select Video')
        self.button_select_video.clicked.connect(self.select_video)
        self.layout.addWidget(self.button_select_video)

        # Tạo layout ngang cho định dạng và ô nhập số frame skip
        hbox_layout = QHBoxLayout()

        self.label_format = QLabel('Select the image format:')
        hbox_layout.addWidget(self.label_format)

        # ComboBox cho định dạng hình ảnh
        self.format_combo = QComboBox()
        self.format_combo.addItems(['JPG', 'PNG', 'BMP'])
        hbox_layout.addWidget(self.format_combo)

        # Ô nhập cho số frame bỏ qua
        self.label_skip = QLabel('Skip frames:')
        hbox_layout.addWidget(self.label_skip)

        self.skip_input = QLineEdit()
        self.skip_input.setPlaceholderText("3")  # Đặt giá trị mặc định
        self.skip_input.setFixedWidth(50)  # Đặt chiều rộng cố định cho ô nhập
        hbox_layout.addWidget(self.skip_input)

        # Thêm layout ngang vào giao diện chính
        self.layout.addLayout(hbox_layout)

        self.button_split_images = QPushButton('Split Video')
        self.button_split_images.clicked.connect(self.split_images)
        self.button_split_images.setEnabled(False)  # Disabled until a video is selected
        self.layout.addWidget(self.button_split_images)

        # Thêm nút "About"
        self.button_about = QPushButton('About')
        self.button_about.clicked.connect(self.show_about_dialog)
        self.layout.addWidget(self.button_about)

        # Thêm thanh tiến trình
        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()  # Ẩn thanh tiến trình ban đầu
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

        self.video_path = None

    def select_video(self):
        # Mở hộp thoại chọn file
        self.video_path, _ = QFileDialog.getOpenFileName(self, 'Select Video', '', 'Video Files (*.avi *.mp4 *.mov *.mkv)')
        
        if self.video_path:
            QMessageBox.information(self, 'Information', 'Video uploaded successfully!', QMessageBox.Ok)
            self.label.setText(f'Video has been uploaded: {self.video_path}')
            self.button_split_images.setEnabled(True)  # Enable the split button

    def split_images(self):
        if not self.video_path:
            return

        # Lấy giá trị skip từ ô nhập và kiểm tra
        try:
            skip_frames = int(self.skip_input.text()) if self.skip_input.text() else 0
            if skip_frames < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Invalid input for frames to skip. Please enter a positive integer.', QMessageBox.Ok)
            return

        # Hiển thị thanh tiến trình
        self.progress_bar.show()
        
        #Create variable video_name  và vide0_folder
        video_folder = os.path.dirname(self.video_path)
        video_name = os.path.basename(self.video_path).split('.')[0]

        # Tạo thư mục để lưu hình ảnh
        #output_dir = os.path.splitext(self.video_path)[0] + '_frames'
        output_dir = os.path.join(video_folder, f'{video_folder}_{video_name}')
        os.makedirs(output_dir, exist_ok=True)

        # Đọc video
        video_capture = cv2.VideoCapture(self.video_path)

        # Kiểm tra xem video có mở thành công không
        if not video_capture.isOpened():
            QMessageBox.warning(self, 'Error', 'Cannot open video.', QMessageBox.Ok)
            return
        
        QMessageBox.information(self, 'Information', 'Processing video, please wait...', QMessageBox.Ok)

        frame_count = 0
        saved_count = 0
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        # Lấy định dạng hình ảnh từ ComboBox
        selected_format = self.format_combo.currentText().lower()
        extension = {
            'jpg': 'jpg',
            'png': 'png',
            'bmp': 'bmp'
        }[selected_format]

        self.progress_bar.setMaximum(total_frames)

        # Lấy tên cơ bản của video
        video_name = os.path.basename(self.video_path).split('.')[0]

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            # Bỏ qua số frame theo giá trị nhập
            if frame_count % (skip_frames + 1) == 0:
                # Lưu hình ảnh
                #frame_filename = os.path.join(output_dir, f'{video_name}_frame_{frame_count:04d}.{extension}')
                frame_filename = os.path.join(output_dir, f'{os.path.basename(video_folder)}_{video_name}_frame_{frame_count:04d}.{extension}')
                cv2.imwrite(frame_filename, frame)
                saved_count += 1

            frame_count += 1

            # Cập nhật thanh tiến trình
            self.progress_bar.setValue(frame_count)
        
        video_capture.release()

        # Hiển thị thông báo hoàn thành
        QMessageBox.information(self, 'Success', f'Finished splitting {saved_count} images and saved to: {output_dir}', QMessageBox.Ok)
        self.progress_bar.setValue(0)  # Reset thanh tiến trình
        self.progress_bar.hide()  # Ẩn thanh tiến trình sau khi hoàn thành

    def show_about_dialog(self):
        about_text = (
            "Version 1.2\n"
            "Copyright belongs to: Truong Thanh Tuyen"
        )
        QMessageBox.about(self, "About Image Splitter", about_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageSplitterApp()
    window.show()
    sys.exit(app.exec_())
