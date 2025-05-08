import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from airtable import Airtable

# Configuration from Environment Variables
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME", "SAISIE DE LIVRES")

# Field names from Airtable (must match exactly)
FIELD_EAN = "EAN"
FIELD_ETAT = "ETAT"
FIELD_RAYON = "RAYON"
FIELD_SOUS_RAYON = "sous rayon" # Assumed name, user confirmed
FIELD_PRIX_MINI = "PRIX MINI"    # User confirmed
FIELD_PRIX_MAXI = "PRIX MAXI"    # User confirmed

# --- Airtable Client Initialization ---
try:
    airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, api_key=AIRTABLE_API_KEY)
    print(f"Airtable client initialized for table: {AIRTABLE_TABLE_NAME}")
except Exception as e:
    print(f"Error initializing Airtable client: {e}")
    airtable = None

# --- Flask App Initialization ---
# Serve static files from 'static' and templates from 'templates'
app = Flask(__name__, static_folder="static", template_folder="templates")

# --- Helper Function to get Dropdown Options ---
def get_dropdown_options(field_name):
    if field_name == FIELD_ETAT:
        # Predefined list for ETAT, as per previous app logic
        return ["EC", "BE", "TB", "CN", "NE"]
    elif field_name == FIELD_RAYON:
        # Predefined list for RAYON, sorted, as per previous app logic
        rayons = [
            "psychanalyse", "histoire", "Jeunesse", "psychologie", "Politinternatio", "art",
            "Sciencespol", "poesie", "Sociologie", "Objetscoll", "Cuisine", "Ethnologie",
            "Economie", "Philosophie", "musique", "Mer", "Quesaisje", "Poche",
            "Classiquespoche", "Esoterisme", "Essais", "Bouddhisme", "Religion", "Romans",
            "Bd", "photographie", "Dictionnaire", "critiqlitt", "Scolaire", "educ",
            "pochehistoire", "Poches", "pochessciences", "litterature", "Droit", "sf",
            "archeologie", "Regionalisme", "Medecine", "Animaux", "corresponda",
            "cinémaacteuramér", "style", "musiquechantgroupes", "Ecologiequotid",
            "bienetre", "Communisme", "sexualité", "politiqfra", "Sciences", "judaisme",
            "mondearabe", "romananglaisssol", "erotique", "Biographies", "Geographie",
            "collbouquins", "paysmonaco", "spiritualite", "greceantiq", "mythologie",
            "cinessais", "edition", "pleiade", "apprentissageanglais", "ange", "cinema",
            "folklore", "tablactusssol", "Architecture", "theatre", "revueslitt",
            "pedagogie", "tableactu", "medecinenaturelle", "savoirvivre", "paysafrique",
            "aviation", "vitrineregio", "justice", "linguistique", "jeandebonnot",
            "pochepolicier", "romanspolicierbroch", "theologie", "Pressejournalism",
            "biographie", "Sport", "bricolage", "Europe", "nationalisme", "Danse",
            "Techniques", "Espagne", "societe", "anthropologie", "latinpoche", "Jeux",
            "voyage", "femme", "adolescence", "pochepolitique", "autobiographie",
            "Communication", "antiquite", "Concours", "Guides", "algerie", "montagne",
            "lettres", "journauxsouvenirs", "asie", "entreprise", "maternité", "humour",
            "parentalite", "financepublique", "dietetique", "psychiatrie", "ameriquelatine",
            "Prostitution", "Acteurs", "grec", "puericulture", "vitrinefacecaisse",
            "Dictionnaires", "trains", "automoto", "francmaconnerie", "Brocante",
            "fantastique", "media", "Geopolitique", "Societessecretes",
            "francaispouretranger", "langue russe", "paris", "moyen orient", "fantasy",
            "revue philosophie", "pays", "templiers", "manga", "Viesquotidiennes",
            "Botanique", "Vin", "Graphologie", "Afriquedunord", "alchimie",
            "Bellesreliuresromanpop", "Objetscollectimbres", "languarabe",
            "editionoriginale", "methodenicois", "romanpopulaire", "VOalld", "astronomie",
            "philopolitique", "epistemologie", "englishbooks", "methodelangueital",
            "VOangloessais", "romanvoyage", "regionparis", "methodelangueespagnol",
            "champignon", "nature", "vousheros", "def", "Couple", "informatique",
            "Racisme", "biologie", "2dguerre", "DeGaulle", "classiqanglais",
            "sciencespolit", "chimie", "yoga", "methodelangue", "scolaireancien",
            "plantes", "peintresvallotton", "langnissart", "préhistoire",
            "relationsinternational"
        ]
        rayons.sort(key=str.lower)
        return rayons
    return []

# --- Flask Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route("/get_form_options", methods=["GET"])
def get_form_options():
    try:
        etat_options = get_dropdown_options(FIELD_ETAT)
        rayon_options = get_dropdown_options(FIELD_RAYON)
        return jsonify({"etats": etat_options, "rayons": rayon_options})
    except Exception as e:
        print(f"Error in /get_form_options: {e}")
        return jsonify({"etats": [], "rayons": []}), 500

@app.route("/add_book_entry_form", methods=["POST"])
def add_book_entry_form():
    if not airtable:
        return jsonify({"message": "Erreur: Connexion Airtable non initialisée."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"message": "Erreur: Aucune donnée reçue."}), 400

    ean = data.get("ean")
    etat = data.get("etat")
    rayon = data.get("rayon")
    sous_rayon = data.get("sous_rayon", "N/A") # Default to N/A if empty
    prix_mini_str = data.get("prix_mini")
    prix_maxi_str = data.get("prix_maxi")

    if not ean or not etat or not rayon:
        return jsonify({"message": "Erreur: EAN, État et Rayon sont requis."}), 400
    
    if not (isinstance(ean, str) and len(ean) == 13 and ean.isdigit()):
        return jsonify({"message": f"Erreur: Format EAN invalide ({ean}). Il doit contenir 13 chiffres."}), 400

    record_data = {
        FIELD_EAN: ean,
        FIELD_ETAT: etat,
        FIELD_RAYON: rayon,
        FIELD_SOUS_RAYON: sous_rayon
    }

    try:
        if prix_mini_str is not None:
            record_data[FIELD_PRIX_MINI] = float(prix_mini_str)
        if prix_maxi_str is not None:
            record_data[FIELD_PRIX_MAXI] = float(prix_maxi_str)
    except ValueError:
        return jsonify({"message": "Erreur: PRIX MINI et PRIX MAXI doivent être des nombres valides."}), 400
    
    if FIELD_PRIX_MINI in record_data and FIELD_PRIX_MAXI in record_data and record_data[FIELD_PRIX_MINI] > record_data[FIELD_PRIX_MAXI]:
        return jsonify({"message": "Erreur: Le PRIX MINI ne peut pas être supérieur au PRIX MAXI."}), 400

    print(f"DEBUG: Attempting to insert into Airtable: {record_data}")

    try:
        created_record = airtable.insert(record_data)
        record_id = created_record.get("id", "N/A")
        print(f"Airtable record created: {record_id} for EAN {ean}")
        return jsonify({"message": f"Livre (EAN: {ean}) ajouté avec succès!"}), 201
    except Exception as e:
        error_message = str(e)
        print(f"Error adding record to Airtable for EAN {ean}: {error_message}")
        # More specific error handling based on Airtable's response
        if "INVALID_VALUE_FOR_COLUMN" in error_message:
            return jsonify({"message": f"Erreur Airtable: Valeur invalide pour une colonne. Vérifiez les options pour État/Rayon ou le format des prix."}), 400
        elif "UNKNOWN_FIELD_NAME" in error_message:
            return jsonify({"message": f"Erreur Airtable: Nom de champ inconnu. Vérifiez la configuration des champs dans Airtable."}), 500
        else:
            return jsonify({"message": f"Erreur interne lors de l\'ajout à Airtable: {error_message}"}), 500

# --- Main Execution ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002)) # Using a different port, e.g., 5002
    app.run(debug=False, host="0.0.0.0", port=port)

