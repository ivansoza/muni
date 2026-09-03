# Operacion de muni - Zacatelco

## Identidad del despliegue

- Municipio: Zacatelco.
- Dominio objetivo: `zacatelco.gob.mx`.
- Rama obligatoria del repositorio: `main_zac`.
- Repositorio remoto: `https://github.com/ivansoza/muni.git`.
- Servidor: instancia EC2 con servicio systemd `muni`.
- Directorio de la aplicacion: `/srv/apps/muni/muni`.
- Servicio web: Gunicorn detras de Nginx.
- Base de datos de produccion: PostgreSQL.

## Estado completado

- El repositorio local esta en `main_zac` y sincronizado con `origin/main_zac`.
- `settings_prod.py` se retiro del repositorio y se conserva solo en el servidor.
- `settings_prod.py` esta ignorado por Git para no publicar secretos ni configuracion especifica del servidor.
- Produccion carga variables desde `/srv/apps/muni/.env` mediante systemd.
- El bucket S3 es `muni-zacatelco`.
- Region S3: `mx-central-1`.
- El acceso S3 usa el rol IAM de la instancia `EC2-S3-Muni-Zacatelco`; no agregar access keys al `.env`.
- Para `mx-central-1` es obligatorio usar:
  `AWS_S3_ENDPOINT_URL=https://s3.mx-central-1.amazonaws.com`.
- La media de Django usa `storages.backends.s3.S3Storage`.
- Las subidas de CKEditor usan `default_storage.url(saved_path)`; no deben construir URLs concatenando `/media/`.
- Se migraron 1,842 archivos a S3, aproximadamente 1.48 GB.
- La carpeta local `media/` fue vaciada y recreada.
- Se elimino el objeto de prueba `s3://muni-zacatelco/prueba-s3.txt`.
- CORS del bucket fue corregido desde AWS para permitir el origen HTTP actual y las peticiones de PDF.js (`GET`, `HEAD`, `Range`).
- `django-storages==1.14.4` y `boto3==1.35.99` estan instalados en `/srv/apps/muni/.venv`.
- El servicio `muni` y Nginx fueron validados como activos.
- Las paginas probadas respondieron `HTTP 200`.
- Se elimino de Nginx el bloque local `location /media/`, porque la media ya se entrega desde S3.

## Configuracion actual del dominio

- DNS publico verificado: `zacatelco.gob.mx` y `www.zacatelco.gob.mx` apuntan a `78.12.42.229`.
- Nginx activo: `server_name zacatelco.gob.mx www.zacatelco.gob.mx`.
- `.env` ya incluye ambos dominios en `DJANGO_ALLOWED_HOSTS`.
- Nginx y Gunicorn fueron recargados despues del cambio.
- HTTP redirige con `301` hacia HTTPS.
- HTTPS responde desde esta instancia con el certificado de Let’s Encrypt.
- El acceso directo por IP devuelve `444` en HTTP y HTTPS; solo los hosts del dominio son atendidos.
- Certbot y `python3-certbot-nginx` estan instalados.
- Renovacion simulada con `sudo certbot renew --dry-run`: correcta.
- Certificados: `/etc/letsencrypt/live/zacatelco.gob.mx/fullchain.pem` y `privkey.pem`.
- `DJANGO_SECURE_SSL_REDIRECT=True` ya esta activo.

## Pasos restantes para activar `zacatelco.gob.mx`

1. Mantener verificado el DNS:
   - `dig +short zacatelco.gob.mx`.
   - `dig +short www.zacatelco.gob.mx`.

2. Mantener Nginx:
   - Conservar `server_name zacatelco.gob.mx www.zacatelco.gob.mx;`.
   - Mantener el proxy al socket `/run/muni/gunicorn.sock`.
   - Ejecutar `sudo nginx -t` antes de recargar.

3. Mantener `/srv/apps/muni/.env`:
   - `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,zacatelco.gob.mx,www.zacatelco.gob.mx`
   - `DJANGO_CSRF_TRUSTED_ORIGINS=https://zacatelco.gob.mx,https://www.zacatelco.gob.mx`
   - Conservar `DJANGO_SECURE_SSL_REDIRECT=True` mientras HTTPS este activo.

4. Mantener certificado:
   - Certificado emitido para `zacatelco.gob.mx` y `www.zacatelco.gob.mx`.
   - Validar renovacion con `sudo certbot renew --dry-run`.

5. Reiniciar o recargar servicios:
   - `sudo systemctl reload nginx`.
   - `sudo systemctl restart muni` despues de modificar `.env`.
   - Verificar `sudo systemctl is-active nginx muni`.

6. Validar la aplicacion:
   - Pagina principal y panel de administracion.
   - Una imagen de S3.
   - Un PDF de una seccion general.
   - Un PDF de recomendaciones mediante PDF.js.
   - Redireccion HTTP a HTTPS.
   - Cookies seguras y ausencia de errores CORS en el navegador.

## Actualizar la aplicacion despues de cambios en Git

Ejecutar en el servidor desde el directorio de la aplicacion:

```bash
cd /srv/apps/muni
git status
git pull --ff-only origin main_zac
/srv/apps/muni/.venv/bin/pip install -r requirements.txt
cd /srv/apps/muni/muni
set -a && source ../.env && set +a
DJANGO_SETTINGS_MODULE=muni.settings_prod /srv/apps/muni/.venv/bin/python manage.py check
DJANGO_SETTINGS_MODULE=muni.settings_prod /srv/apps/muni/.venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart muni
sudo nginx -t && sudo systemctl reload nginx
sudo systemctl is-active muni nginx
```

- No ejecutar `git reset --hard` en este servidor.
- Confirmar que la rama sea `main_zac` antes de hacer `git pull`.
- Respaldar o revisar cambios locales antes de actualizar.
- `settings_prod.py` y `.env` son locales y no deben eliminarse durante la actualizacion.
- Si cambia el codigo sin cambiar dependencias, se puede omitir la instalacion de requirements.
- Si falla `manage.py check`, no reiniciar el servicio hasta corregir el error.

## Recargar solo la aplicacion

Para cambios de Python, plantillas, CSS, JavaScript o archivos de la aplicacion no es necesario reiniciar la instancia EC2:

```bash
sudo systemctl restart muni
sudo systemctl is-active muni
curl -I http://127.0.0.1/ -H 'Host: zacatelco.gob.mx'
```

Para cambios unicamente en Nginx:

```bash
sudo nginx -t && sudo systemctl reload nginx
sudo systemctl is-active nginx
```

Para cambios en `/etc/systemd/system/muni.service`:

```bash
sudo systemctl daemon-reload
sudo systemctl restart muni
sudo systemctl is-active muni
```

Reiniciar la instancia completa solo es necesario por cambios del sistema operativo, kernel, red o mantenimiento de EC2:

```bash
sudo systemctl reboot
```

## Archivos, rutas y comandos principales

| Elemento | Ruta o comando |
|---|---|
| Raiz del repositorio | `/srv/apps/muni` |
| Codigo Django | `/srv/apps/muni/muni` |
| Entorno virtual | `/srv/apps/muni/.venv` |
| Variables de produccion | `/srv/apps/muni/.env` |
| Settings de produccion | `/srv/apps/muni/muni/muni/settings_prod.py` |
| Servicio systemd | `/etc/systemd/system/muni.service` |
| Configuracion Nginx activa | `/etc/nginx/sites-available/muni` |
| Socket Gunicorn | `/run/muni/gunicorn.sock` |
| Archivos estaticos | `/srv/apps/muni/muni/staticfiles` |
| Media | Bucket S3 `muni-zacatelco` |
| Rama de produccion | `main_zac` |
| Reiniciar Django/Gunicorn | `sudo systemctl restart muni` |
| Recargar Nginx | `sudo nginx -t && sudo systemctl reload nginx` |
| Probar bloqueo de IP | `curl -I http://78.12.42.229/` |
| Ver logs de la aplicacion | `sudo journalctl -u muni -f` |
| Ver logs de Nginx | `sudo tail -f /var/log/nginx/error.log` |
| Ver espacio disponible | `df -h /` |

## Reiniciar o detener la instancia EC2

La instancia actual es `i-07ef7f38cb474addc` en la cuenta AWS `730335662889`.
Estos comandos requieren permisos EC2 y deben ejecutarse desde un equipo con AWS CLI configurada.

Consultar estado:

```bash
aws ec2 describe-instances --instance-ids i-07ef7f38cb474addc \
   --query 'Reservations[0].Instances[0].State.Name' --output text
```

Reiniciar el sistema operativo sin cambiar la instancia:

```bash
sudo systemctl reboot
```

Detener la instancia EC2:

```bash
aws ec2 stop-instances --instance-ids i-07ef7f38cb474addc
```

Iniciar la instancia EC2:

```bash
aws ec2 start-instances --instance-ids i-07ef7f38cb474addc
```

Reiniciar la instancia EC2 desde AWS:

```bash
aws ec2 reboot-instances --instance-ids i-07ef7f38cb474addc
```

- `stop-instances` apaga la maquina y puede interrumpir el sitio; no usar para un simple cambio de codigo.
- Antes de detenerla, comprobar que no haya migraciones, cargas de archivos o procesos activos.
- Despues de iniciar o reiniciar, validar SSH, PostgreSQL, `muni`, Nginx, DNS y HTTPS.
- La IP publica puede cambiar despues de detener la instancia si no usa Elastic IP.

## Dependencias y archivos locales pendientes

- `requirements.txt` contiene los paquetes S3, pero el cambio aun debe publicarse en `main_zac`.
- `.env.example` existe localmente y no debe contener secretos reales.
- `deploy/muni.service` y `deploy/nginx-muni.conf.example` existen localmente, pero aun no estan versionados.
- Revisar y publicar esos archivos solo despues de confirmar que no contienen rutas o valores exclusivos de otro municipio.
- `settings_prod.py` no debe volver al repositorio; cada servidor debe provisionarlo de forma segura.

## Incidencias conocidas

- CKEditor registra el error preexistente `No module named 'path_to_storage'` por un valor placeholder en `CKEDITOR_5_FILE_STORAGE`. No esta relacionado con S3 y queda pendiente.
- El rol IAM de la instancia no tiene permisos para consultar o modificar CORS del bucket (`s3:GetBucketCORS`, `s3:PutBucketCORS`). Los cambios CORS deben hacerlos un administrador AWS o una politica IAM autorizada.
- GitHub reporto 4 vulnerabilidades moderadas en la rama por defecto; revisar Dependabot.

## Comandos de comprobacion

```bash
git -C /srv/apps/muni branch --show-current
git -C /srv/apps/muni status --short
sudo systemctl is-active muni nginx
sudo nginx -t
curl -I http://zacatelco.gob.mx/
aws sts get-caller-identity
aws s3 ls s3://muni-zacatelco --summarize --human-readable
aws ec2 describe-instances --instance-ids i-07ef7f38cb474addc \
   --query 'Reservations[0].Instances[0].State.Name' --output text
df -h /
```

## Seguridad

- No publicar `/srv/apps/muni/.env`.
- No agregar claves de acceso AWS: el rol IAM de EC2 ya proporciona credenciales temporales.
- No borrar `settings_prod.py` local mientras el servicio systemd lo use.
- Antes de limpiar archivos, comprobar que existan en S3 y que la aplicacion genere URLs firmadas funcionales.
- Vigilar espacio con `df -h /`.
