from pwpt.base_functions import duplicate_slide
from pwpt.text_functions import update_slide_text
from pwpt.figure_functions import create_and_position_image

from core_funcs import obj_to_s3
from constants import today_ymd

def update_overview_slide(pres, campaign_dict, slide_index):

    new_overview_slide = duplicate_slide(pres, slide_index)
    update_slide_text(new_overview_slide, campaign_dict)

    # Some stuff on replacing assets?
    
    print('* Overview slide updated *')
    pass


def update_mop_slide(pres, campaign_dict, slide_index, s3_output_prefix):

    new_overview_slide = duplicate_slide(pres, slide_index)
    update_slide_text(new_overview_slide, campaign_dict)
    
    # Adds in MOP daily perf
    create_and_position_image(new_overview_slide, campaign_dict['daily_fig_performance'], 'daily_fig.png')
    obj_to_s3('/tmp/daily_fig.png', f"{s3_output_prefix}/{today_ymd}/{campaign_dict['campaign_name']}_daily.png")

    print('* MOP slide updated *')
    pass