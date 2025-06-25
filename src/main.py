from app import create_app
from nicegui import ui

if __name__ in {"__main__", "__mp_main__"}:
    app = create_app()
    ui.run(title='Ceramics Analytics', reload=False)