# AI4Good Hackathon Dataset 

- 2024 Mar. AI4Good Hackathon 
- 대회 주제 : UN SDGs 주제에 맞는 AI 서비스 개발 해커톤 
- **Cactus팀 아이디어** : 시각장애인의 그래픽 접근성을 높이는 학습 보조 도구. **PPT 그래픽 강의 자료에서 text, figure 등의 요소를 점자 패드 형식으로 일대일 대응시켜 변환해주는 시스템**.
- **AI 활용 : PPT에서 document 요소 객체탐지 추출** 
- AI Dataset 수집을 위한 레포입니다 

### description

- text_image_eng.py : 영어 text 요소 이미지를 생성하여 수집하기 위한 코드.
- natural_image_fast.py : google에서 image 요소 이미지를 크롤링하여 수집하기 위한 코드. 
- diagram_gcrawler.py : google에서 diagram 요소 이미지를 크롤링하여 수집하기 위한 코드. 
- ppt_object_synthesizer.py : PPT 도형 요소들을 PPT에 배치하기 위한 코드.
- slide_content_bbox_dataset/*.py : 각 요소 이미지들을 PPT에 무작위로 배치하여 최종 데이터셋을 구축하기 위한 코드.

