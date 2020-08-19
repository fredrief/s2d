from fitz import Pixmap
from main import RELEVANT_IMAGE_RATIO
import fitz

def get_images(page, imblocks, page_index):
    im_list = []
    i = 0
    pagepix = page.getPixmap(page_index)
    pw = pagepix.width
    ph = pagepix.height
    # print("PH: {}\nPW: {}\n\n".format(ph, pw))
    for block in imblocks:
        try:
            ending = block["ext"]
            pix = Pixmap(block["image"])
            x0 = block["bbox"][0]
            y0 = block["bbox"][1]
            x1 = block["bbox"][2]
            y1 = block["bbox"][3]
            w = pix.width
            h = pix.height
            filename = "static/images/image_{}-{}.{}".format(page_index, i, ending)
            if is_relevant_image(pw, ph, pix, x0, y0, x1, y1):
                if pix.n < 5:  # this is GRAY or RGB
                    pix.writePNG(filename)
                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG(filename)
                    pix1 = None
                pix = None
                if h > w:
                    im_list.append((filename, "H"))
                else:
                    im_list.append((filename, "W"))
            i += 1
        except:
            pass
        finally:
            pass
    return im_list

def is_relevant_image(page_width, page_height, pix, x0, y0, x1, y1):
    # Add tests to decide if the image is relevant and should be included in document
    w = pix.width
    h = pix.height
    # print("X: {}\nY: {}\n\n".format(x0, y0))
    if w/h > RELEVANT_IMAGE_RATIO or h/w > RELEVANT_IMAGE_RATIO:
        return False
    if is_corner_image(page_width, page_height, x0, y0, x1, y1):
        return False
    if abs(page_height-y0)<100:
        return False
    return True

def is_corner_image(page_width, page_height, x0, y0, x1, y1):
    right_margin = page_width-x1
    top_margin = y0
    bottom_margin = page_height-y1
    left_margin = x0
    # print("LM: {}\nTM: {}\n".format(right_margin, top_margin))
    if (right_margin < 10 and top_margin < 50) or (left_margin < 10 and top_margin < 50) or (right_margin < 10 and bottom_margin < 50) or (left_margin < 10 and bottom_margin < 50):
        return True
    return False
