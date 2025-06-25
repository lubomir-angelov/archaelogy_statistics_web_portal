from nicegui import ui
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import FileResponse
import os

def build_analytics_page():
    df = pd.DataFrame({
        'site': ['A', 'B'],
        'layer': ['L1', 'L2'],
        'image_url': ['https://via.placeholder.com/150', 'https://via.placeholder.com/200']
    })

    with ui.row().classes('w-full'):
        with ui.column().classes('w-1/4'):
            ui.label('Columns:')
            selected = {}
            for col in df.columns:
                selected[col] = ui.checkbox(col, value=True)

        with ui.column().classes('w-2/4'):
            fig, ax = plt.subplots()
            df['layer'].value_counts().plot(kind='bar', ax=ax)
            output = BytesIO()
            fig.savefig(output, format='png')
            output.seek(0)
            with open('/tmp/plot.png', 'wb') as f:
                f.write(output.getbuffer())

            ui.image('/plot-image')

            ui.table(columns=[{'name': col, 'label': col, 'field': col} for col in df.columns],
                     rows=df.to_dict('records'))

        with ui.column().classes('w-1/4'):
            ui.label('Images')
            for url in df['image_url']:
                ui.image(url).classes('w-full h-auto')

from fastapi import FastAPI
app = FastAPI()

@app.get('/plot-image')
def plot_image():
    return FileResponse('/tmp/plot.png', media_type='image/png')