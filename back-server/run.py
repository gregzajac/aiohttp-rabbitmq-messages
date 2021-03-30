from app import app

if __name__ == "__main__":
    try:
        app.start_app()
    except KeyboardInterrupt:
        app.close_app()
