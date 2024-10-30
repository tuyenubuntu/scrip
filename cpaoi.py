import os
import shutil
import pandas as pd

# Đường dẫn file Excel log để ghi lại quá trình copy
log_file_path = 'copy_log.xlsx'

# Đọc dữ liệu từ file Excel
excel_path = 'data (6).xlsx'
data = pd.read_excel(excel_path)

def initialize_log_file():
    # Kiểm tra nếu file log đã tồn tại, nếu chưa thì tạo mới với các cột cần thiết
    if not os.path.exists(log_file_path):
        log_df = pd.DataFrame(columns=["LineName", "MixName", "ElementType"])
        log_df.to_excel(log_file_path, index=False)
        return log_df
    else:
        # Nếu đã có file log, đọc dữ liệu hiện có
        log_df = pd.read_excel(log_file_path)
        return log_df

def copy_images(src_root, dest_root, log_df):
    # Danh sách LineName tự tạo
    LineName = ['06', '07', '08', '09', '11', '12', '17']

    # Tạo DataFrame mới từ log_df cho mục đích so sánh
    comparison_df = log_df.copy()

    for line_name in LineName:
        image_count = 0
        line_data = data[data['LineName'] == line_name]

        # Lấy danh sách các MixName hiện có cho LineName hiện tại
        exists = comparison_df[comparison_df['LineName'] == line_name]['MixName'].tolist()

        for _, row in line_data.iterrows():
            mix_name = row['MixName']
            element_type = row['ElementType']
            #track_name = row['TrackName']

            # Kiểm tra nếu MixName đã tồn tại trong danh sách exists
            if mix_name in exists:
                print(f"Bỏ qua {line_name} - {mix_name} do đã tồn tại trong danh sách.")
                continue

            # Thêm vào comparison_df
            comparison_df = comparison_df.append({"LineName": line_name, "MixName": mix_name, "ElementType": element_type}, ignore_index=True)

            src_folder = os.path.join(src_root, str(line_name), str(mix_name), "A", "SaddleSurface")
            src_folder_b = os.path.join(src_root, str(line_name), str(mix_name), "B", "SaddleSurface")
            dest_folder = os.path.join(dest_root, str(element_type))
            
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            for folder in [src_folder, src_folder_b]:
                if os.path.exists(folder) and image_count < 2000:
                    for filename in os.listdir(folder):
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                            src_path = os.path.join(folder, filename)
                            dest_path = os.path.join(dest_folder, filename)

                            counter = 1
                            while os.path.exists(dest_path):
                                name, ext = os.path.splitext(filename)
                                dest_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
                                counter += 1

                            shutil.copy(src_path, dest_path)
                            image_count += 1

                            # Thêm vào log_df nhưng không lưu ngay
                            log_entry = pd.DataFrame([[line_name, mix_name, element_type]], columns=["LineName", "MixName", "ElementType"])
                            log_df = pd.concat([log_df, log_entry], ignore_index=True)

                            # Ghi log vào file Excel sau mỗi 1000 ảnh được copy
                            if image_count % 1000 == 0:
                                log_df.to_excel(log_file_path, index=False)

                            # Kiểm tra nếu đã đủ 2000 hình ảnh
                            if image_count >= 2000:
                                break
                    if image_count >= 2000:
                        break

        if image_count >= 2000:
            print(f"Đã copy đủ 2000 ảnh từ LineName {line_name}. Chuyển sang LineName tiếp theo.")
            continue
        else:
            print(f"Đã copy tổng {image_count} ảnh từ LineName {line_name}.")

    # Lưu log_df vào file Excel một lần cuối khi hoàn tất
    log_df.to_excel(log_file_path, index=False)

# Đường dẫn thư mục nguồn và đích
src_root = 'Data'  # Thay bằng đường dẫn đến thư mục Data của bạn
dest_root = 'CollectedImages'  # Thay bằng đường dẫn thư mục đích

# Khởi tạo file log và bắt đầu copy
log_df = initialize_log_file()
copy_images(src_root, dest_root, log_df)
