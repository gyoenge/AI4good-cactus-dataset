from dotenv import load_dotenv
import os
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import uuid
import random
# font_list_eng.py에 font file name 문자열 리스트 설정 분리
from font_list_eng import font_list_eng as fonts

load_dotenv()
api_key = os.getenv('LOREM_IPSUM_KEY')

text_types = ["short", "line", "paragraph"]
color_types = ["grayscale", "color"]
# fonts = ["arial.ttf", "arialbd.ttf", "arialbi.ttf", "ariali.ttf", "ariblk.ttf", "times.ttf"]
# styles = ["normal", "bold", "italic"]


def get_random_text(text_type):
    if text_type == "short":
        paragraphs, max_length = 1, random.randint(5, 25)
    elif text_type == "line":
        paragraphs, max_length = 1, random.randint(35, 60)
    else:  # paragraph
        paragraphs, max_length = 1, random.randint(300, 500)

    url = f'https://api.api-ninjas.com/v1/loremipsum?paragraphs={paragraphs}&max_length={max_length}&start_with_lorem_ipsum=false&random=true'
    response = requests.get(url, headers={'X-Api-Key': api_key})

    if response.status_code == 200:
        response_text = json.loads(response.text)['text']
        print(f"Download : {response_text}")
        return response_text
    else:
        print("Error:", response.status_code)
        return None


def text_to_image(fileroot, color_type, text):
    image_width = random.choice([500, 600, 700])
    # image = Image.new("RGB", (image_width, 1600), color=(255, 255, 255))
    image = Image.new("RGBA", (image_width, 1600), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    font_file = random.choice(fonts)
    font_size = random.choice([10, 15, 20, 25, 30])
    if color_type == "grayscale":
        gray_value = random.randint(0, 128)
        font_color = (gray_value, gray_value, gray_value, 255)
    else:
        font_color = (random.randint(0, 128), random.randint(
            0, 128), random.randint(0, 128), 255)
    # style = random.choice(styles)
    font = ImageFont.truetype(font_file, font_size)

    # line break
    lines = []
    line = ""
    for char in text:
        test_line = line + char
        test_line = test_line.replace("\n", "")
        test_width = draw.textlength(test_line, font=font)
        if test_width <= image_width:
            line = test_line
        else:
            lines.append(line)
            line = char
    if line:
        lines.append(line)

    # draw & crop
    try:
        if len(lines) == 1:
            lines[0] = lines[0].replace("\n", "")
            print(lines[0])
            x = draw.textlength(lines[0], font=font)
            y = sum(font.getmetrics())
            draw.text((0, 0), lines[0], fill=font_color, font=font)
        else:
            x, y = image_width, 0
            for line in lines:
                line = line.replace("\n", "")
                draw.text((0, y), line, fill=font_color, font=font)
                y += sum(font.getmetrics())
        cropped_image = image.crop((0, 0, x, y))
        # filename = f"{fileroot}{uuid.uuid4()}.jpg"
        filename = f"{fileroot}{uuid.uuid4()}.png"
        cropped_image.save(filename)
    except:
        print(f"Failed to download : font is {font_file}")


if __name__ == "__main__":
    IMG_ROOT_FOLDER = "dataset/text_image/"
    IMG_SET_NUM = 500

    for text_type in text_types:
        for color_type in color_types:
            folder_name = f"{text_type}_{color_type}/"
            fileroot = os.path.join(IMG_ROOT_FOLDER, folder_name)
            if not os.path.exists(fileroot):
                os.makedirs(fileroot)

            for _ in range(IMG_SET_NUM):
                text = get_random_text(text_type)
                if text:
                    text_to_image(fileroot, color_type, text)
