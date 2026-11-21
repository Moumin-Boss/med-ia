MEDIA AI — PROTOTYPE V1
=======================

CE QUE FAIT CETTE VERSION
- Importer un cours PDF contenant du texte sélectionnable.
- Extraire le texte du PDF.
- Générer une fiche de révision.
- Générer des QCM corrigés.
- Poser des questions sur le document avec indication des pages utilisées.

PRÉREQUIS
- Un ordinateur Windows, macOS ou Linux.
- Internet.
- Python 3.10 ou plus récent.
- Une clé API Gemini (voir plus bas).

INSTALLATION WINDOWS — ÉTAPES SIMPLES
1. Décompresse MEDIA_AI_V1.zip dans un dossier facile à retrouver.
2. Installe Python depuis https://www.python.org/downloads/
   Pendant l'installation Windows, coche "Add Python to PATH".
3. Ouvre le dossier MEDIA_AI_V1.
4. Clique dans la barre d'adresse de l'Explorateur Windows, tape cmd puis Entrée.
5. Dans la fenêtre noire, exécute ces commandes une par une :

   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt

CONFIGURER LA CLÉ GEMINI
1. Ouvre https://aistudio.google.com/app/apikey
2. Connecte-toi à ton compte Google et crée une clé API.
3. Dans le dossier du projet, copie le fichier .env.example.
4. Renomme la copie en .env (sans .example).
5. Ouvre .env avec le Bloc-notes.
6. Après GEMINI_API_KEY= colle ta clé, sans guillemets.
7. Enregistre et ferme.

IMPORTANT : ne partage jamais ta clé API, ne la publie pas sur GitHub et ne l'envoie pas dans une capture d'écran.

LANCER MEDIA AI
Dans la même fenêtre noire, exécute :

   streamlit run app.py

Le navigateur devrait ouvrir MEDIA AI automatiquement.
Si ce n'est pas le cas, copie l'adresse locale affichée (souvent http://localhost:8501) dans ton navigateur.

ARRÊTER L'APPLICATION
Dans la fenêtre noire, appuie sur CTRL + C.

TEST CONSEILLÉ
- Utilise d'abord un cours PDF non confidentiel.
- Essaie une fiche de révision.
- Génère 5 QCM.
- Pose une question dont la réponse figure clairement dans le cours.
- Vérifie les pages citées dans le document original.

LIMITES DE LA V1
- Les PDF scannés comme des images ne sont pas encore lus (OCR à ajouter).
- Les références PubMed/OMS ne sont pas encore recherchées automatiquement.
- L'application utilise le texte du PDF importé ; elle ne constitue pas une base médicale complète.
- Le contexte transmis au modèle est limité à environ 45 000 caractères.
- L'API Gemini peut appliquer des quotas et limites d'utilisation qui changent selon le compte et le modèle.
- Une clé API gratuite n'est pas une garantie d'accès illimité. Vérifie les conditions et tarifs officiels.

CONFIDENTIALITÉ ET SÉCURITÉ
- Ne téléverse aucune donnée nominative, dossier patient identifiable ou document confidentiel.
- Le texte extrait du cours est envoyé à l'API Gemini lorsque tu demandes une génération.
- Vérifie les règles de confidentialité et les conditions de traitement de Google avant tout usage avec des documents sensibles.
- Les réponses peuvent contenir des erreurs. Vérifie toujours les informations médicales avec les sources originales et les protocoles locaux.
- MEDIA AI est un outil éducatif, pas un dispositif médical, un outil de diagnostic ou de prescription.

LIENS UTILES
Python : https://www.python.org/downloads/
Google AI Studio : https://aistudio.google.com/app/apikey
Documentation Gemini : https://ai.google.dev/gemini-api/docs
Streamlit : https://docs.streamlit.io/
