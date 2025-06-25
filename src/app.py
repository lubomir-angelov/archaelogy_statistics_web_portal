from fastapi import FastAPI
from nicegui import ui, app as fastapi_app

# local imports
from src.analytics import build_analytics_page

def create_app() -> FastAPI:
    app = FastAPI()

    @ui.page('/')
    def index_page(client):
        ui.label('Welcome')
        ui.link('Analytics', '/analytics')

    @ui.page('/analytics')
    def analytics_page(client):
        build_analytics_page()

    # Mount NiceGUI onto FastAPI’s router
    fastapi_app.include_router(app.router)

    # *** DO NOT call ui.run() or ui.run_with() here! ***
    return fastapi_app