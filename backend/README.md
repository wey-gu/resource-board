# Resource board backend



## Note on add new resources from PostgreSQL

```bash
$ psql resource_board
```



```sql
resource_board=#
INSERT INTO resources (id,name,scale,note,high_availability,storage_backend,hardware_type,last_changed_by,state_name,used_by)
   VALUES  (9,'DC-new_1',4,'CP test','t','LVM','HP','foo','occupied','bar'),
           (10,'DC-new_2',5,'CP test','t','LVM','HP','foo','occupied','bar');

```



## Gunicorn cmdline

```bash
~/resource_board/backend $ cat wsgi.py
#!/bin/env python
from app import create_instance
application = app = create_instance()

gunicorn -b 127.0.0.1:5001 -k eventlet -w 1 wsgi
```



## Nginx configuration



```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
        server_name dc.siwei.info;

    root ~/www/resource-board/client/dist;
  location / {
    root ~/www/resource-board/client/dist;
    try_files $uri $uri/ @rewrites;
  }

  location @rewrites {
    rewrite ^(.+)$ /index.html last;
  }

  location ~* \.(?:ico|css|js|gif|jpe?g|png)$ {
    # Some basic cache-control for static files to be sent to the browser
    expires max;
    add_header Pragma public;
    add_header Cache-Control "public, must-revalidate, proxy-revalidate";
  }
}


# Virtual Host configuration for example.com
#
# You can move that to a different file under sites-available/ and symlink that
# to sites-enabled/ to enable it.
#
upstream flack_nodes {
    # Socket.IO requires sticky sessions
    ip_hash;
    #
    server 127.0.0.1:5001;
    #             # to scale the app, just add more nodes here!
    #
}
server {
        listen 5000 default_server;
        server_name dc.siwei.info;
    location / {
        proxy_pass http://flack_nodes;
        proxy_redirect off;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # reverse proxy for Socket.IO connections
    location /socket.io {
        proxy_pass http://flack_nodes/socket.io;
        proxy_http_version 1.1;
        proxy_redirect off;
        proxy_buffering off;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }

}
```

