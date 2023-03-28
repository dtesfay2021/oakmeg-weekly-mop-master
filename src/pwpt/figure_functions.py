from pwpt.figs.build_plots import plot_bar
from constants import LAMBDA_TMP_FILE_PATH_DIR


def create_and_position_image(slide, results_dict, filename):
    
    plot_bar(results_dict, filename=filename)
    
    # Adds new shape (graph) ontop (numbers relate to placeholder dims: left, top, width, height)
    filepath = LAMBDA_TMP_FILE_PATH_DIR + filename
    slide.shapes.add_picture(filepath, 826831, 3033007, 11163604, 3541872)
    
    pass