# Guía: instalar y ejecutar esta API en un servidor RHEL (manual, sin Claude Code)

> Probada solo en teoría: adapta versiones y nombres a tu RHEL (aquí se asume RHEL 9 o derivados). Los comandos con `sudo` requieren un usuario con permisos.

## 0. Idea general
En un servidor real hay que hacer a mano lo que en local hace tu máquina: instalar Python y git, traer el código, crear un entorno virtual, instalar dependencias, y dejar la app como **servicio** (systemd) para que arranque sola y se reinicie si cae.

## 1. Paquetes del sistema
```bash
sudo dnf update -y
sudo dnf install -y git python3.12 python3.12-pip
python3.12 --version
```
- El Python por defecto de RHEL 9 es 3.9. Hay paquetes `python3.11` / `python3.12` en los repos.
- Nuestro CI usa **3.14**, que normalmente **no** está en los repos de RHEL. Opciones: compilar desde fuentes, usar `uv` o `pyenv`, o bajar el CI a una versión disponible en RHEL (3.12). Lo más limpio en producción: que CI y servidor usen la misma versión.

## 2. Usuario de servicio (sin privilegios)
```bash
sudo useradd --system --create-home --shell /sbin/nologin apiuser
```
Nunca ejecutes la app como root.

## 3. Traer el código
```bash
sudo -u apiuser -H bash -c 'cd ~ && git clone https://github.com/NenoDaconte/cicd-practica.git'
```
Repo público: no hace falta autenticación. Si fuera privado: *deploy key* SSH o token.

## 4. Entorno virtual y dependencias
```bash
sudo -u apiuser -H bash -c '
  cd ~/cicd-practica &&
  python3.12 -m venv .venv &&
  .venv/bin/pip install -r requirements.txt'
```

## 5. Probar a mano
```bash
sudo -u apiuser -H bash -c 'cd ~/cicd-practica && .venv/bin/pytest -q'
sudo -u apiuser -H bash -c 'cd ~/cicd-practica && .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000'
# en otra terminal:
curl http://127.0.0.1:8000/health
```

## 6. Servicio systemd
Crea `/etc/systemd/system/cicd-practica.service`:
```ini
[Unit]
Description=API cicd-practica
After=network.target

[Service]
User=apiuser
WorkingDirectory=/home/apiuser/cicd-practica
ExecStart=/home/apiuser/cicd-practica/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now cicd-practica
sudo systemctl status cicd-practica
journalctl -u cicd-practica -f        # logs
```

## 7. Exponerla al exterior
Lo habitual es poner un proxy inverso (nginx) delante, y que uvicorn escuche solo en 127.0.0.1.
```bash
sudo dnf install -y nginx
```
`/etc/nginx/conf.d/cicd-practica.conf`:
```nginx
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
```
```bash
sudo setsebool -P httpd_can_network_connect 1   # SELinux: nginx puede conectar al backend
sudo systemctl enable --now nginx
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
curl http://IP_DEL_SERVIDOR/health
```
- **SELinux**: no lo desactives; ajusta booleanos o contextos.
- **firewalld**: abre solo los puertos necesarios.
- Para HTTPS: certbot / Let's Encrypt.

## 8. Actualizar a una nueva versión
```bash
sudo -u apiuser -H bash -c 'cd ~/cicd-practica && git pull && .venv/bin/pip install -r requirements.txt'
sudo systemctl restart cicd-practica
```
Esto es lo que el CD automatizará más adelante.

## 9. Glosario del servidor
| Término | Significado |
|---|---|
| **dnf** | Gestor de paquetes de RHEL. |
| **systemd / unit** | Gestor de servicios; la *unit* describe cómo arrancar uno. |
| **journalctl** | Ver logs de systemd. |
| **uvicorn** | Servidor ASGI que ejecuta FastAPI. |
| **Proxy inverso** | Servidor (nginx) que recibe peticiones y las reenvía a la app. |
| **SELinux** | Control de acceso obligatorio de RHEL. |
| **firewalld** | Cortafuegos de RHEL (`firewall-cmd`). |
| **Usuario de servicio** | Usuario sin login ni privilegios que ejecuta la app. |
