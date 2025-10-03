from . import (
   resume_controller
)


def register_routers(app):
    app.include_router(
        resume_controller.router, prefix="/api", tags=["Resume Filter"]
    )