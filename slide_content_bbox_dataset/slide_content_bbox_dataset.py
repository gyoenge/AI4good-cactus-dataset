import shutil
import os
import uuid
from pptx import Presentation
import subprocess
from pdf2image import convert_from_path
import json

import content_placer_utils as slideMaster
import annonation_utils as labelMaster


with open("config.json", 'r') as config_file:
    config = json.load(config_file)
OUTPUT_ROOT = config['OUTPUT_DIR']['root']
IMAGES_DIR = config['OUTPUT_DIR']['IMAGES_DIR']
YOLO_LABELS_DIR = config['OUTPUT_DIR']['LABELS_DIR']   # Yolo label
COCO_ANN_FILE = config['OUTPUT_DIR']['OUTPUT_FILE']  # Coco label
COCO_CATEGORIES = config['COCO_CATEGORIES']
YOLO_RESULTS_DIR = config['RESULT_DIR']['YOLO_RESULTS_DIR']  # Yolo vis
COCO_RESULTS_DIR = config['RESULT_DIR']['COCO_RESULTS_DIR']  # Coco vis


class SlideContentBboxDataGenerator:
    """
        content images -> PPT에 random하게 배치 후 이미지화 -> image, bbox label 정보 저장 
        - 슬라이드 하나씩 생성 및 저장 진행 
        - 1차적으로 YOLO dataset format을 사용해 images/label 폴더에 저장 
    """

    def __init__(self):
        # for yolo dataset format
        self.output_temp_root = self._load_dir_with_mkdir(OUTPUT_ROOT+"temp/")
        self.output_img_root = self._load_dir_with_mkdir(IMAGES_DIR)
        self.output_label_yolo_root = self._load_dir_with_mkdir(
            YOLO_LABELS_DIR)
        self.output_img_id = uuid.uuid4()

    def _load_dir_with_mkdir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    def _ppt_slide_with_content(self):
        prs = Presentation()
        slide = slideMaster.make_slide(prs)
        bboxes = []
        # slide 내에 content 랜덤하게 배치
        grid_info = slideMaster.select_layout_and_contents()
        for content_frame_info in grid_info:
            frame_grid = content_frame_info['frame_grid']
            content_image_path = content_frame_info['content_image_path']
            slide, bbox = slideMaster.place_content_in_frame(
                slide, frame_grid, content_image_path)
            # bbox 맨 앞에 class_id 추가
            bbox.insert(0, content_frame_info['class_id_yolo'])
            bboxes.append(bbox)
        return prs, bboxes

    def _save_prs_to_jpg(self, prs):
        # .ppt -> .pdf -> .jpg & clean-up
        ppt_temp_path = f"{self.output_temp_root}{self.output_img_id}.pptx"
        pdf_temp_path = f"{self.output_temp_root}{self.output_img_id}.pdf"
        prs.save(ppt_temp_path)
        cmd = ['soffice', '--convert-to', 'pdf', '--outdir',
               self.output_temp_root, ppt_temp_path]  # use LibreOffice
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        images = convert_from_path(pdf_temp_path)  # use Poppler
        images[0].save(
            f"{self.output_img_root}{self.output_img_id}.jpg", "JPEG")
        if os.path.exists(ppt_temp_path):
            os.remove(ppt_temp_path)
        if os.path.exists(pdf_temp_path):
            os.remove(pdf_temp_path)

    def _save_bbox_label_yolo(self, bboxes):
        label_file_name = os.path.join(
            YOLO_LABELS_DIR, f"{self.output_img_id}.txt")
        print(label_file_name)
        with open(label_file_name, 'w') as label_file:
            for bbox in bboxes:
                class_id, x0, y0, x1, y1 = bbox
                label_file.write(f"{class_id} {x0} {y0} {x1} {y1}\n")

    def generate_data(self):
        # place contents on ppt slide
        prs, bboxes = self._ppt_slide_with_content()
        # save image
        self._save_prs_to_jpg(prs)
        # save label (yolo format)
        self._save_bbox_label_yolo(bboxes)


def convert_to_coco():
    """
        IMG_SET_NUM 개에 대해 yolo format dataset 만든 후, 
        - 2차적으로 COCO dataset format label을 annotation.json에 저장
    """
    yoloToCoco = labelMaster.YoloToCoco(IMAGES_DIR, YOLO_LABELS_DIR,
                                        COCO_ANN_FILE, COCO_CATEGORIES)
    yoloToCoco.convert_and_save()


def vis_dataset_yolo_coco():
    """
        yolo labels, coco annotation 사용한 bbox visualize 
    """
    labelMaster.save_yolo_bbox_results(
        IMAGES_DIR, YOLO_LABELS_DIR, YOLO_RESULTS_DIR)
    labelMaster.save_coco_bbox_results(
        IMAGES_DIR, COCO_ANN_FILE, COCO_RESULTS_DIR)


def delete_files_in_dir(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


if __name__ == "__main__":
    for dir in [IMAGES_DIR, YOLO_LABELS_DIR, YOLO_RESULTS_DIR, COCO_RESULTS_DIR]:
        delete_files_in_dir(dir)

    IMG_SET_NUM = 800
    for i in range(IMG_SET_NUM):
        print(i)
        datasetGenerator = SlideContentBboxDataGenerator()
        datasetGenerator.generate_data()
    convert_to_coco()
    vis_dataset_yolo_coco()
