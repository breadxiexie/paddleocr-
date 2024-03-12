import cv2
from paddleocr import PaddleOCR
import os
import numpy as np

# 初始化 PaddleOCR，设置语言为中文
ocr = PaddleOCR(lang="ch")

# 定义旋转函数
def rotate_image(img, angle):
    (h, w) = img.shape[:2]  # 获取图像的高和宽
    center = (w // 2, h // 2)  # 计算图像中心点

    # 计算旋转矩阵，不进行缩放
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    # 计算新图像的边界框尺寸
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    # 更新旋转矩阵的平移部分，以确保旋转后的图像居中
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]

    # 执行旋转，并且使用BORDER_REFLECT填充边界
    rotated_img = cv2.warpAffine(img, M, (new_w, new_h), borderMode=cv2.BORDER_REFLECT101)

    return rotated_img



# 文本识别并保存为txt
def ocr_to_txt(ocr_model, img_path, txt_path):
    result = ocr_model.ocr(img_path, cls=True)
    #text = '\n'.join([line[1][0] for line in result])
    for line in result:
        for item in line:
            print(item[1][0])
    with open(txt_path, 'w', encoding='utf-8') as f:
        #f.write(text)
        for line in result:
            for item in line:
                f.write(item[1][0]+"\n")

# 根据文件夹名字来判断旋转角度
def get_rotation_angle(folder_name):
    if "90" in folder_name:
        return 90
    if "180" in folder_name:
        return 180
    if "270" in folder_name:
        return 270
    if "360" in folder_name:  # 新增旋转360度的处理
        return 360
    return 0

# 主处理函数
def process_images(base_folder):
    result_folder = os.path.join(base_folder, 'result')
    # 创建result目录
    os.makedirs(result_folder, exist_ok=True)
    
    # 循环每一个要求的文件夹名称，新增对'circle360'的处理
    for folder_name in ['circle90', 'circle180', 'circle270', 'circle360']:
        folder_path = os.path.join(base_folder, folder_name)
        
        # 获取旋转角度
        rotation_angle = get_rotation_angle(folder_name)
        
        # 遍历子文件夹
        for sub_folder_name in os.listdir(folder_path):
            if sub_folder_name.lower().startswith('paper'):
                sub_folder_path = os.path.join(folder_path, sub_folder_name)

                # 遍历子文件夹下的所有图片文件
                for image_name in os.listdir(sub_folder_path):
                    if image_name.lower().endswith(('.jpg', '.png', '.jpeg')):
                        image_path = os.path.join(sub_folder_path, image_name)
                        img = cv2.imread(image_path)
                        txt_file_name = os.path.splitext(image_name)[0] + '.txt'

                        if img is not None and rotation_angle > 0:
                            # 旋转图片
                            img_rotated = rotate_image(img, rotation_angle)
                            # 命名新图片
                            new_image_name = os.path.splitext(image_name)[0] + 'new' + os.path.splitext(image_name)[1]
                            new_image_path = os.path.join(sub_folder_path, new_image_name)
                            # 保存新图片
                            cv2.imwrite(new_image_path, img_rotated)
                            img_to_ocr = new_image_path
                        else:
                            img_to_ocr = image_path
                            
                        # OCR提取文字
                        result_txt_folder = os.path.join(result_folder, folder_name, sub_folder_name)
                        os.makedirs(result_txt_folder, exist_ok=True)
                        txt_file_path = os.path.join(result_txt_folder, txt_file_name)
                        
                        ocr_to_txt(ocr, img_to_ocr, txt_file_path)
                        print(f"Processed and extracted text from {image_name} in {sub_folder_name}")
                    else:
                        print(f"Skipping file {image_name} as it does not appear to be a valid image file.")

# 设定根目录路径
base_folder = r'C:\your position'

# 处理图片
process_images(base_folder)

