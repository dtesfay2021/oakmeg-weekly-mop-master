

def update_slide_text(slide, campaign_dict: dict):
    """
    Loop through newly created slide, shapes, and paragraphs.
    Replaces text matching index in `campaign_dict`. 
    
    No need to return the slide, function updates the Presentation variable
    """
    # Loop through new slide shapes
    for shape in slide.shapes:
        if shape.has_text_frame:
            # Set text
            text_frame = shape.text_frame
            for p_idx, para in enumerate(text_frame.paragraphs):
                for t_idx, text in enumerate(para.runs):
                    cur_text = text_frame.paragraphs[p_idx].runs[t_idx].text.lower()

                    # Check campaign dict
                    if cur_text in campaign_dict.keys():
                        new_text = campaign_dict[cur_text]
                        text_frame.paragraphs[p_idx].runs[t_idx].text = new_text

                        print(f"{cur_text} changed to {new_text}")
    pass




