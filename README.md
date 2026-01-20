Plugin Builder Results

Your plugin GeoTimeLapse was created in:
    /srv/http/cristian/geo_timelapse

Your QGIS plugin directory is located at:
    /home/cristian/.local/share/QGIS/QGIS3/profiles/default/python/plugins

## generate translation

```bash
pylupdate5 \
geo_timelapse_dialog.py \
$(find src/frontend -name "*.py") \
$(find src/frontend/ui -name "*.ui") \
-ts i18n/GeoTimeLapse_en.ts
```

## compile translation

```bash
lrelease i18n/GeoTimeLapse_en.ts
```

## load image with qrc

```bash
pyrcc5 resources.qrc -o resources.py
```
