import fitz  # PyMuPDF

def is_junk(text):
    lower = text.lower()
    return (
        lower.startswith("arxiv:")
        or "license" in lower
        or "rights reserved" in lower
        or "preprint" in lower
        or "doi" in lower
        or len(lower) < 4
    )

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    font_stats = {}
    title_text = ""

    # Step 1: Collect font sizes and find title from first page
    max_size = 0
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = " ".join([span["text"] for span in line["spans"]]).strip()
                if not line_text or is_junk(line_text):
                    continue
                span = line["spans"][0]
                size = round(span["size"])
                font_stats[size] = font_stats.get(size, 0) + 1

                # Pick title from page 1, ignoring junk
                if page_num == 1 and size > max_size:
                    max_size = size
                    title_text = line_text

    if not title_text:
        title_text = "Untitled Document"

    # Step 2: Deduce H1, H2, H3 from font sizes
    sorted_fonts = sorted(font_stats.items(), key=lambda x: (-x[0], -x[1]))
    h1_size = sorted_fonts[0][0]
    h2_size = sorted_fonts[1][0] if len(sorted_fonts) > 1 else h1_size - 2
    h3_size = sorted_fonts[2][0] if len(sorted_fonts) > 2 else h2_size - 2

    # Step 3: Extract all headings using font size
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = " ".join([span["text"] for span in line["spans"]]).strip()
                if not line_text or is_junk(line_text):
                    continue

                span = line["spans"][0]
                size = round(span["size"])
                level = None

                if size == h1_size:
                    level = "H1"
                elif size == h2_size:
                    level = "H2"
                elif size == h3_size:
                    level = "H3"

                if level:
                    outline.append({
                        "level": level,
                        "text": line_text,
                        "page": page_num
                    })

    return {
        "title": title_text,
        "outline": outline
    }
