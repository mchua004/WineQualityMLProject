#!/usr/bin/env python
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px
import json
import os
# predict the wine quality
def wine_quality(prediction):
    if prediction < 5 :
        quality = 'Poor Quality '
    elif prediction > 7:
        quality = 'Good Quality '
    else:
        quality = 'Average Quality '
    return quality

# predict the wine type
def wine_type(prediction):
    if prediction == 0:
        wtype='white'
    else:
        wtype='red'
    return wtype

def plotly_figure_type(df_compoents,data_point_components, categories):
    # plotting the dataset that we already have
    fig = px.scatter(df_compoents, x=0, y=1, color=categories)
    #changing the marker size
    fig.update_traces(marker=dict(size=10,line=dict(width=1.5, color='DarkSlateGrey')))
    #updating the plot layout
    fig.update_layout(
    xaxis_title="PC 1",
    yaxis_title="PC 2",
    title={'text':  "First two principal components of PCA",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor':'top'},
    font_family= 'Arial',
    legend_title="Wine Color")
    #adding the new point evaluated
    fig.add_trace(
    go.Scatter(
        x=[data_point_components[0][0]],
        y=[data_point_components[0][1]],
        mode="markers",
        name = "predicted data point",
        marker=dict(
            color='Lime',
            size=15,
            line=dict(
                color='DarkGreen',
                width=3
            )),
        showlegend=True))
    graphJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJson

def new_dataframe(dataframe, series):
    return dataframe.append(series, ignore_index=True).reset_index(drop=True)

def rm_tmp_file():
    try:
        os.remove('lib/data/winequality-flask.csv')
    except:
        pass


if __name__ == "__main__":
    wtype = wine_quality(0)
    qual = wine_quality(8)
    print(wtype,' Wine of ', qual)      

