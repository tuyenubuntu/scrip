import sys
import pandas as pd
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout,
    QHBoxLayout, QGridLayout, QTableView, QFileDialog, QHeaderView,
    QComboBox, QSlider, QAbstractItemView
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import QItemSelectionModel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.df = None
        self.selectedFilter = "-- No filter --"
        self.startFrame = None
        self.endFrame = None
        self.steps = None
        self.logfilePath = None  # Lưu đường dẫn đến file log
        self.initUI()

        self.errorMessagesTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.errorMessagesTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        #self.errorMessagesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Ngăn không cho chỉnh sửa trực tiếp
        self.errorMessagesTable.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Cho phép chọn nhiều ô
        self.errorMessagesTable.setDragEnabled(True)
        self.errorMessagesTable.setAcceptDrops(True)
        self.errorMessagesTable.setDragDropMode(QAbstractItemView.InternalMove)

        # Bổ sung quyền chọn nhiều dòng và cột để sao chép
        self.errorMessagesTable.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.errorMessagesTable.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def initUI(self):

        self.loadLogButton = QPushButton('Load Logfile', self)
        self.printErrorButton = QPushButton('Print Error Messages', self)
        self.exportButton = QPushButton('Export to .xlsx', self)  # Nút để xuất dữ liệu
        #Add check box
        # Thêm vào initUI sau nút exportButton
        self.exportAllCheckbox = QCheckBox('Export all', self)
        self.exportCommentedCheckbox = QCheckBox('Only errors that have been commented', self)
        #add clear status button
        self.clearStatusButton = QPushButton("Clear Status", self)
        self.clearStatusButton.clicked.connect(self.clear_status)

        self.messageFilter = QComboBox(self)
        self.messageFilter.addItems([
            "-- No filter --",
            "Not passed Laser",
            "No laser completed signal",
            "Belt chưa kiểm tra endplay",
            "Belt lạ phát hiện trên hook"
        ])
        self.messageFilter.currentIndexChanged.connect(self.updateSelection)

        self.statusLabel = QLabel('No file selected', self)
        self.statusLabel.setStyleSheet("font-size: 10px; color: gray;")

        self.errorMessagesLabel = QLabel('Error Messages', self)
        self.errorMessagesTable = QTableView(self)
        self.errorMessagesTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.errorMessagesTable.setMinimumHeight(200)
        self.errorMessagesTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.errorMessagesTable.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)

        self.evaluationLabel = QLabel('Evaluation', self)
        self.startFrameLabel = QLabel('Startframe', self)
        self.startFrameInput = QLineEdit(self)
        
        self.endFrameLabel = QLabel('Endframe', self)
        self.endFrameInput = QLineEdit(self)

        self.stepsLabel = QLabel('Steps', self)
        self.stepsInput = QLineEdit(self)
        
        self.inputStatusLabel = QLabel('Inputs for plotting:', self)

        self.startEvaluationButton = QPushButton('Start Evaluation', self)

        # Bố trí giao diện
        
        # Create a horizontal layout for the status label and clear status button
        statusLayout = QHBoxLayout()
        statusLayout.addWidget(self.statusLabel)
        statusLayout.addStretch()  # Add stretchable space to push the button to the right
        statusLayout.addWidget(self.clearStatusButton)
        
        
        mainLayout = QVBoxLayout()
        topButtonLayout = QVBoxLayout()
        buttonRowLayout = QHBoxLayout()
        buttonRowLayout.addWidget(self.loadLogButton)
        buttonRowLayout.addWidget(self.messageFilter)
        buttonRowLayout.addWidget(self.printErrorButton)
        buttonRowLayout.addWidget(self.exportButton)  # Thêm nút xuất dữ liệu
        buttonRowLayout.addWidget(self.exportAllCheckbox)
        buttonRowLayout.addWidget(self.exportCommentedCheckbox)
        topButtonLayout.addLayout(buttonRowLayout)
        topButtonLayout.addWidget(self.statusLabel)
        #add layout clear status button
        '''buttonRowLayout.addWidget(self.clearStatusButton)'''
        topButtonLayout.addLayout(statusLayout)


        mainLayout.addLayout(topButtonLayout)
        mainLayout.addWidget(self.errorMessagesLabel)
        mainLayout.addWidget(self.errorMessagesTable)
        mainLayout.addWidget(self.evaluationLabel)
        mainLayout.addWidget(self.inputStatusLabel)

        evaluationLayout = QGridLayout()
        evaluationLayout.addWidget(self.startFrameLabel, 0, 0)
        evaluationLayout.addWidget(self.startFrameInput, 0, 1)
        evaluationLayout.addWidget(self.endFrameLabel, 0, 2)
        evaluationLayout.addWidget(self.endFrameInput, 0, 3)
        evaluationLayout.addWidget(self.stepsLabel, 0, 4)
        evaluationLayout.addWidget(self.stepsInput, 0, 5)
        evaluationLayout.addWidget(self.startEvaluationButton, 0, 6)

        mainLayout.addLayout(evaluationLayout)

        self.setLayout(mainLayout)

        # Kết nối các nút với chức năng tương ứng
        self.loadLogButton.clicked.connect(self.load_logfile)
        self.printErrorButton.clicked.connect(self.print_error_messages)
        self.exportButton.clicked.connect(self.export_to_excel)
        self.startEvaluationButton.clicked.connect(self.start_evaluation)
        
        # Kết nối các ô nhập liệu
        self.startFrameInput.textChanged.connect(self.updateStartFrame)
        self.endFrameInput.textChanged.connect(self.updateEndFrame)
        self.stepsInput.textChanged.connect(self.updateSteps)

        self.setWindowTitle('Logfile Evaluation Tool')
        self.setGeometry(100, 100, 1000, 600)
        self.show()

    def load_logfile(self):
        self.clear_status()
        
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Open CSV File",
            "",
            "CSV Files (*.csv)",
            options=options
        )
        
        if filePath:
            try:
                self.statusLabel.setText("Please wait...")
                self.statusLabel.setStyleSheet("color: black;")
                QApplication.processEvents()
                self.df = pd.read_csv(
                    filePath,
                    delimiter=";",
                    on_bad_lines='skip',
                    low_memory=False
                )
                self.df.columns = ['Timestamp', 'Detections', 'Objects', 'Messages', 'Centroids']
                self.df = self.df.fillna('none')
                self.statusLabel.setText("Loading successful")
                self.statusLabel.setStyleSheet("color: green;")
                self.logfilePath = filePath  # Lưu đường dẫn file log
            except Exception as e:
                print(e)
                self.statusLabel.setText("Error when loading the file")
                self.statusLabel.setStyleSheet("color: red;")

    def print_error_messages(self):
        try:
            QApplication.processEvents()
            # Lọc thông báo lỗi
            if self.selectedFilter == "-- No filter --":
                filteredMessages = self.df[self.df['Messages'] != 'none']
            else:
                filteredMessages = self.df[self.df['Messages'].str.contains(self.selectedFilter, na=False)]

            DictErrorMessages = []

            # Điền dữ liệu vào từ điển với Messages, Timestamp và Frame Number
            lastErrorPosition = None
            for index, row in filteredMessages.iterrows():
                if lastErrorPosition is None or index - lastErrorPosition > 250:
                    newRow = {
                        'Messages': row['Messages'],
                        'Timestamp': row['Timestamp'],
                        'Frame Number': index,
                        'Comment': '',
                        'Slutions': ''  # Thêm cột "Slutions"
                    }
                    DictErrorMessages.append(newRow)
                    lastErrorPosition = index
            
            dfErrorMessages = pd.DataFrame(DictErrorMessages)

            if not dfErrorMessages.empty:
                # Tạo mô hình với cột Comment có thể chỉnh sửa
                model = QStandardItemModel(dfErrorMessages.shape[0], dfErrorMessages.shape[1])
                model.setHorizontalHeaderLabels(['Messages', 'Timestamp', 'Frame Number', 'Comment', 'Slutions'])
                for row in range(dfErrorMessages.shape[0]):
                    for column in range(dfErrorMessages.shape[1]):
                        item = QStandardItem(str(dfErrorMessages.iloc[row, column]))
                        if column in [dfErrorMessages.columns.get_loc('Comment'), dfErrorMessages.columns.get_loc('Slutions')]:
                            item.setEditable(True)
                        else:
                            item.setEditable(False)
                        model.setItem(row, column, item)
                self.errorMessagesTable.setModel(model)
            else:
                self.statusLabel.setText("No Errors found")
                self.statusLabel.setStyleSheet("color: red;")
        except Exception as e:
            print(e)
            self.statusLabel.setText("Error when loading the file")
            self.statusLabel.setStyleSheet("color: red;")

    def clear_status(self):
        self.statusLabel.setText("")
        self.statusLabel.setStyleSheet("")


    def export_to_excel(self):
        #update status
        self.clear_status()
        
        if self.df is None:
            self.statusLabel.setText("No data to export")
            self.statusLabel.setStyleSheet("color: red;")
            return
        try:
            # Thu thập dữ liệu từ mô hình bảng
            data = []
            model = self.errorMessagesTable.model()
            if model is None:
                self.statusLabel.setText("No errors to export")
                self.statusLabel.setStyleSheet("color: red;")
                return
            for row in range(model.rowCount()):
                rowData = []
                for column in range(model.columnCount()):
                    index = model.index(row, column)
                    rowData.append(model.data(index))
                #condition for export, "Export all" or "Only errors that have been commented"
                if self.exportCommentedCheckbox.isChecked():
                    if rowData[3]:
                        data.append(rowData)
                else:
                    data.append(rowData)
            # Tạo DataFrame
            dfExport = pd.DataFrame(data, columns=['Messages', 'Timestamp', 'Frame Number', 'Comment', 'Slutions'])
            # Tạo tên file xuất dựa trên tên file log và tên thư mục chứa log file
            if self.logfilePath:
                dir_path = os.path.dirname(self.logfilePath)
                dir_name = os.path.basename(dir_path)
                baseName = os.path.splitext(os.path.basename(self.logfilePath))[0]
                exportFileName = f"{baseName}_{dir_name}.xlsx"
                exportFilePath = os.path.join(dir_path, exportFileName)
            else:
                exportFileName = 'errors.xlsx'
                exportFilePath = exportFileName
            # Lưu vào Excel
            dfExport.to_excel(exportFilePath, index=False)
            self.statusLabel.setText(f"Exported to {exportFilePath}")
            self.statusLabel.setStyleSheet("color: green;")
        except Exception as e:
            print(e)
            self.statusLabel.setText("Error exporting to Excel")
            self.statusLabel.setStyleSheet("color: red;")

    def start_evaluation(self):
        try:
            # Kiểm tra đầu vào không hợp lệ
            if (
                (self.df is None) or
                (self.startFrame is None) or
                (self.endFrame is None) or
                (self.steps is None) or
                not (0 <= self.startFrame < self.endFrame) or
                not (self.startFrame < self.endFrame < self.df.shape[0]) or
                not (0 < self.steps <= (self.endFrame - self.startFrame))
            ):
                raise Exception
            self.inputStatusLabel.setText("Inputs for plotting:")
            self.inputStatusLabel.setStyleSheet("color: black;")
            self.plot_window = PlotWindow(self.df, self.startFrame, self.endFrame, self.steps)
            self.plot_window.show()          
        except Exception as e:
            # print(e)
            self.inputStatusLabel.setText("Invalid Input - Check the values:")
            self.inputStatusLabel.setStyleSheet("color: red;")

    def updateSelection(self):
        self.selectedFilter = self.messageFilter.currentText()
    
    def updateStartFrame(self):
        try:
            if self.startFrameInput.text() != '':
                self.startFrame = int(self.startFrameInput.text())
            self.inputStatusLabel.setText("Inputs for plotting:")
            self.inputStatusLabel.setStyleSheet("color: black;")                
        except Exception as e:
            # print(e)
            self.inputStatusLabel.setText("Invalid Input:")
            self.inputStatusLabel.setStyleSheet("color: red;")

    def updateEndFrame(self):
        try:
            if self.endFrameInput.text() != '':
                self.endFrame = int(self.endFrameInput.text())
            self.inputStatusLabel.setText("Inputs for plotting:")
            self.inputStatusLabel.setStyleSheet("color: black;")
        except Exception as e:
            # print(e)
            self.inputStatusLabel.setText("Invalid Input:")
            self.inputStatusLabel.setStyleSheet("color: red;")

    def updateSteps(self):
        try:
            if self.stepsInput.text() != '':
                self.steps = int(self.stepsInput.text())
            self.inputStatusLabel.setText("Inputs for plotting:")
            self.inputStatusLabel.setStyleSheet("color: black;")
        except Exception as e:
            # print(e)
            self.inputStatusLabel.setText("Invalid Input:")
            self.inputStatusLabel.setStyleSheet("color: red;")

class PlotWindow(QWidget):
    def __init__(self, df, start_frame, end_frame, steps):
        super().__init__()
        self.df = df
        self.startFrame = start_frame
        self.endFrame = end_frame
        self.steps = steps

        self.setWindowTitle("Plot Window")
        self.setGeometry(120, 120, 1000, 800)

        layout = QVBoxLayout(self)

        label_layout = QVBoxLayout()

        self.message_label = QLabel('Status', self)
        label_layout.addWidget(self.message_label)

        self.details_label = QLabel("Objects and Detections")
        label_layout.addWidget(self.details_label)

        layout.addLayout(label_layout)

        # Tạo hình và canvas matplotlib
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(self.startFrame)
        self.slider.setMaximum(self.endFrame)
        self.slider.setValue(self.startFrame)
        self.slider.setTickInterval(self.steps)
        self.slider.setSingleStep(self.steps)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.update_plot)
        layout.addWidget(self.slider)

        # Khung hình hiện tại
        self.label = QLabel(f"Frame: {self.startFrame}", self)
        layout.addWidget(self.label)

        # Vẽ lần đầu
        self.update_plot(self.startFrame)

    def e_distance(self, _object, _detection):
        return math.sqrt((_object[0]-_detection[0])**2 + (_object[1]-_detection[1])**2)

    def center_to_2points(self, width, height, x, y):
        a = float(x) - float(width)/2
        b = float(y) - float(height)/2
        c = float(x) + float(width)/2
        d = float(y) + float(height)/2
        return (a, b, c, d)

    def draw_status(self, index):
        canvas = np.zeros((720, 1500, 3), np.uint8)
        canvas.fill(255)
        area_list = {
            'inputArea': (500, 130, 1025, 467),
            'laserArea': (667, 0, 833, 130),
            'hangArea': (0, 133, 667, 420),
            'specialArea': (500, 270, 950, 500),
            'calibArea': (97, 83, 388, 430),
            'scaleArea': (70, 83, 340, 430),
            'inputArea2': (147, 133, 338, 380),
            'outputArea': (25, 140, 195, 210)
        }
        color = 250
        for area in area_list:
            cv2.rectangle(
                canvas,
                (area_list[area][0], area_list[area][1]),
                (area_list[area][2], area_list[area][3]),
                (0, 0, color),
                -1
            )
            color -= 10
        
        objects = self.df.iloc[index].Objects
        detections = self.df.iloc[index].Detections
        timestamp = self.df.iloc[index].Timestamp
        messages = self.df.iloc[index].Messages

        self.message_label.setText(f"Timestamp: {timestamp}\nMessages: {messages}\nObjects: {objects}")

        details_objects_detections = []

        try:
            no_object = (len(detections.split(",")) - 1) // 6
            color = 100
            for i in range(no_object):
                detection_data = detections.split(",")
                location = self.center_to_2points(
                    detection_data[i * 6 + 2],
                    detection_data[i * 6 + 3],
                    detection_data[i * 6 + 4],
                    detection_data[i * 6 + 5]
                )
                location_ = (
                    float(detection_data[i*6+2]),
                    float(detection_data[i*6+3]),
                    float(detection_data[i*6+4]),
                    float(detection_data[i*6+5])
                )
                details_objects_detections.append(
                    f"Detection {i}: {location_} {detection_data[i*6+1]}"
                )
                if int(detection_data[i * 6]) == 0:
                    cv2.rectangle(
                        canvas,
                        (int(location[0]), int(location[1])),
                        (int(location[2]), int(location[3])),
                        (0, color, 0),
                        -1
                    )
                    color += 100
                    cv2.putText(
                        canvas,
                        detection_data[i * 6 + 1],
                        (
                            int(float(detection_data[i * 6 + 4])) - 50,
                            int(float(detection_data[i * 6 + 5])) - 200
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 0)
                    )
                else:
                    cv2.rectangle(
                        canvas,
                        (int(location[0]), int(location[1])),
                        (int(location[2]), int(location[3])),
                        (255, 0, 0),
                        -1
                    )

            no_object = (len(objects.split(",")) - 1) // 6
            for i in range(no_object):
                object_data = objects.split(",")
                cv2.putText(
                    canvas,
                    object_data[i * 6 + 3],
                    (
                        int(float(object_data[i * 6 + 1])) - 50,
                        int(float(object_data[i * 6 + 2])) - 50
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 0)
                )
                location = self.center_to_2points(
                    20, 20, object_data[i * 6 + 1], object_data[i * 6 + 2]
                )
                location_ = (
                    20,
                    20,
                    float(object_data[i*6+1]),
                    float(object_data[i*6+2])
                )
                details_objects_detections.append(f"Object{i}: {location_}")
                cv2.rectangle(
                    canvas,
                    (int(location[0]), int(location[1])),
                    (int(location[2]), int(location[3])),
                    (0, 0, 0),
                    -1
                )
                
            self.message_label.setText(
                f"Timestamp: {timestamp}\nMessages: {messages}\nObjects: {objects}\nNo of detection: {no_object}\nNo of object: {no_object}"
            )
            self.details_label.setText("\n".join(details_objects_detections))
        except Exception as e:
            print(e)

        return canvas

    def update_plot(self, index):
        self.label.setText(f"Frame: {index}")
        canvas = self.draw_status(index)
        self.figure.clear()
        plt.imshow(canvas)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
