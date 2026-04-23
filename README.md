Propuesta de sistema automático: TikTok Shop → Capturar imágenes → Crear Reels → Publicar en Pinterest + YouTube Shorts

Este repositorio es un esqueleto MVP para automatizar un flujo de creación y distribución de contenido. El objetivo es convertir listados de TikTok Shop en reels y distribuirlos en Pinterest y YouTube Shorts con mínima intervención manual.

Arquitectura propuesta
- Módulo de extracción: obtiene URLs de imágenes desde TikTok Shop (o desde tu backend si dispones de una API). En este MVP usamos URLs de ejemplo para ilustrar el flujo.
- Módulo de captura: descarga imágenes y las almacena localmente o en almacenamiento externo.
- Módulo de creación de reels: compone un video 9:16 a partir de imágenes, añade overlays simples y exporta un reel.
- Módulo de publicación: publica el reel en Pinterest y YouTube Shorts con metadatos apropiados.
- Orquestador: coordina los pasos, maneja errores y reintentos, y facilita la ejecución mediante CLI o CI.
- CI/CD: automatiza la ejecución mediante GitHub Actions o un scheduler propio.

Requisitos previos
- Fuente de imágenes de tus productos (API de TikTok Shop, Shopify u otro backend propio).
- Credenciales para Pinterest API y YouTube Data API (OAuth2 y/o API Keys).
- Python 3.8+ y ffmpeg disponible en el entorno de ejecución.
- Un almacenamiento (local o en la nube) para las imágenes y videos generados.

Ejecución local
- Configura credenciales en un archivo .env o en tu gestor de secretos de CI.
- Ejecuta: python src/main.py --shop-id <ID> --board-id <PinterestBoardID> --youtube-category "Shorts" --output-dir outputs

Estructura del proyecto
- .github/workflows/automation.yml
- src/
- requirements.txt

Notas de seguridad
- No subas credenciales al repositorio. Utiliza GitHub Secrets o herramientas de gestión de secretos.
- Asegúrate de respetar las políticas de uso de APIs y derechos de autor de contenidos (música, imágenes).
