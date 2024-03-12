from paddleocr import PaddleOCR
ocr=PaddleOCR(use_angle_cls=True,lang="ch")
img_path=r'C:\your position'
result=ocr.ocr(img_path,cls=True)
for line in result:
    for item in line:
        print(item[1][0])

with open (r'C:your position.txt','w')as f:
    for line in result:
        for item in line:
            f.write(item[1][0]+"\n")
