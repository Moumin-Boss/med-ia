import os
import streamlit as st
import fitz
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="MED IA", page_icon="✚", layout="wide")

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
MAX_CHARS = 45000

def extract_pdf(uploaded_file):
    data = uploaded_file.getvalue()
    doc = fitz.open(stream=data, filetype="pdf")
    pages = []
    for i, page in enumerate(doc):
        txt = page.get_text("text").strip()
        if txt:
            pages.append({"page": i + 1, "text": txt})
    return pages

def get_client():
    key = st.secrets.get("GEMINI_API_KEY", None) if hasattr(st, "secrets") else None
    key = key or os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    return genai.Client(api_key=key)

def document_context(pages):
    chunks = []
    for p in pages:
        chunks.append(f"[Page {p['page']}]\n{p['text']}")
    return "\n\n".join(chunks)[:MAX_CHARS]

def ask_ai(prompt, context):
    client = get_client()
    if client is None:
        raise RuntimeError("Clé API Gemini manquante. Ajoute GEMINI_API_KEY dans le fichier .env.")
    full_prompt = f"""
Tu es MED IA, un assistant documentaire et pédagogique en santé.
Règles impératives :
- Utilise prioritairement le document fourni.
- N'invente jamais une citation, une page, une recommandation ou une référence.
- Si le document ne contient pas la réponse, dis-le clairement.
- Distingue les informations du document de tes connaissances générales.
- Il s'agit d'un outil éducatif, pas d'un dispositif de diagnostic ou de prescription.
- Réponds en français clair, structuré et adapté à des étudiants et professionnels de santé.
- Quand tu utilises le document, indique les numéros de pages entre crochets, par exemple [Page 3].

DOCUMENT FOURNI :
{context}

DEMANDE :
{prompt}
"""
    response = client.models.generate_content(model=MODEL, contents=full_prompt)
    return response.text or "Aucune réponse textuelle reçue."

st.markdown("""
<div style="padding:8px 0 14px 0">
  <div style="font-size:30px;font-weight:800;letter-spacing:-1px">✚ MED IA</div>
  <div style="color:gray">Medical Learning & Documentation Assistant</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("MED IA")
    st.caption("Prototype V1 · Démonstration")
    st.markdown("---")
    st.markdown("**Modules disponibles**")
    st.markdown("- Analyse de cours PDF\n- Fiches de révision\n- QCM corrigés\n- Questions-réponses")
    st.markdown("---")
    st.caption(f"Modèle configuré : `{MODEL}`")
    st.caption("Ne téléverse pas de données nominatives ou confidentielles de patients.")

st.info("MED IA est un outil pédagogique expérimental. Toute information médicale doit être vérifiée dans des références fiables et les protocoles locaux.")

uploaded = st.file_uploader("Importer un cours médical au format PDF", type=["pdf"])

if uploaded:
    try:
        pages = extract_pdf(uploaded)
        if not pages:
            st.error("Aucun texte n'a été extrait. Le PDF est peut-être un scan image. L'OCR sera ajouté dans une prochaine version.")
            st.stop()
        context = document_context(pages)
        st.success(f"Document chargé : {uploaded.name} · {len(pages)} page(s) contenant du texte.")
        with st.expander("Aperçu du texte extrait"):
            st.text(context[:5000] + ("\n\n[Extrait tronqué pour l'aperçu]" if len(context) > 5000 else ""))
        st.caption(f"Le moteur utilise jusqu'à {MAX_CHARS:,} caractères du document dans cette version.")

        tabs = st.tabs(["📝 Fiche de révision", "☑ Générateur de QCM", "💬 Poser une question"])

        with tabs[0]:
            st.subheader("Créer une fiche de révision")
            level = st.selectbox(
                "Niveau de détail",
                ["Simple et synthétique", "Intermédiaire", "Approfondi"]
            )

            structure = st.selectbox(
                "Choisir la structure de ma fiche",
                [
                    "Fiche classique",
                    "Fiche approfondie",
                    "Fiche synthétique",
                    "Fiche personnalisée"
                ]
            )

            structure_sections = {
                "Fiche classique": [
                    "Définition et généralités",
                    "Causes et facteurs de risque",
                    "Signes cliniques",
                    "Diagnostic",
                    "Prise en charge"
                ],
                "Fiche approfondie": [
                    "Définition et généralités",
                    "Épidémiologie",
                    "Causes et facteurs de risque",
                    "Physiopathologie expliquée étape par étape",
                    "Signes cliniques",
                    "Examens complémentaires",
                    "Diagnostic positif",
                    "Diagnostics différentiels",
                    "Prise en charge",
                    "Complications et suivi"
                ],
                "Fiche synthétique": [
                    "Définitions essentielles",
                    "Points clés à retenir",
                    "Tableau récapitulatif",
                    "Pièges et erreurs à éviter"
                ]
            }

            if structure == "Fiche personnalisée":
                available_sections = [
                    "Définition et généralités",
                    "Épidémiologie",
                    "Causes et facteurs de risque",
                    "Physiopathologie",
                    "Signes cliniques",
                    "Examens complémentaires",
                    "Diagnostic positif",
                    "Diagnostics différentiels",
                    "Prise en charge",
                    "Complications et suivi",
                    "Tableaux récapitulatifs",
                    "Points clés à retenir",
                    "Pièges et erreurs à éviter",
                    "Questions pour vérifier ma compréhension"
                ]
                selected_sections = st.multiselect(
                    "Sélectionne les rubriques à inclure",
                    available_sections,
                    default=[
                        "Définition et généralités",
                        "Physiopathologie",
                        "Signes cliniques",
                        "Diagnostic positif",
                        "Prise en charge",
                        "Points clés à retenir"
                    ]
                )
            else:
                selected_sections = structure_sections[structure]
                st.caption("Rubriques prévues : " + " · ".join(selected_sections))

            focus = st.text_input(
                "Point particulier à privilégier (facultatif)",
                placeholder="Ex. physiopathologie, diagnostic, traitement..."
            )

            if st.button("Générer ma fiche", type="primary", key="summary"):
                if not selected_sections:
                    st.warning("Sélectionne au moins une rubrique pour créer ta fiche.")
                else:
                    with st.spinner("MED IA analyse le document..."):
                        try:
                            sections_text = "\n".join(f"- {section}" for section in selected_sections)
                            prompt = f"""Crée une fiche de révision de niveau {level}.
Respecte cette structure et conserve exactement l'ordre des rubriques :
{sections_text}

Consignes :
- Développe chaque rubrique uniquement avec les informations présentes dans le document.
- Si une rubrique n'est pas abordée dans le document, indique clairement : « Non précisé dans le document ».
- Explique les mécanismes de façon progressive et compréhensible lorsque la rubrique physiopathologie est sélectionnée.
- Utilise des tableaux lorsque cela facilite la mémorisation.
- Termine par les points essentiels si cette rubrique a été sélectionnée.
- Ajoute les numéros de pages sources pour les informations extraites.
- N'invente ni donnée, ni recommandation, ni référence.

Point particulier à privilégier : {focus or 'aucun'}."""
                            st.markdown(ask_ai(prompt, context))
                        except Exception as e:
                            st.error(f"Erreur lors de la génération : {e}")

        with tabs[1]:
            st.subheader("Générer des QCM")
            number = st.slider("Nombre de questions", 5, 20, 10)
            difficulty = st.selectbox("Difficulté", ["Facile", "Intermédiaire", "Difficile", "Progressive"])
            if st.button("Générer les QCM", type="primary", key="qcm"):
                with st.spinner("Préparation des questions..."):
                    try:
                        prompt = f"""Crée {number} QCM de difficulté {difficulty} exclusivement à partir du document.
Pour chaque question :
- propose 4 ou 5 choix A à E ;
- précise s'il y a une ou plusieurs bonnes réponses ;
- donne la correction après les questions ;
- explique chaque proposition ;
- indique la ou les pages sources.
N'ajoute aucune information absente du document."""
                        st.markdown(ask_ai(prompt, context))
                    except Exception as e:
                        st.error(f"Erreur lors de la génération : {e}")

        with tabs[2]:
            st.subheader("Assistant documentaire")
            question = st.text_area("Ta question", placeholder="Ex. Explique la physiopathologie de cette maladie...", height=110)
            if st.button("Envoyer ma question", type="primary", key="ask"):
                if not question.strip():
                    st.warning("Écris d'abord une question.")
                else:
                    with st.spinner("Recherche dans le document et préparation de la réponse..."):
                        try:
                            st.markdown(ask_ai(question, context))
                        except Exception as e:
                            st.error(f"Erreur lors de la génération : {e}")
    except Exception as e:
        st.error(f"Impossible de lire ce PDF : {e}")
else:
    st.markdown("### Comment commencer ?")
    st.markdown("1. Sélectionne un cours médical PDF.\n2. Choisis une fonction : fiche, QCM ou question.\n3. Vérifie les réponses avec ton cours et les références officielles.")
    st.markdown("### Ce que contient cette première version")
    c1, c2, c3 = st.columns(3)
    c1.metric("Modules", "3")
    c2.metric("Format accepté", "PDF")
    c3.metric("Langue", "Français")
    st.warning("Pour utiliser les fonctions IA, une clé API Gemini est nécessaire. Le mode sans clé permet de lancer l'interface, mais pas de générer des réponses.")

st.markdown("---")
st.caption("MED IA · Assistant pédagogique médical · Version 1.1")
