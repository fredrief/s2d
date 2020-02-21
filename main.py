from convert import *
import os

# Height of images to be inserted in document
DOCUMENT_IMAGE_HEIGHT = 200
# w/h-ratio to select images
RELEVANT_IMAGE_RATIO = 3
# Bullet list characters
BULLET_CHARACTERS = [ "->", "–>", "-", "–", "•", " ̈"]
NUMBERED_LIST_CHARACTERS = ["1.","2.","3.","4.","5.","6.","7.","8.","9.","10."]


if __name__ == '__main__':
    convert("slides/hd.pdf", "docs/hd.docx")
