from app import new_app


if __name__ == '__main__':
    try:
        new_app.start_app()
    except KeyboardInterrupt:
        new_app.close_app()
