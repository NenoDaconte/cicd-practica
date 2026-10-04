# Guía: lo que hemos hecho y glosario de git / CI/CD

## 1. Cronología de lo realizado

1. **API mínima** (`app/main.py`) con FastAPI: `GET /` (saludo) y `GET /health` (`{"status":"ok"}`).
2. **Test** (`tests/test_health.py`) con pytest para `/health`.
3. **`requirements.txt`** con versiones fijadas (`==`) para que local, CI y servidor usen exactamente lo mismo.
4. **`.gitignore`** de Python (venvs, caches, `.env`...).
5. **Identidad de git** configurada solo en este repo (`git config user.name` / `user.email`). Se usa el email `noreply` de GitHub para no exponer el correo personal.
6. **Primer commit** y renombrado de la rama a `main` (`git branch -m main`).
7. **Instalación de `gh`** (GitHub CLI) y login con `gh auth login`.
8. **Creación del repo remoto** y subida: `gh repo create cicd-practica --public --source=. --remote=origin --push`.
9. **Rama `ci/primer-workflow`**, workflow `.github/workflows/ci.yml` (ejecuta pytest), commit, push de la rama y **Pull Request #1**. El check `test` pasó en verde.
10. **Rama `docs/guias`** con estas guías (otro PR).

## 2. Flujo profesional resumido

```
git switch main && git pull          # partir de lo último
git switch -c tipo/descripcion       # rama nueva
# ...editar...
git add <archivos> && git commit     # commits pequeños
git push -u origin tipo/descripcion  # subir la rama
gh pr create                         # abrir Pull Request
# CI corre solo -> revisión -> merge
git switch main && git pull          # traer el resultado
git branch -d tipo/descripcion       # borrar rama local
```

## 3. Glosario de git y GitHub

| Término | Significado |
|---|---|
| **Repositorio (repo)** | Carpeta de proyecto con todo su historial de cambios (carpeta oculta `.git`). |
| **Local / remoto** | Local: tu copia en tu máquina. Remoto: copia alojada en un servidor (GitHub). |
| **origin** | Nombre por defecto del remoto principal. Solo es un alias de la URL. |
| **main** | Nombre de la rama principal, la que representa el código "bueno" y desplegable. Antes se llamaba `master`; es solo convención. |
| **master** | Nombre antiguo de la rama principal. Git lo usaba por defecto. |
| **Rama (branch)** | Línea de desarrollo independiente. Permite trabajar en un cambio sin tocar `main`. |
| **HEAD** | Puntero a "dónde estás ahora": normalmente la rama activa y su último commit. |
| **Commit** | Foto del proyecto en un momento, con autor, fecha y mensaje. Se identifica por un hash (`d2fa2c4`). |
| **Hash** | Identificador único de un commit (SHA-1), p. ej. `d2fa2c4...`. |
| **Staging / índice** | Zona intermedia: `git add` coloca ahí lo que irá en el próximo commit. |
| **Working tree** | Los archivos tal como están ahora en tu carpeta. |
| **clone** | Copiar un repo remoto a tu máquina. |
| **add** | Añade cambios al staging. |
| **push** | Sube tus commits locales al remoto. |
| **pull** | Baja del remoto y integra en tu rama (`fetch` + `merge`). |
| **fetch** | Baja novedades del remoto sin integrarlas. |
| **merge** | Unir los cambios de una rama en otra. |
| **squash merge** | Merge que junta todos los commits de la rama en uno solo en `main`. |
| **rebase** | Reescribir una rama para que parta de otro punto; deja un historial lineal. |
| **switch / checkout** | Cambiar de rama (`switch` es la forma moderna). |
| **stash** | Guardar cambios sin commit en un cajón temporal. |
| **diff** | Diferencias entre dos versiones. |
| **log** | Historial de commits. |
| **status** | Estado actual: qué cambió, qué está en staging. |
| **tag** | Etiqueta fija sobre un commit, típica para versiones (`v1.0.0`). |
| **upstream** | Rama remota con la que una rama local está enlazada (`-u`). |
| **Fork** | Copia de un repo ajeno en tu cuenta. |
| **Pull Request (PR)** | Petición para integrar una rama en otra, con revisión y checks. |
| **Code review** | Revisión del código de un PR por otra persona. |
| **Issue** | Ticket: tarea, bug o idea registrada en GitHub. |
| **Conventional Commits** | Convención de mensajes: `feat:`, `fix:`, `ci:`, `docs:`... |
| **Branch protection** | Reglas de GitHub sobre una rama (exigir PR, CI en verde, aprobaciones). |
| **.gitignore** | Lista de archivos que git no debe rastrear. |
| **Conflicto de merge** | Dos ramas cambiaron lo mismo; hay que resolverlo a mano. |

## 4. Glosario de CI/CD

| Término | Significado |
|---|---|
| **CI (Integración Continua)** | Ejecutar automáticamente build/tests en cada cambio. |
| **CD (Entrega / Despliegue Continuo)** | Entrega: dejar el artefacto listo para desplegar. Despliegue: desplegarlo automáticamente. |
| **Pipeline** | Secuencia automatizada de pasos (lint, test, build, deploy). |
| **GitHub Actions** | Sistema de CI/CD integrado en GitHub. |
| **Workflow** | Archivo YAML en `.github/workflows/` que define un pipeline. |
| **Trigger (`on:`)** | Evento que lo lanza: push, pull_request, schedule... |
| **Job** | Conjunto de pasos que corren en una misma máquina. |
| **Step** | Un paso: un comando (`run`) o una action (`uses`). |
| **Action** | Pieza reutilizable (`actions/checkout`). |
| **Runner** | Máquina que ejecuta los jobs (`ubuntu-latest`). |
| **Check** | Resultado (verde/rojo) de un job, visible en el PR. |
| **Artefacto** | Resultado de un build (imagen, binario, zip). |
| **Secret** | Valor sensible guardado cifrado en GitHub, no en el código. |
| **Pinning (fijar versiones)** | Usar versiones exactas (`==`) para builds reproducibles. |
| **venv** | Entorno virtual de Python: dependencias aisladas por proyecto. |
| **Endpoint** | Ruta de la API (`/health`). |
| **Health check** | Endpoint que indica si la app está viva; lo usan balanceadores y monitorización. |
