> referring to blog on this project: <https://note.siwei.info/project-resource-board-a-scalable-webapp-with-flask-socketio-and-vue-js/>



## arch digram

> Arch designed as below

![Arch digram](https://note.siwei.info/project-resource-board-a-scalable-webapp-with-flask-socketio-and-vue-js/arch_diagram_0.png)



## prototpying

Created by Balsamiq Mockups, an animation was created as well.

```bash
resource-board ❯ tree prototype
prototype
├── board.bmpr
├── board.pdf
└── demo-board-history.mp4
```



## web-client

> Single-page web client created by Vue.js

```bash
cd client
npm install
npm run build
```



## backend

> RESTful and SocketIO server createy with Flask-Socket.IO

```bash
cp backend/.env-example backend/.env
cd backend
vim .env # edit configurations
python server.py
```

