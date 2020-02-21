import math
from main import BULLET_CHARACTERS, NUMBERED_LIST_CHARACTERS
import statistics


def get_page_heading(page_blocks, page_index):
    ## Find the heading of the page
    # Assume the heading is the line width the largest font size

    # Find the largest font size
    spans = get_spans(page_blocks)
    max_font_size = get_max_font_size(spans)
    # print("SPANS:\n {} \n".format(spans))
    # print("MAX FONT SIZE: {}\n".format(max_font_size))
    # Get the text of the heading
    heading = ""
    for span in spans:
        font_size = span["size"]
        y0 = get_y0(span)
        x0 = get_x0(span)
        if page_index == 0:
            # If main page, only check for font size
            if font_size == max_font_size:
                return span["text"]
        else:
            # Check for position as well
            # print("{}\nX: {}\nY: {}\n\n".format(span["text"], x0, y0))
            if is_heading(span, max_font_size):
                heading += " " + span["text"].strip()
    return heading

def get_paragraphs(page_blocks):
    # Get relevant paragraphs of page.
    # Loop over all text spans and find the relevant ones
    # Let all text have bulletpoint style
    paragraphs = []

    # Find the largest, smallest and median font size
    spans = get_spans(page_blocks)
    if len(spans) > 1:
        (max_font_size, min_font_size, median_font_size) = get_font_sizes(spans)
    else:
        max_font_size = get_max_font_size(spans)
        min_font_size = max_font_size
        median_font_size = max_font_size
    # Find position of left margin
    left_xpos = 10000

    # Get left margin and check if block has list content
    is_list = False
    for span in spans:
        # print("TEXT: {}\n".format(span["text"]))
        # Check for list char
        if any(c in span["text"] for c in BULLET_CHARACTERS):
            is_list=True
        # Check that this is not the title and that the text is relevant
        # Check only first half of span list
        if not span["size"] == max_font_size and is_relevant_text(span, min_font_size, median_font_size) and span in spans[:math.floor(len(spans)/2)]:
            x0 = get_x0(span)
            # print("{}\nX: {}\nLeft Pos: {}\n\n".format(span["text"], x0, left_xpos))

            # If the line starts with whitespace, adjust x0
            text0 = span["text"]
            text1 = text0.strip()
            ws = len(text0) - len(text1)
            x0 += ws * 8

            if x0 < left_xpos:
                if any(c in span["text"] for c in BULLET_CHARACTERS):
                    left_xpos = x0 + 20
                else:
                    left_xpos = x0

    for i in range(len(spans)):
        span = spans[i]
        # Check that this is not the title and that the text is relevant
        y0 = get_y0(span)
        x0 = get_x0(span)
        # print("THIS:\n{}\nSize:{}\nX: {}\nY: {}\nIs Relevant: {}\n\n".format(span["text"],span["size"], x0, y0, is_relevant_text(span, min_font_size, median_font_size)))
        if not is_heading(span, max_font_size) and is_relevant_text(span, min_font_size, median_font_size):
            p = clean_text(span["text"])
            j = i+1 if i<len(spans)-1 else i

            span0 = span
            next_span = spans[j]

            # print("THIS:\n{}\nX: {}\nY: {}".format(span["text"], x0, y0))
            # print("NEXT:\n{}\nX: {}\nY: {}".format(next_span["text"], get_x0(next_span), get_y0(next_span)))
            # print("IS SAME PAR: {}\n\n".format(is_same_par(span, next_span)))
            # append paragraph:
            while  is_list and is_same_par(span0, next_span) and not i==j:
                # print("{}\nX: {}\nY: {}\n\n".format(spans[j]["text"], get_x0(spans[j]), get_y0(spans[j])))
                p = p + " " + clean_text(next_span["text"])
                spans[j]["text"] = ""
                j = j+1 if j<len(spans)-1 else i
                span0 = next_span
                next_span = spans[j]
            level = get_level(left_xpos, span)
            paragraphs.append((p, level))
    return paragraphs

def is_heading(span, max_font_size):
    y0 = get_y0(span)
    x0 = get_x0(span)
    size = span["size"]
    # print("TEXT: {}\nx0: {} y0: {}\nSIZE: {}\n".format(span["text"], x0, y0, size))
    return y0<100 and abs(size-max_font_size) < 8

def is_same_par(span, next_span):
    x0 = get_x0(span)
    y0 = get_y0(span)
    x1 = get_x1(span)
    y1 = get_y1(span)
    next_x0 = get_x0(next_span)
    next_y0 = get_y0(next_span)
    font_size = span["size"]
    next_font_size = next_span["size"]
    # print("1: {}\nX0: {}\nY0: {}\nX1: {}\nY1: {}\nSize: {}\n\n2: {}\nX: {}\nY: {}\nSize: {}\n\n".format(span["text"], x0, y0, x1, y1, font_size,next_span["text"], next_x0, next_y0, next_font_size))

    return (next_y0-y0 < 10 and abs(next_x0-x1) < 10) or ((abs(next_y0-y1) < 10) and
                                 not any(c in next_span["text"].strip()[:1] for c in BULLET_CHARACTERS) and
                                 abs(font_size - next_font_size) < 1  and
                                 not any(c in next_span["text"].strip()[:2] for c in NUMBERED_LIST_CHARACTERS))

def clean_text(text):
    "Remove unwanted characters"
    # print(text)
    for c in BULLET_CHARACTERS:
        if c in text.strip()[:2]:
            text = text.replace(c, "", 1).strip()
    return text.strip()

def get_level(left_xpos, span):
    x0 = get_x0(span)

    # If the line starts with whitespace, adjust x0
    text0 = span["text"]
    text1 = text0.strip()

    for c in text0:
        if c.strip() == '':
            x0 += 8
        else:
            break

    if any(c in text1[0] for c in BULLET_CHARACTERS):
        x0 += 20

    # print("TEXT: {}\nx_pos: {}\nleft_xpos: {}\n\n".format(text1, x0, left_xpos))

    if x0 - left_xpos < 5:
        return 0
    elif 5 < (x0 - left_xpos) < 30:
        return 1
    elif 30 < (x0 - left_xpos):
        return 2
    return 0

def get_x0(span):
    return span["bbox"][0]

def get_y0(span):
        return span["bbox"][1]

def get_x1(span):
    return span["bbox"][2]

def get_y1(span):
        return span["bbox"][3]

def repr_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_relevant_text(span, min_font_size = 0, median_font_size = 0):
    # Check if single text span contains relevant information
    text = span["text"]
    size = span["size"]
    y0 = get_y0(span)
    is_relevant = True
    if len(clean_text(text)) < 2 or repr_int(text.strip()):
        # Irrelevant or page number
        is_relevant = False
    elif abs(size - min_font_size) < 1 and median_font_size-min_font_size > 8 and y0 > 480:
        # Some bottom line text
        is_relevant = False
    elif abs(size - min_font_size) < 1 and size < 14 and y0 > 500:
        # Some bottom line text
        is_relevant = False
    return is_relevant

def get_max_font_size(spans):
    font_size_list = []
    for span in spans:
        if is_relevant_text(span):
            font_size_list.append(span["size"])
    return max(font_size_list) if len(font_size_list)>0 else 0

def get_font_sizes(spans):
    # returns (max, min, median)
    font_size_list = []
    for span in spans:
        if is_relevant_text(span):
            font_size_list.append(span["size"])
    return (max(font_size_list), min(font_size_list), statistics.median(font_size_list)) if len(font_size_list) > 0 else 0

def get_spans(page_blocks):
    spans = []
    for block in page_blocks:
        if block["type"] == 0:
        # then the block has text
            for line in block["lines"]:
                for span in line["spans"]:
                    spans.append(span)
    return spans