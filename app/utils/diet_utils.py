import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from openai import AsyncOpenAI
import os
import asyncio
from app.core.mongo_core import mongo_find_one, mongo_update_one, mongo_insert_one
from app.config.generic_conf import DIET_AI_MODEL
from datetime import datetime, timezone
from bson import ObjectId
import json
import re

from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

# Set up OpenAI API key
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def step_1_analisi_paziente(patient_data):
    info = {k:v for k,v in patient_data["personal_info"].items() if k in ['dob','motivo_visita','gender','altezza']}
    weight = {k:v for k,v in patient_data["weight_history"].items() if v is not None}
    diet_history = {k:v for k,v in patient_data["diet_history"].items() if v is not None}
    eating_habits = {k:v for k,v in patient_data["eating_habits"].items() if v is not None}
    supplements_and_drugs = {k:v for k,v in patient_data["supplements_and_drugs"].items() if v is not None}
    gut_health = {k:v for k,v in patient_data["gut_health"].items() if v is not None}
    stomach_health = {k:v for k,v in patient_data["stomach_health"].items() if v is not None}
    women_health = {k:v for k,v in patient_data["women_health"].items() if v is not None}
    medical_history = {k:v for k,v in patient_data["medical_history"].items() if v is not None}
    food_preferences = {k:v for k,v in patient_data["food_preferences"].items() if v is not None}
    smoking_sleep_stress = {k:v for k,v in patient_data["smoking_sleep_stress"].items() if v is not None}
    
    extra_command = """
        Stima il fabbisogno calorico giornaliero del paziente in base alla sua routine di allenamento ed all'intensità della giornata lavorativa. ecco alcune info utili
        Lunedì, Mercoledì, Venerdì
         Giornate di allenamento personale sala pesi + lavoro misto da casa 
         Obiettivo: energia e supporto muscolare, buon apporto di CHO (carboidrati)
        Kcal/die: circa 1800 kcal
        Distribuzione:
        Colazione alta (CHO + proteine)
        Pranzo alto (piatto completo e saziante)
        Cena leggera (verdure, proteine leggere, pochi carbo)

        Martedì - Giovedì
         Giornate molto attive, fuori casa, molte ore di lezione
         Obiettivo: prestazione + lucidità mentale + digestione leggera
        Kcal/die: circa 1600 kcal
        Distribuzione:
        Colazione alta (energia duratura)
        Pranzo medio, più proteine e grassi, pochi CHO (no "abbiocco")
        Cena alta (recupero serale, piatto più ricco)

        Sabato - Domenica
         Weekend di recupero attivo/passivo
         Obiettivo: scarico, detox, drenaggio, benessere digestivo
        Kcal/die: 1500-1600 kcal
        Filosofia alimentare:
        Pasti leggeri, ricchi di verdure, fibre, acque aromatizzate/detox
        Tisane drenanti, fermenti, infusi digestivi
        Meno sale, zero zuccheri raffinati
        Favorire cotture semplici (vapore, crudo, forno) 
    """
    
    if patient_data["personal_info"]['gender'] == "female":
        harris_benedict_calories = 655.095 + (9.563 * weight["peso_attuale"]) + (1.8496 * info["altezza"]) - (4.6756 * (2025 - int(info["dob"][:4])))
    else:
        harris_benedict_calories = 66.473 + (13.7516 * weight["peso_attuale"]) + (5.0033 * info["altezza"]) - (6.755 * (2025 - int(info["dob"][:4])))
    
    prompt = f"""
        Il paziente è una {info.get('gender', 'persona')} di {2025 - int(info['dob'][:4])} anni (nato il {info.get('dob', 'N/A')}). 
        È alto {info.get('altezza', 'N/A')} cm e pesa {weight.get('peso_attuale', 'N/A')} kg.

        Motivo della visita: {info.get('motivo_visita', 'non specificato')}.
        Stile di vita: {eating_habits.get('attivita_fisica', 'non specificato').lower()}.
        Professione: {info.get('professione', 'non specificata')}.
        Storia familiare: {medical_history.get('storia_familiare', 'non indicata')}.

        Mangia tipicamente {eating_habits.get('pasti_giornata_tipo', 'non indicato')} agli orari: {eating_habits.get('orari_frequenza_pasti', 'non specificati')}.
        Ha già seguito diete in passato? {diet_history.get('esperienze_dietetiche', 'non specificato')}.

        Fabbisogno calorico (Harris-Benedict): {harris_benedict_calories} kcal.

        Preferenze alimentari:
        - Cibi non graditi: {food_preferences.get('cibi_non_graditi', 'nessuno dichiarato')}.
        - Comfort food: {food_preferences.get('comfort_food', 'non specificato')}.

        Problemi digestivi segnalati:
        - Gonfiore da: {gut_health.get('alimenti_gonfiore', 'nessuno noto')}.
        - Fastidi allo stomaco da: {stomach_health.get('alimenti_fastidio', 'nessuno noto')}.

        Sonno: {smoking_sleep_stress.get('qualita_sonno', 'non indicata')}, stress: {smoking_sleep_stress.get('livello_stress', 'non indicato')}.
        Integrazioni o farmaci attuali: {supplements_and_drugs.get('integratori_farmaci', 'non segnalati')}.

        {f"Salute femminile: {women_health}" if women_health else ""}

        {extra_command}

        Stimami il fabbisogno calorico giornaliero, con una breve analisi nutrizionale basata su queste informazioni.
    """

    response = await client.chat.completions.create(
        model=DIET_AI_MODEL,
        messages=[
            {"role": "system", "content": "Sei un nutrizionista esperto che deve valutare l'anmnesi du un paziente."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    
    return response.choices[0].message.content.strip()

async def step_2_vincoli_dietetici(fabbisogno_output):
    prompt = f"""
        A partire dalla seguente analisi del paziente e fabbisogno nutrizionale:

        {fabbisogno_output}

        Definisci:
        - Tieni conto di eventuali indicazioni specifiche per i giorni della settimana.
        - Limiti giornalieri consigliati per carboidrati, zuccheri semplici, grassi saturi, proteine e fibra.
        - Linee guida alimentari: cosa privilegiare (es. legumi, cereali integrali), cosa evitare.
        - Indicazioni su varie patologie e condizioni fisiche da tenere in considerazione.
    """

    response = await client.chat.completions.create(
        model=DIET_AI_MODEL,
        messages=[
            {"role": "system", "content": "Sei un nutrizionista esperto che sta facendo una stima del fabbisogno del paziente al fine di creare una dieta."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    
    return response.choices[0].message.content.strip()

async def step_3_schema_giornaliero(vincoli_output):
    prompt = f"""
        Seguendo queste linee guida nutrizionali:

        {vincoli_output}

        Crea uno schema giornaliero con 3 pasti principali (colazione, pranzo, cena) e 2 spuntini, indicando:
        - Alimenti consigliati per ciascun pasto
        - Esempio di un pasto per ogni fascia
        - Grammature indicative
        - Ripartizione percentuale delle calorie
        - Voglio che gli spuntini siano un po' più sostanziosi ed i pasti un po' più leggeri    
        - Tieni conto di eventuali linee guida specifiche per i giorni della settimana
        - tieni conto di eventuali condimenti come olio, sale, aceto e spezie
    """

    response = await client.chat.completions.create(
        model=DIET_AI_MODEL,
        messages=[
            {"role": "system", "content": "Sei un nutrizionista specializzato in meal planning."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    
    return response.choices[0].message.content.strip()

async def step_4_menu_settimanale(schema_output):
    prompt = f"""
        Partendo da questo schema giornaliero:

        {schema_output}

        Crea un menu settimanale bilanciato. Il menu deve essere:
        - Variato (piatti diversi ogni giorno, ma puoi ripetere alcune colazioni o spuntini)
        - Basato su alimenti che seguano eventuali linee guida per patologie
        - Facile da preparare anche in viaggio o al lavoro
        - con alimenti di facile reperibilità
        - inserisci le ricette schematiche se il piatto non è autoesplicativo
        - Quantificato (grammature e calorie per ogni pasto)
        - tieni conto dei condimenti come olio, sale, aceto e spezie
    """

    response = await client.chat.completions.create(
        model=DIET_AI_MODEL,
        messages=[
            {"role": "system", "content": "Sei un dietista esperto in pianificazione settimanale."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )
    
    return response.choices[0].message.content.strip()

async def step_5_esporta_menu(menu_output, formato="json"):
    prompt = f"""
        Trasforma il seguente menu settimanale in un JSON strutturato.

        La struttura JSON deve essere esattamente la seguente, senza modifiche:

        {{
        "menu_settimanale": {{
            "giorno_della_settimana": {{
            "colazione": {{
                "nome": "nome del piatto",
                "ingredienti": [
                {{
                    "nome": "ingrediente",
                    "grammature": "quantità",
                    "calorie": numero
                }}
                ],
                "calorie_stimate": numero
            }},
            "spuntino_mattina": {{ ... }},
            "pranzo": {{ ... }},
            "spuntino_pomeriggio": {{ ... }},
            "cena": {{ ... }}
            }}
        }}
        }}

        Per ogni **giorno** della settimana (lunedì, martedì, mercoledì, giovedì, venerdì, sabato, domenica), devono essere presenti **tutti e 5 i pasti**: colazione, spuntino_mattina, pranzo, spuntino_pomeriggio, cena.

        Per ogni pasto devi fornire:
        - il campo "nome" (nome del piatto),
        - la lista "ingredienti", con per ogni ingrediente:
        - "nome" (es: "banana"),
        - "grammature" (quantità espressa in grammi o millilitri),
        - "calorie" (numero stimato delle calorie),
        - il campo "calorie_stimate" (numero stimato delle calorie totali del pasto).

        Se le grammature o calorie non sono specificate nel testo, inferiscile in modo ragionevole in base agli ingredienti.

        **Importante:**
        - Non aggiungere testi, commenti o spiegazioni fuori dal JSON.
        - Non cambiare la struttura del JSON richiesta.

        Menu:

        {menu_output}   
    """


    response = await client.chat.completions.create(
        model=DIET_AI_MODEL,
        messages=[
            {"role": "system", "content": "Converte il menu settimanale in un JSON strutturato secondo le istruzioni."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        response_format={ "type": "json_object" } 
    )
    
    return response.choices[0].message.content

async def make_diet(patient_id):
    # Fetch user data from MongoDB
    patient_data = await mongo_find_one("patients", {"_id": ObjectId(patient_id)})
    
    if not patient_data:
        print("User data not found.")
        return

    # Generate the diet plan
    t0 = datetime.now()
    step1 = await step_1_analisi_paziente(patient_data)
    t1 = datetime.now()
    print(f"Tempo analisi paziente: {t1 - t0}")
    step2 = await step_2_vincoli_dietetici(step1)
    t2 = datetime.now()
    print(f"Tempo valutazione vincoli dietetici: {t2 - t1}")
    step3 = await step_3_schema_giornaliero(step2)
    t3 = datetime.now()
    print(f"Tempo generazione schema giornaliero: {t3 - t2}")
    step4 = await step_4_menu_settimanale(step3)
    t4 = datetime.now()
    print(f"Tempo creazione menu settimanale: {t4 - t3}")
    diet_plan = await step_5_esporta_menu(step4, formato="json")
    t5 = datetime.now()
    print(f"Tempo esportazione menu in formato json: {t5 - t4}")
    print(f"Tempo totale generazione dieta: {t5 - t0}")
    
    
    # Insert the diet plan into the "diets" collection
    diet_document = {
        "patient_id": patient_id,
        "patient_analysis": step1,
        "diet_boundaries": step2,
        "daily_schema": step3,
        "weekly_menu": step4,
        "diet_plan_json": json.loads(re.sub(r"```(?:json)?\n?|\n```", "", diet_plan).strip()),
        "created_at": datetime.now(timezone.utc) 
    }
    diet_insert_result = await mongo_insert_one(
        "diets",
        diet_document
    )

    if diet_insert_result and diet_insert_result.inserted_id:
        update_result = await mongo_update_one(
            "patients",
            {"_id": ObjectId(patient_id)},
            {"$set": {"diet_id": diet_insert_result.inserted_id}}
        )
    else:
        print("Failed to insert the diet plan into the 'diets' collection.")
        return
    
    if update_result and update_result.modified_count > 0:
        print("Diet plan successfully updated in the database.")
    else:
        print("Failed to update the diet plan in the database.")
        
    return diet_insert_result.inserted_id

async def generate_diet_pdf(diet_id):
    diet_data = await mongo_find_one("diets", {"_id": ObjectId(diet_id)})

    if not diet_data or 'diet_plan_json' not in diet_data:
        print('Document not found or missing "diet_plan_json" key.')
        return

    # Extract the diet plan
    menu_settimanale = diet_data['diet_plan_json']['menu_settimanale']

    env = Environment(loader=FileSystemLoader('/home/alessio/nutribot/app/models'))
    template = env.get_template("diet_pdf_template.html")

    # 3. Render HTML
    rendered_html = template.render(menu_settimanale=menu_settimanale)

    # 4. Esporta come PDF
    output_path = f"/home/alessio/nutribot/data/diet_plan_{diet_id}.pdf"
    HTML(string=rendered_html).write_pdf(output_path)
    print(f"PDF generated successfully at {output_path}")    
    
if __name__ == "__main__":
    patient_id = "67f66a543387c752d861e18a"
    loop = asyncio.get_event_loop()
    diet_id = loop.run_until_complete(make_diet(patient_id))
    if diet_id:
        loop.run_until_complete(generate_diet_pdf(diet_id))
