from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import BackgroundTasks
from typing import List
import os
import shutil

documents_path  = "C:/Users/Ximena/Desktop/vehiculos"

async def vehicle_documents(company_code: str, vehicle_number: str):
  try:
    base_path = os.path.join(documents_path, company_code, vehicle_number)
    documents = []

    if not os.path.exists(base_path):
      return JSONResponse(content={"message": "Documentos no encontrados para la unidad."}, status_code=404)

    for i in range(1, 16):
      doc_id = f"docu{str(i).zfill(2)}"
      doc_base = f"{doc_id}.pdf"
      existe = 0
      folios = 0
      mensaje = ""

      if os.path.exists(os.path.join(base_path, doc_base)):
          existe = 1

      # Verificar folios: docu011.pdf, docu012.pdf ... docu019.pdf
      folios_existentes = [
          f for f in os.listdir(base_path)
          if f.startswith(doc_id) and f != doc_base and f.endswith(".pdf")
      ]

      if folios_existentes:
        folios = 1
        mensaje = f"Tiene {len(folios_existentes) + 1} folios."

      documents.append({
        "nombre_documento": doc_id,
        "existe": existe,
        "folios": folios,
        "mensaje": mensaje if folios else ""
      })

    return JSONResponse(content=jsonable_encoder(documents), status_code=200)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=500)