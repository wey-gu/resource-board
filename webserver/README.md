

## certboot to generate cert for https

```bash
$ wget https://dl.eff.org/certbot-auto
$ chmod +x certbot-auto
$ sudo ./certbot-auto certonly --server https://acme-v02.api.letsencrypt.org/directory --preferred-challenges=dns --manual
```

