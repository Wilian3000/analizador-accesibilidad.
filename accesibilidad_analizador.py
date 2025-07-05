import requests
from bs4 import BeautifulSoup
import json

def analizar_accesibilidad(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        return {"error": str(e)}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Imágenes sin alt
    imagenes = soup.find_all('img')
    imgs_sin_alt = [str(img)[:100] for img in imagenes if not img.has_attr('alt') or not img['alt'].strip()]

    # Inputs sin label
    inputs = soup.find_all(['input', 'textarea', 'select'])
    campos_sin_label = []
    for campo in inputs:
        id_campo = campo.get('id')
        if id_campo:
            label = soup.find('label', attrs={'for': id_campo})
            if not label:
                campos_sin_label.append(str(campo)[:100])
        else:
            campos_sin_label.append(str(campo)[:100])

    resultados = {
        "url": url,
        "imagenes_sin_alt": imgs_sin_alt,
        "campos_sin_label": campos_sin_label,
        "total_errores": len(imgs_sin_alt) + len(campos_sin_label)
    }

    # Guardar a archivo
    with open("reporte_accesibilidad.json", "w", encoding='utf-8') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    return resultados
