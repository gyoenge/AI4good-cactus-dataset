import json
import os
from pathlib import Path
from PIL import Image, ImageDraw
from datetime import datetime


class YoloToCoco:
    """
        COCO anntoation file 생성 : YOLO data format -> COCO data format으로 json화하여 저장 
    """

    def __init__(self, images_dir, labels_dir, output_file, categories):
        self.images_dir = Path(images_dir)
        self.labels_dir = Path(labels_dir)
        self.output_file = output_file
        self.coco_ann = {'images': [],
                         'annotations': [], 'categories': categories}
        self.annotation_id = 1

    def _convert_single(self, image_id: int, image_file: str, label_file: str):
        # generate "images" list item
        image_path = self.images_dir / image_file
        image = Image.open(image_path)
        image_width, image_height = image.size

        now_iso = datetime.now().isoformat()
        now_datetime = datetime.fromisoformat(now_iso)
        formatted_now = now_datetime.strftime('%Y-%m-%d %H:%M:%S')

        self.coco_ann['images'].append({
            'id': image_id,
            'width': int(image_width),
            'height': int(image_height),
            'file_name': image_file,
            'date_captured': str(formatted_now)
        })

        # generate "annotations" list item
        with open(self.labels_dir / label_file, 'r') as file:
            try:
                for line in file:
                    class_id, x0, y0, x1, y1 = map(float, line.split())
                    category_id = int(class_id) + 1
                    width = int((x1-x0)*image_width)
                    height = int((y1-y0)*image_height)
                    # x_center = int((x0*image_width) + (width/2))
                    x_0 = int(x0*image_width)
                    # y_center = int((y0*image_height) + (height/2))
                    y_0 = int(y0*image_height)
                    self.coco_ann['annotations'].append({
                        'id': self.annotation_id,
                        'image_id': image_id,
                        'category_id': category_id,
                        'bbox': [x_0, y_0, width, height]
                    })
                    self.annotation_id += 1
            except:
                print(f"{label_file} doesn't match with Yolo label format")

    def _save_coco_annotation(self):
        with open(self.output_file, 'w') as file:
            json.dump(self.coco_ann, file)

    def convert_and_save(self):
        for image_id, image_file in enumerate(sorted(os.listdir(self.images_dir)), start=1):
            label_file = f"{Path(image_file).stem}.txt"
            self._convert_single(image_id, image_file, label_file)
        self._save_coco_annotation()


def save_yolo_bbox_results(images_dir, labels_dir, yolo_bbox_result_dir):
    """
        Yolo format OD dataset -> draw bbox on img & save 
    """
    if not os.path.exists(yolo_bbox_result_dir):
        os.makedirs(yolo_bbox_result_dir)

    for file_name in os.listdir(images_dir):
        image_path = os.path.join(images_dir, file_name)
        label_file_name = os.path.splitext(file_name)[0] + '.txt'
        label_path = os.path.join(labels_dir, label_file_name)

        if not os.path.exists(label_path):
            continue

        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        with open(label_path, 'r') as file:
            for line in file:
                class_id, x0, y0, x1, y1 = map(float, line.split())
                image_width, image_height = image.size
                x0, y0, x1, y1 = x0*image_width, y0*image_height, x1*image_width, y1*image_height
                draw.rectangle([x0, y0, x1, y1], outline="red", width=2)

        annotated_image_path = os.path.join(
            yolo_bbox_result_dir, f"annotated_{file_name}")
        image.save(annotated_image_path)


def save_coco_bbox_results(images_dir, annotation_path, coco_bbox_result_dir):
    """
        Coco format OD dataset -> draw bbox on img & save 
    """
    if not os.path.exists(coco_bbox_result_dir):
        os.makedirs(coco_bbox_result_dir)

    with open(annotation_path, 'r') as f:
        coco_ann = json.load(f)

    for image_info in coco_ann['images']:
        image_id = image_info['id']
        file_name = image_info['file_name']
        image_path = os.path.join(images_dir, file_name)

        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        annotations = [
            ann for ann in coco_ann['annotations'] if ann['image_id'] == image_id]
        for ann in annotations:
            # x_center, y_center, width, height = ann['bbox']
            # x0, y0 = x_center - width / 2, y_center - height / 2
            x0, y0, width, height = ann['bbox']
            x1, y1 = x0 + width, y0 + height
            draw.rectangle([x0, y0, x1, y1], outline="red", width=2)

        annotated_image_path = os.path.join(
            coco_bbox_result_dir, f"annotated_{file_name}")
        image.save(annotated_image_path)


# test code
if __name__ == "__main__":
    # load config
    with open("config.json", 'r') as config_file:
        config = json.load(config_file)

    # YoloToCoco test
    IMAGES_DIR = config['OUTPUT_DIR']['IMAGES_DIR']
    LABELS_DIR = config['OUTPUT_DIR']['LABELS_DIR']
    OUTPUT_FILE = config['OUTPUT_DIR']['OUTPUT_FILE']
    COCO_CATEGORIES = config['COCO_CATEGORIES']

    yoloToCoco = YoloToCoco(IMAGES_DIR, LABELS_DIR,
                            OUTPUT_FILE, COCO_CATEGORIES)
    yoloToCoco.convert_and_save()

    # save_*_bbox_results test
    YOLO_RESULTS_DIR = config['RESULT_DIR']['YOLO_RESULTS_DIR']
    COCO_RESULTS_DIR = config['RESULT_DIR']['COCO_RESULTS_DIR']

    save_yolo_bbox_results(IMAGES_DIR, LABELS_DIR, YOLO_RESULTS_DIR)
    save_coco_bbox_results(IMAGES_DIR, OUTPUT_FILE, COCO_RESULTS_DIR)
