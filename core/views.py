from django.shortcuts import render
import pytesseract
from PIL import Image
from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DangerousSubstance

import re
import unidecode

@csrf_exempt
def ocr_view(request):
    if request.method == 'POST':
        if 'image' not in request.FILES:
            return JsonResponse({"error": "Nicio imagine primită!"}, status=400)

        file = request.FILES['image']
        img = Image.open(BytesIO(file.read()))

        # pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
        extracted_text = pytesseract.image_to_string(img, lang='eng+ron')

        text_lower = extracted_text.lower()
        text_normalized = unidecode.unidecode(text_lower)

        all_substances = DangerousSubstance.objects.all()

        found_unhealthy = []

        for sub in all_substances:

            name_ro_norm = unidecode.unidecode(sub.name_ro.lower()) if sub.name_ro else ""
            name_en_norm = unidecode.unidecode(sub.name_en.lower()) if sub.name_en else ""
            abbr_norm    = unidecode.unidecode(sub.abbreviation.lower()) if sub.abbreviation else ""

            patterns = []
            if name_ro_norm:
                patterns.append(r"\b{}\b".format(re.escape(name_ro_norm)))
            if name_en_norm:
                patterns.append(r"\b{}\b".format(re.escape(name_en_norm)))
            if abbr_norm:
                patterns.append(r"\b{}\b".format(re.escape(abbr_norm)))

            matched = False
            for pat in patterns:
                if re.search(pat, text_normalized):
                    matched = True
                    break

            if matched:
                found_unhealthy.append({
                    "name_ro": sub.name_ro,
                    "abbreviation": sub.abbreviation,
                    "description": sub.description
                })

        response = {
            "text_extras": extracted_text.strip(),
            "unhealthy_substances_found": found_unhealthy
        }
        return JsonResponse(response, status=200)

    else:
        return JsonResponse({"error": "Use POST with an 'image' file."}, status=405)
