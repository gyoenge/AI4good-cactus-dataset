# AI4Good Hackathon Project - Dataset 
## PPT Object Detection Dataset Code 

- Event: AI4Good Hackathon (March 2023)
- Theme: An AWS AI service development hackathon aligned with the UN Sustainable Development Goals (SDGs). 
- Team Idea: An assistive learning tool that **improves graphic accessibility for the visually impaired by converting elements (text, figures) from PowerPoint slides into a Braille pad-compatible format**. 
- Team Size: 5 members (1 Project Manager, 1 Frontend, 1 Backend, 2 AI)
- My Role: Implemented the **PPT Objetect detection features, utilizing AWS Custom Labels & Rekognition Service**.

### Description

This repository is dedicated to **collecting and preprocessing the dataset** for training our AI model.

- `text_image_eng.py`: A script to generate and collect image samples of English text elements.
- `natural_image_fast.py`: A script to crawl and collect natural image elements from Google Images.
- `diagram_gcrawler.py`: A script to crawl and collect diagram elements from Google Images.
- `ppt_object_synthesizer.py`: A script for arranging various shape elements within a PowerPoint (PPT) slide.
- `slide_content_bbox_dataset/*.py`: A collection of scripts to build the final dataset by randomly placing the collected element images onto PPT slides.

### Preview

- Each objects:
<p align="center">
<img width="50%" alt="cactus_dataset_preview" src="https://github.com/user-attachments/assets/7bab9b35-8802-41bc-ae80-5a67e50bc79d" />
</p>  

- Synthesized PPT image (simgle one): 
<p align="center">
<img width="50%" alt="image" src="https://github.com/user-attachments/assets/696a3bed-9292-4a61-a5c1-ed7264d338e0" />
</p>

- Our approach is limited to basic combinations of PowerPoint elements and does not support any overlap between them within our grid system. 
