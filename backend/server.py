#!/bin/env python
from app import create_instance, socketio

if __name__ == '__main__':
    app = create_instance()
    socketio.run(app)
