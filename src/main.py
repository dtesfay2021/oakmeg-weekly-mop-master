from constants import S3_OUTPUT_KEY, LAMBDA_TMP_FILE_PATH_DIR, today_ymd
from slides import update_overview_slide, update_mop_slide
from core_funcs import obj_to_s3

from pwpt.base_functions import load_template, delete_slide
from mop.pull_data import pull_campaigns


def main(project, S3_PREFIX):
        
    campaign_list = pull_campaigns(project)
    template_presentation = load_template()
    overview_slide_index = 3
    mop_slide_index = 4

    # Process each campaign sequentiall
    for result in campaign_list:
        campaign = result[0]

        # Duplicate & update overview slide
        update_overview_slide(template_presentation, campaign, overview_slide_index)

        # Duplicate & update mop slide
        update_mop_slide(template_presentation, campaign, mop_slide_index, S3_PREFIX)
        
        print('---')
    
    delete_slide(template_presentation, mop_slide_index)
    delete_slide(template_presentation, overview_slide_index)
    
    # Save updated Pwpt locally, upload to S3
    lambda_tmp_file_path = LAMBDA_TMP_FILE_PATH_DIR + 'output.pptx'
    template_presentation.save(lambda_tmp_file_path)
    
    pwpt_s3_key = S3_PREFIX + '/' + today_ymd + '/' + S3_OUTPUT_KEY
    obj_to_s3(lambda_tmp_file_path, pwpt_s3_key)
    pass


if __name__ == '__main__':
    main()