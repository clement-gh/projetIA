FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN git clone https://github.com/IDEA-Research/GroundingDINO.git
RUN git clone https://github.com/facebookresearch/segment-anything.git segmentAnything
RUN git clone https://github.com/WongKinYiu/yolov7.git

RUN mkdir -p weights
WORKDIR weights
RUN curl -O https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
RUN curl -O https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
WORKDIR /
RUN mkdir -p yolov7
WORKDIR yolov7
RUN wget https://github.com/clement-gh/4A-Internship/raw/main/best.pt -O best.pt
WORKDIR /

RUN pip install -e GroundingDINO

CMD ["python", "main.py"]


