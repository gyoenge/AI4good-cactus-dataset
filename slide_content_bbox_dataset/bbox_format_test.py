import json
from annonation_utils import YoloToCoco, save_coco_bbox_results, save_yolo_bbox_results


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

    print("-------------")
