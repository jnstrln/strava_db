#!/usr/bin/env python3
"""Module docstring"""

import csv
import sys
from datetime import datetime
import emoji
from db_config import CONFIG
from db_connection import db_connection

def init_activities_table(connection):
    """Initialisation de la table activities."""

    drop_table_query = """
    DROP TABLE IF EXISTS activities CASCADE;
    """
    with connection.cursor() as drop_table_cursor:
        drop_table_cursor.execute(drop_table_query)
        connection.commit()

    create_table_query = """
    CREATE TABLE activities (
        id BIGINT PRIMARY KEY,
        date TIMESTAMP,
        nom TEXT,
        type_activite TEXT,
        description TEXT,
        note_privee TEXT,
        materiel_utilise TEXT,
        nom_fichier TEXT,
        poids_athlete FLOAT,
        poids_velo FLOAT,
        temps_ecoule FLOAT,
        duree_deplacement FLOAT,
        distance FLOAT,
        vitesse_max FLOAT,
        vitesse_moyenne FLOAT,
        denivele_positif FLOAT,
        denivele_negatif FLOAT,
        altitude_min FLOAT,
        altitude_max FLOAT,
        pente_max FLOAT,
        pente_moyenne FLOAT,
        pente_positive_moyenne FLOAT,
        pente_negative_moyenne FLOAT,
        cadence_max FLOAT,
        cadence_moyenne FLOAT,
        frequence_cardiaque_max FLOAT,
        frequence_cardiaque_moyenne FLOAT,
        puissance_max FLOAT,
        puissance_moyenne FLOAT,
        calories FLOAT,
        temperature_max FLOAT,
        temperature_moyenne FLOAT,
        effort_relatif FLOAT,
        effort_total FLOAT,
        nb_sorties_course_a_pied INTEGER,
        temps_montee FLOAT,
        temps_descente FLOAT,
        autres_temps FLOAT,
        effort_ressenti FLOAT,
        type TEXT,
        heure_debut FLOAT,
        puissance_moyenne_ponderee FLOAT,
        nb_echantillons_puissance INTEGER,
        utiliser_effort_ressenti BOOLEAN,
        effort_relatif_ressenti FLOAT,
        deplacement_transport BOOLEAN,
        poids_total_souleve FLOAT,
        a_partir_du_telechargement BOOLEAN,
        distance_ajustee_pente FLOAT,
        heure_observation_meteo FLOAT,
        conditions_meteo TEXT,
        temperature_previsions_meteo FLOAT,
        temperature_ressentie FLOAT,
        point_rosee TEXT,
        humidite FLOAT,
        pression_atmospherique FLOAT,
        vitesse_vent FLOAT,
        rafale_vent TEXT,
        direction_vent TEXT,
        intensite_precipitations TEXT,
        heure_lever_soleil FLOAT,
        heure_coucher_soleil FLOAT,
        phase_lune TEXT,
        velo FLOAT,
        materiel TEXT,
        proba_precipitations FLOAT,
        type_precipitations TEXT,
        couverture_nuageuse TEXT,
        visibilite_previsions_meteo TEXT,
        indice_uv FLOAT,
        ozone_previsions_meteo FLOAT,
        nb_sauts INTEGER,
        grit_total FLOAT,
        flow_moyen FLOAT,
        signale BOOLEAN,
        vitesse_moyenne_temps_ecoule FLOAT,
        distance_sur_chemin FLOAT,
        distance_recemment_decouverte FLOAT,
        distance_sur_chemin_recemment_decouverte FLOAT,
        nb_activites INTEGER,
        nb_total_pas BIGINT,
        co2_economise FLOAT,
        longueur_piscine FLOAT,
        charge_entrainement FLOAT,
        intensite FLOAT,
        vitesse_moyenne_ajustee_pente FLOAT,
        temps_chrono FLOAT,
        nb_total_cycles INTEGER,
        recuperation BOOLEAN,
        avec_animal BOOLEAN,
        competition BOOLEAN,
        sortie_longue BOOLEAN,
        pour_bonne_cause BOOLEAN,
        avec_enfant BOOLEAN,
        distance_descente FLOAT,
        nb_series INTEGER,
        nb_repetitions INTEGER,
        support TEXT
    );
    """

    with connection.cursor() as create_table_cursor:
        create_table_cursor.execute(create_table_query)
        connection.commit()

def remove_emojis(text):
    "Retire les emojis."
    return emoji.replace_emoji(text, replace='.')

def parse_date(value):

    if not value:
        return None

    months = {
        'janv.': 'Jan',
        'févr.': 'Feb',
        'mars': 'Mar',
        'avr.': 'Apr',
        'mai': 'May',
        'juin': 'Jun',
        'juil.': 'Jul',
        'août': 'Aug',
        'sept.': 'Sep',
        'oct.': 'Oct',
        'nov.': 'Nov',
        'déc.': 'Dec'
    }

    value = value.replace(",", "")

    for fr, en in months.items():
        value = value.replace(fr, en)

    formats = [
        "%d %b %Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass

    print(f"Unknown date format: {value}")

    return None

def parse_float(value):

    if value in (None, "", "--"):
        return None

    value = str(value).replace(",", ".")

    try:
        return float(value)
    except ValueError:
        print(f"Invalid float: {value}")
        return None

def parse_int(value):

    if value in (None, "", "--"):
        return None

    try:
        return int(float(str(value).replace(",", ".")))
    except ValueError:
        print(f"Invalid int: {value}")
        return None

def parse_bool(value):

    if value is None:
        return False

    return str(value).strip().lower() in (
        "true",
        "1",
        "yes",
        "oui",
        "vrai"
    )

def convert_row(row, ints, dates, floats, bools, strs):
    """
    Convertit les types des champs dans une ligne d'activité en fonction de leurs types attendus.
    """
    for field in ints:
        row[field] = parse_int(row[field])
    for field in dates:
        row[field] = parse_date(row[field])
    for field in floats:
        row[field] = parse_float(row[field])
    for field in bools:
        row[field] = parse_bool(row[field])
    for field in strs:
        if row.get(field):
            row[field] = str(remove_emojis(row[field]))
        else:
            row[field] = None
    return row

def insert_strava_data(connection):
    """Insertion des données du csc dans la table activities."""
    with open(CONFIG.activities_path, 'r', encoding='utf-8') as file:
        activities = csv.DictReader(file)

        insert_query = """
        INSERT INTO activities (
            id,
            date,
            nom,
            type_activite,
            description,
            note_privee,
            materiel_utilise,
            nom_fichier,
            poids_athlete,
            poids_velo,
            temps_ecoule,
            duree_deplacement,
            distance,
            vitesse_max,
            vitesse_moyenne,
            denivele_positif,
            denivele_negatif,
            altitude_min,
            altitude_max,
            pente_max,
            pente_moyenne,
            pente_positive_moyenne,
            pente_negative_moyenne,
            cadence_max,
            cadence_moyenne,
            frequence_cardiaque_max,
            frequence_cardiaque_moyenne,
            puissance_max,
            puissance_moyenne,
            calories,
            temperature_max,
            temperature_moyenne,
            effort_relatif,
            effort_total,
            nb_sorties_course_a_pied,
            temps_montee,
            temps_descente,
            autres_temps,
            effort_ressenti,
            type,
            heure_debut,
            puissance_moyenne_ponderee,
            nb_echantillons_puissance,
            utiliser_effort_ressenti,
            effort_relatif_ressenti,
            deplacement_transport,
            poids_total_souleve,
            a_partir_du_telechargement,
            distance_ajustee_pente,
            heure_observation_meteo,
            conditions_meteo,
            temperature_previsions_meteo,
            temperature_ressentie,
            point_rosee,
            humidite,
            pression_atmospherique,
            vitesse_vent,
            rafale_vent,
            direction_vent,
            intensite_precipitations,
            heure_lever_soleil,
            heure_coucher_soleil,
            phase_lune,
            velo,
            materiel,
            proba_precipitations,
            type_precipitations,
            couverture_nuageuse,
            visibilite_previsions_meteo,
            indice_uv,
            ozone_previsions_meteo,
            nb_sauts,
            grit_total,
            flow_moyen,
            signale,
            vitesse_moyenne_temps_ecoule,
            distance_sur_chemin,
            distance_recemment_decouverte,
            distance_sur_chemin_recemment_decouverte,
            nb_activites,
            nb_total_pas,
            co2_economise,
            longueur_piscine,
            charge_entrainement,
            intensite,
            vitesse_moyenne_ajustee_pente,
            temps_chrono,
            nb_total_cycles,
            recuperation,
            avec_animal,
            competition,
            sortie_longue,
            pour_bonne_cause,
            avec_enfant,
            distance_descente,
            nb_series,
            nb_repetitions,
            support
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """

        ints = [
            "ID de l'activité",
            "Nombre de sorties course à pied",
            "Nombre d'échantillons de puissance",
            "Nombre de sauts",
            "Nombre d'activités",
            "Nombre total de pas",
            "Nombre total de cycles",
            "Nombre total de séries",
            "Nombre total de répétitions"
        ]

        dates = [
            "Date de l'activité"
        ]

        floats = [
            "Poids de l'athlète",
            "Poids du vélo",
            "Temps écoulé",
            "Durée de déplacement",
            "Distance",
            "Vitesse max.",
            "Vitesse moyenne",
            "Dénivelé positif",
            "Dénivelé négatif",
            "Altitude min.",
            "Altitude max.",
            "Pente max.",
            "Pente moyenne",
            "Pente positive moyenne",
            "Pente négative moyenne",
            "Cadence max.",
            "Cadence moyenne",
            "Fréquence cardiaque max.",
            "Fréquence cardiaque moyenne",
            "Puissance max.",
            "Puissance moyenne",
            "Calories",
            "Température max.",
            "Température moyenne",
            "Effort relatif",
            "Effort total",
            "Temps de montée",
            "Temps de descente",
            "Autres temps",
            "Effort ressenti",
            "Puissance moyenne pondérée",
            "Effort relatif ressenti",
            "Poids total soulevé",
            "Distance ajustée selon la pente",
            "Température selon les prévisions météo",
            "Température ressentie",
            "Humidité",
            "Pression atmosphérique",
            "Vitesse du vent",
            "Vélo",
            "Probabilité de précipitations",
            "Indice UV",
            "Ozone selon les prévisions météo",
            "Grit total",
            "Flow moyen",
            "Vitesse moyenne (temps écoulé)",
            "Distance sur chemin",
            "Distance récemment découverte",
            "Distance sur chemin récemment découverte",
            "CO2 économisé",
            "Longueur de piscine",
            "Charge d’entraînement",
            "Intensité",
            "Vitesse moyenne ajustée selon la pente",
            "Temps enregistré par le chronomètre",
            "Heure de début",
            "Heure d'observation de la météo",
            "Heure de lever du soleil",
            "Heure de coucher du soleil",
            "Distance en descente"
        ]

        bools = [
            "Utiliser l'Effort ressenti",
            "Déplacement-transport",
            "À partir du téléchargement",
            "Signalé",
            "Récupération",
            "Avec mon animal de compagnie",
            "Compétition",
            "Sortie longue",
            "Pour la bonne cause",
            "Avec enfant"
        ]

        strs = [
            "Nom de l'activité",
            "Type d'activité",
            "Description de l'activité",
            "Note privée sur les activités",
            "Matériel utilisé pour l'activité",
            "Nom du fichier",
            "Type",
            "Conditions météo",
            "Point de rosée",
            "Rafale de vent",
            "Direction du vent",
            "Intensité des précipitations",
            "Phase de la lune",
            "Matériel",
            "Type de précipitations",
            "Couverture nuageuse",
            "Visibilité selon les prévisions météo",
            "Support"
        ]

        print("ints:"+str(len(ints)))
        print("dates:"+str(len(dates)))
        print("floats:"+str(len(floats)))
        print("bools:"+str(len(bools)))
        print("strs:"+str(len(strs)))
        print("total:"+str(len(ints)+len(dates)+len(floats)+len(bools)+len(strs)))

        with connection.cursor() as insertion_cursor:
            for row in activities:
                if (
                    row["ID de l'activité"] is not None
                ):
                    activity=convert_row(row, ints, dates, floats, bools, strs)
                    insertion_cursor.execute(insert_query, (
                        activity["ID de l'activité"],
                        activity["Date de l'activité"],
                        activity["Nom de l'activité"],
                        activity["Type d'activité"],
                        activity["Description de l'activité"],
                        activity["Note privée sur les activités"],
                        activity["Matériel utilisé pour l'activité"],
                        activity["Nom du fichier"],
                        activity["Poids de l'athlète"],
                        activity["Poids du vélo"],
                        activity["Temps écoulé"],
                        activity["Durée de déplacement"],
                        activity["Distance"],
                        activity["Vitesse max."],
                        activity["Vitesse moyenne"],
                        activity["Dénivelé positif"],
                        activity["Dénivelé négatif"],
                        activity["Altitude min."],
                        activity["Altitude max."],
                        activity["Pente max."],
                        activity["Pente moyenne"],
                        activity["Pente positive moyenne"],
                        activity["Pente négative moyenne"],
                        activity["Cadence max."],
                        activity["Cadence moyenne"],
                        activity["Fréquence cardiaque max."],
                        activity["Fréquence cardiaque moyenne"],
                        activity["Puissance max."],
                        activity["Puissance moyenne"],
                        activity["Calories"],
                        activity["Température max."],
                        activity["Température moyenne"],
                        activity["Effort relatif"],
                        activity["Effort total"],
                        activity["Nombre de sorties course à pied"],
                        activity["Temps de montée"],
                        activity["Temps de descente"],
                        activity["Autres temps"],
                        activity["Effort ressenti"],
                        activity["Type"],
                        activity["Heure de début"],
                        activity["Puissance moyenne pondérée"],
                        activity["Nombre d'échantillons de puissance"],
                        activity["Utiliser l'Effort ressenti"],
                        activity["Effort relatif ressenti"],
                        activity["Déplacement-transport"],
                        activity["Poids total soulevé"],
                        activity["À partir du téléchargement"],
                        activity["Distance ajustée selon la pente"],
                        activity["Heure d'observation de la météo"],
                        activity["Conditions météo"],
                        activity["Température selon les prévisions météo"],
                        activity["Température ressentie"],
                        activity["Point de rosée"],
                        activity["Humidité"],
                        activity["Pression atmosphérique"],
                        activity["Vitesse du vent"],
                        activity["Rafale de vent"],
                        activity["Direction du vent"],
                        activity["Intensité des précipitations"],
                        activity["Heure de lever du soleil"],
                        activity["Heure de coucher du soleil"],
                        activity["Phase de la lune"],
                        activity["Vélo"],
                        activity["Matériel"],
                        activity["Probabilité de précipitations"],
                        activity["Type de précipitations"],
                        activity["Couverture nuageuse"],
                        activity["Visibilité selon les prévisions météo"],
                        activity["Indice UV"],
                        activity["Ozone selon les prévisions météo"],
                        activity["Nombre de sauts"],
                        activity["Grit total"],
                        activity["Flow moyen"],
                        activity["Signalé"],
                        activity["Vitesse moyenne (temps écoulé)"],
                        activity["Distance sur chemin"],
                        activity["Distance récemment découverte"],
                        activity["Distance sur chemin récemment découverte"],
                        activity["Nombre d'activités"],
                        activity["Nombre total de pas"],
                        activity["CO2 économisé"],
                        activity["Longueur de piscine"],
                        activity["Charge d’entraînement"],
                        activity["Intensité"],
                        activity["Vitesse moyenne ajustée selon la pente"],
                        activity["Temps enregistré par le chronomètre"],
                        activity["Nombre total de cycles"],
                        activity.get("Récupération"),
                        activity.get("Avec mon animal de compagnie"),
                        activity.get("Compétition"),
                        activity.get("Sortie longue"),
                        activity.get("Pour la bonne cause"),
                        activity.get("Avec enfant"),
                        activity.get("Distance en descente"),
                        activity.get("Nombre total de séries"),
                        activity.get("Nombre total de répétitions"),
                        activity["Support"]
                    ))
            connection.commit()

def main():
    """Main function docstring."""
    # activities_db PostgreSQL
    activitiesdb_connection = db_connection()

    print("Table initialization", file=sys.stderr)
    init_activities_table(activitiesdb_connection)
    print("Strava data insertion", file=sys.stderr)
    insert_strava_data(activitiesdb_connection)

    activitiesdb_connection.close()

if __name__ == "__main__":
    main()
