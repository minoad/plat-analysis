# Plat Analysis

## Introduction

Find the plats

Given a set of pdf's of plats
    1. Remove watermark
    1. OCR document
    1. Store text data
    1. Analyse text data

## Setup

```shell
# TODO: Move this to .devcontainer
## If needed: sudo vi /etc/apt/sources.list
## deb http://archive.ubuntu.com/ubuntu bionic universe
apt update
apt install -y tesseract-ocr libtesseract-dev libpoppler-cpp-dev poppler-utils
pip install -e .

# Install pytesseract
# windows https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe
# ubuntu 
```