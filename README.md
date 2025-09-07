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
