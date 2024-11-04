from flask import Flask, request, jsonify
app = Flask(__name__, static_url_path='/data', static_folder='data')

from dotenv import load_dotenv
load_dotenv()

""" configuration gemini """

import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

"""
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-002",
  generation_config=generation_config,
  system_instruction="J'aimerais avoir un système qui permet de valider et de vérifier si un cours est vraiment fait ou non . L'utilisateur insère une fiche de présence sous forme d'image et le système va récupérer la première ligne (la partie horizontale) du fiche où un nom d'étudiants est écrit et va compter le nombre de colonne où il y a une signature . Si il n'y a pas de signature alors il doit dire que la fiche est vide, dans le cas contraire il affiche le message cours vérifier. \nToutes les colonnes ne sont pas obligés d'être signé\n\nEn sortie, le système va récupérer la mention , le parcours, le niveau , le nom de la matière ainsi que la date de chaque signature (je ne veux pas avoir le nom des étudiants je veux juste avoir le nombre de colonne signée avec la date de chaque signature dans la réponse json, il doit prendre en compte si la colonne est vide ou non).\n\n Lorsque il a finit de compter les signatures et d'extraire les informations il va notifier si le cours est vraiment fait  ou non. \n\nLes conditions: \n- un cours possède un nombre de crédit, \n- un nombre de crédit dans une fiche de présence suit la règle suivante : \n 1 crédit correspond à 12h ,une colonne signée(la partie verticale) représente 4h donc 1 crédit correspond à 3 colonnes signés.\n\nA la fin du traitement, le système doit afficher le nombre de crédit du fiche de présence. si dans le cas contraire, le fiche de présence n'est pas signé, alors il doit afficher \"la fiche de présence est vide \"\n\nle système doit prendre en compte que la première ligne signée",
)
"""

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-002",
  generation_config=generation_config,
  system_instruction="J'aimerais créer un système qui permet de reconnaitre les élément sur une image.\n Le système doit renvoyer à quoi correspond l'élément sur la photo et ecrire le nom en français et en anglais . Si l'image correspond à plusieurs elements alors il envoie le mot englobant tous les elements. Je veux un seul mot par image et un mot facile pour les enfants",
)

"""
history=[
    {
      "role": "user",
      "parts": [
        upload_to_gemini("data/ok.jpeg", mime_type="image/jpeg"),
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"mention\": null, \"parcours\": \"GL\", \"niveau\": \"M2\", \"matiere\": null, \"nom_enseignant\": null, \"signatures\": [{\"date\": \"15/07/24\", \"colonne_signee\": true}, {\"date\": \"15/07/\", \"colonne_signee\": true}, {\"date\": \"16/07/24\", \"colonne_signee\": true}], \"cours_fait\": true, \"credit\": 1, \"message\": \"cours vérifié\"}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        upload_to_gemini("data/fpok.jpeg", mime_type="image/jpeg"),
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"mention\": \"Science de la société\", \"parcours\": \"GESTION\", \"niveau\": \"L3\", \"matiere\": \"Technique de négociation\", \"nom_enseignant\": \"Mme Saholinirina Borhel\", \"signatures\": [{\"date\": \"01/10/24\", \"colonne_signee\": true}, {\"date\": \"02/10/24\", \"colonne_signee\": true}, {\"date\": \"03/10/24\", \"colonne_signee\": true}, {\"date\": \"04/10/24\", \"colonne_signee\": true}, {\"date\": \"07/10/24\", \"colonne_signee\": true}, {\"date\": \"08/10/24\", \"colonne_signee\": true}, {\"date\": \"09/10/24\", \"colonne_signee\": true}, {\"date\": \"10/10/24\", \"colonne_signee\": true}], \"cours_fait\": true, \"credit\": 2, \"message\": \"cours vérifié\"}\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        upload_to_gemini("data/fp.jpeg", mime_type="image/jpeg"),
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"mention\": \"Science de la société\", \"parcours\": \"GESTION\", \"niveau\": \"L3\", \"matiere\": \"Technique de négociation\", \"nom_enseignant\": \"Mme Saholinirina Borhel\", \"signatures\": [{\"date\": \"01/10/24\", \"colonne_signee\": true}, {\"date\": \"02/10/24\", \"colonne_signee\": true}, {\"date\": \"03/10/24\", \"colonne_signee\": true}, {\"date\": \"04/10/24\", \"colonne_signee\": true}, {\"date\": \"07/10/24\", \"colonne_signee\": true}, {\"date\": \"08/10/24\", \"colonne_signee\": true}, {\"date\": \"09/10/24\", \"colonne_signee\": true}, {\"date\": \"10/10/24\", \"colonne_signee\": true}], \"cours_fait\": true, \"credit\": 2, \"message\": \"cours vérifié\"}\n\n\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        upload_to_gemini("data/Sans titre.jpg", mime_type="image/jpeg"),
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\"mention\": null, \"parcours\": null, \"niveau\": \"L3\", \"matiere\": \"Développement d'Application Intranet Internet\", \"nom_enseignant\": null, \"signatures\": [], \"cours_fait\": false, \"credit\": 0, \"message\": \"la fiche de présence est vide\"}\n\n\n```",
      ],
    },
  ]
"""

history=[
    {
      "role": "user",
      "parts": [
        upload_to_gemini("data/raisin.jpg", mime_type="image/jpeg"),
      ],
    },
    {
      "role": "model",
      "parts": [
        "Raisin / Grapes\n",
      ],
    },
    {
      "role": "user",
      "parts": [
         upload_to_gemini("data/pantalon.jpg", mime_type="image/jpeg"),
      ],
    },
    {
      "role": "model",
      "parts": [
        "Chien / Dog\n",
      ],
    },
    {
      "role": "user",
      "parts": [
  upload_to_gemini("data/fruits.jpg", mime_type="image/jpeg"),
      ],
    },
    {
      "role": "model",
      "parts": [
        "Fruits / Fruits\n",
      ],
    },
  ]