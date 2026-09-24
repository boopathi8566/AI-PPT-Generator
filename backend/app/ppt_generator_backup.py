from pptx import Presentation


def create_presentation(presentation_data, output_path):
    prs = Presentation()

    # Remove the default empty slide
    if len(prs.slides) > 0:
        slide = prs.slides[0]
        rId = slide.slide_id
        prs.part.drop_rel(slide.part.rId)
        del prs.slides._sldIdLst[0]

    for slide_data in presentation_data["slides"]:
        slide = prs.slides.add_slide(
            prs.slide_layouts[1]
        )

        title = slide.shapes.title
        body = slide.placeholders[1]

        title.text = slide_data["title"]

        body.text = ""

        for point in slide_data["content"]:
            paragraph = body.text_frame.add_paragraph()
            paragraph.text = point
            paragraph.level = 0

    prs.save(output_path)

    return output_path