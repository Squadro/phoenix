def get_gunicorn_config():
    return {
        'bind': '0.0.0.0:8000',
        'workers': 2,
        'timeout': 60,
        # Other Gunicorn settings...
    }
