import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

from pwpt.figs.plotly_utils import M0_LAYOUT, DEFAULT_LAYOUT
from constants import LAMBDA_TMP_FILE_PATH_DIR


def save_fig_to(fig, filename, local, width=None, height=None):
    if local:
        save_path = local + filename
    else:
        save_path = LAMBDA_TMP_FILE_PATH_DIR + filename

    if width and height:
        fig.write_image(save_path, width=width, height=height, scale=4)
    else:
        fig.write_image(save_path, scale=4)
        pio.write_image(fig, file=save_path, format='png')


def plot_bar(result, filename, local=False):
    """
    Plot a daily performance bar + line chart
    Returns: figure (plotly.graph_object.Figure)
    """
    # Pull data from campaign_dict
    date_list = [x for x in result for x in x.keys()]
    impression_list = [x[0] for x in result for x in x.values()]
    ctr_list = [x[2] for x in result for x in x.values()]
    
    # Create plot
    fig = make_subplots(
        specs=[[{"secondary_y": True}]],
        figure=go.Figure(layout={**DEFAULT_LAYOUT, **M0_LAYOUT})
        )

    w_basis = np.asarray([1000 * 3600 * 19] * len(date_list))

    # Add Impressions
    bar_imp = go.Bar(
        x = date_list,
        y = impression_list,
        text = impression_list,
        name = "Impressions",
        marker_color = 'rgb(61,99,151)',
        texttemplate = "%{text:.2s}",
        textfont_color = "white",
        offset = -w_basis / 2,
    )
    fig.add_trace(bar_imp, secondary_y=False)

    # Add CTR
    ctr_scatter = go.Scatter(
        x = date_list,
        y = ctr_list,
        text = ctr_list,
        name = "CTR",
        marker_color = 'rgb(69,148,59)',
        textposition = "top center",
        texttemplate = "CTR:%{text:0.2%}",
        mode = "lines+markers",
    )
    fig.add_trace(ctr_scatter, secondary_y=True)

    # Formatting
    fig.update_layout(
        yaxis = dict(tickformat= ","),
        yaxis2 = dict(tickformat= "0.02%"),
        xaxis = dict(tickformat= "%b %d", tickmode= 'auto'),
        font_family = "AppleGothic",
        font_size = 15,
        width = 1500,
        height = 500
        )

    fig.update_yaxes(title_text= "Impressions", secondary_y= False)
    fig.update_yaxes(title_text= "CTR", secondary_y= True, range= [0, max(ctr_list) * 1.5])
    fig.update_layout()

    save_fig_to(fig, filename, local)

    pass
