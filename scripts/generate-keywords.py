import json
import re

def slugify(text):
    text = text.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')

base_keywords = [
    "Software zur Flächenakquise Photovoltaik",
    "Solar Potentialflächen Finder Tool",
    "Automatisierte Flächenanalyse PV Freiflächen",
    "GIS Daten mit Ratsdaten verknüpfen Solar"
]

# Regionale Daten mit VÖLLIG UNIQUE Content für Problem-Section
regional_data = {
    "Bayern": {
        "kommunen_soft": "über 2.000 Kommunen",
        "h2_problem": "Über 2.000 Kommunen. Eine zentrale Plattform.",
        "problem_intro": "In Bayerns vielfältiger Verwaltungslandschaft ist der entscheidende Aufstellungsbeschluss oft tief in einem der zahlreichen Ratsinformationssysteme verborgen.",
        "besonderheit": "Bayern hat mit seinem Klimaschutzgesetz ambitionierte Ziele für erneuerbare Energien definiert.",
        "herausforderung": "Die bekannte 10H-Abstandsregelung für Windkraft macht PV-Freiflächen zu einer wichtigen Alternative für Projektentwickler.",
        "ratssystem": "Viele bayerische Kommunen nutzen etablierte Ratsinformationssysteme.",
        "landschaft": "Von den Alpen bis Franken bietet Bayern vielfältige Standortbedingungen.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in Bayern?",
        "faq3_a": "In Bayern sind die kommunalen Flächennutzungspläne und die Regelungen für Windkraft-Abstände relevant. Viele Kommunen setzen daher verstärkt auf PV-Freiflächen als Alternative.",
        "faq4_q": "In welchen Regionen Bayerns ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Erfahrungsgemäß zeigen ländliche Regionen in Niederbayern, der Oberpfalz und Franken eine hohe Aktivität bei der Ausweisung von PV-Flächen."
    },
    "Baden-Württemberg": {
        "kommunen_soft": "über 1.000 Kommunen",
        "h2_problem": "Mehr als 1.000 Gemeinden. Ein effizienter Workflow.",
        "problem_intro": "Ob im Schwarzwald oder im Rheintal: Relevante Planungsdaten sind auf unzählige kommunale Portale verteilt, was die manuelle Suche extrem zeitaufwendig macht.",
        "besonderheit": "Baden-Württemberg hat klare Flächenziele für PV-Freiflächen im Klimaschutzgesetz definiert.",
        "herausforderung": "Die kleinteilige Flurstruktur erfordert präzise Standortanalysen.",
        "ratssystem": "Viele Kommunen nutzen Bürgerinfo-Portale für ihre Ratsdokumente.",
        "landschaft": "Vom Bodensee bis zum Odenwald – vielfältige Standortbedingungen.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in Baden-Württemberg?",
        "faq3_a": "Baden-Württemberg fokussiert auf Agri-PV und benachteiligte Gebiete. Viele Kommunen erstellen eigene Energieleitpläne mit priorisierten Flächen.",
        "faq4_q": "In welchen Regionen Baden-Württembergs ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Besonders aktiv sind erfahrungsgemäß die ländlichen Kreise in Heilbronn-Franken und im Nordosten des Bundeslandes."
    },
    "Brandenburg": {
        "kommunen_soft": "mehrere hundert Kommunen",
        "h2_problem": "Hunderte Amtsblätter. Ein automatisierter Scan.",
        "problem_intro": "Gerade in Brandenburg mit seinen vielen Konversionsflächen ist Geschwindigkeit entscheidend – doch die Daten liegen verstreut in lokalen Systemen.",
        "besonderheit": "Brandenburg gehört zu den führenden PV-Bundesländern in Deutschland.",
        "herausforderung": "Die hohe Nachfrage nach Flächen erfordert schnelle Reaktionszeiten bei neuen Aufstellungsbeschlüssen.",
        "ratssystem": "Brandenburgische Kommunen nutzen überwiegend etablierte Ratsinformationssysteme.",
        "landschaft": "Dünn besiedelte Gebiete und ehemalige Konversionsflächen bieten Potential.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in Brandenburg?",
        "faq3_a": "Brandenburg bietet durch dünn besiedelte Gebiete und ehemalige Konversionsflächen (Tagebau, Militär) gute Bedingungen. Die Landesregierung unterstützt den PV-Ausbau aktiv.",
        "faq4_q": "In welchen Regionen Brandenburgs ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Erfahrungsgemäß zeigen die Landkreise Uckermark, Prignitz und die ländlichen Gebiete um Berlin hohe Aktivität."
    },
    "Niedersachsen": {
        "kommunen_soft": "nahezu 1.000 Kommunen",
        "h2_problem": "Fast 1.000 Kommunen im Blick behalten.",
        "problem_intro": "Die Kombination aus Wind- und Solarparks erfordert in Niedersachsen einen genauen Blick auf die Beschlusslage in den vielen ländlichen Gemeinden.",
        "besonderheit": "Niedersachsen kombiniert langjährige Erfahrung im Windkraftbereich mit wachsendem PV-Ausbau.",
        "herausforderung": "Die Koordination mit bestehenden Windparkprojekten ist ein wichtiger Faktor.",
        "ratssystem": "Niedersächsische Kommunen nutzen verschiedene Ratsinformationssysteme.",
        "landschaft": "Vom Emsland bis zum Weserbergland – große Agrarflächen.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in Niedersachsen?",
        "faq3_a": "Niedersachsen hat durch die Erfahrung im Windkraftbereich etablierte Genehmigungsstrukturen. Viele Kommunen kombinieren Wind- und PV-Planung.",
        "faq4_q": "In welchen Regionen Niedersachsens ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Erfahrungsgemäß zeigen das Emsland und die östlichen Landkreise hohe Aktivität bei PV-Planungen."
    },
    "NRW": {
        "kommunen_soft": "knapp 400 Kommunen",
        "h2_problem": "Dicht besiedelt. Komplex verwaltet.",
        "problem_intro": "In Nordrhein-Westfalen ist der Wettbewerb um Flächen besonders hoch. Wer hier zuerst von neuen Beschlüssen erfährt, sichert sich den entscheidenden Vorteil.",
        "besonderheit": "Als bevölkerungsreichstes Bundesland setzt NRW verstärkt auf innovative PV-Konzepte.",
        "herausforderung": "Hohe Flächenkonkurrenz erfordert präzise Analyse von Planungsbeschlüssen.",
        "ratssystem": "NRW-Kommunen nutzen überwiegend etablierte Bürgerinformationssysteme.",
        "landschaft": "Vom Münsterland bis zum Ruhrgebiet – vielfältige Rahmenbedingungen.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in NRW?",
        "faq3_a": "NRW fokussiert auf innovative Konzepte wie Floating-PV und Agri-PV. Die Landesregierung hat ambitionierte Ausbauziele definiert.",
        "faq4_q": "In welchen Regionen NRWs ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Erfahrungsgemäß zeigen das Münsterland mit Agrarflächen und das Ruhrgebiet mit Konversionspotential hohe Aktivität."
    },
    "Hessen": {
        "kommunen_soft": "über 400 Kommunen",
        "h2_problem": "Über 400 Kommunen effizient screenen.",
        "problem_intro": "Die hessischen Vorranggebiete sind heiß begehrt. Unser Tool filtert für Sie die relevanten Beschlüsse aus der Flut der kommunalen Informationen.",
        "besonderheit": "Hessen hat im Landesentwicklungsplan klare Vorranggebiete für erneuerbare Energien definiert.",
        "herausforderung": "Die heterogene Landschaft erfordert differenzierte Standortanalysen.",
        "ratssystem": "Hessische Kommunen nutzen verschiedene Ratsinformationssysteme.",
        "landschaft": "Von Rhein-Main bis Nordhessen – unterschiedliche Bedingungen.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in Hessen?",
        "faq3_a": "Hessen definiert im Landesentwicklungsplan Vorranggebiete. Im ländlichen Nordhessen und Vogelsberg bestehen gute Potentiale.",
        "faq4_q": "In welchen Regionen Hessens ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Erfahrungsgemäß zeigen die ländlichen Kreise in Waldeck-Frankenberg und im Vogelsberg hohe Aktivität."
    },
    "Sachsen-Anhalt": {
        "kommunen_soft": "über 200 Kommunen",
        "h2_problem": "Große Flächen. Schnelle Entscheidungen.",
        "problem_intro": "In Sachsen-Anhalt bieten ehemalige Industrieareale riesige Chancen, doch die entsprechenden Planungsprozesse laufen oft dezentral und unbemerkt ab.",
        "besonderheit": "Sachsen-Anhalt bietet durch geringe Bevölkerungsdichte gute PV-Bedingungen.",
        "herausforderung": "Ehemalige Bergbau- und Militärflächen erfordern detaillierte Prüfung.",
        "ratssystem": "Sachsen-Anhaltische Kommunen nutzen etablierte Ratsinformationssysteme.",
        "landschaft": "Von der Altmark bis zum Burgenlandkreis – viel Raum für Großprojekte.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in Sachsen-Anhalt?",
        "faq3_a": "Sachsen-Anhalt profitiert von ehemaligen Bergbau- und Militärflächen. Die Landesregierung fördert deren Reaktivierung für PV.",
        "faq4_q": "In welchen Regionen Sachsen-Anhalts ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Erfahrungsgemäß zeigt die Börde-Region hohe Aktivität bei der Ausweisung neuer Flächen."
    },
    "Mecklenburg-Vorpommern": {
        "kommunen_soft": "mehrere hundert Kommunen",
        "h2_problem": "Weites Land. Versteckte Daten.",
        "problem_intro": "MV bietet Platz für Großprojekte, aber die relevanten Beschlüsse verstecken sich oft in den Sitzungsprotokollen kleiner Ämter und Gemeinden.",
        "besonderheit": "Mecklenburg-Vorpommern bietet große zusammenhängende Freiflächen.",
        "herausforderung": "Die geringe Bevölkerungsdichte bedeutet weniger, aber größere Projekte pro Beschluss.",
        "ratssystem": "MV-Kommunen nutzen verschiedene Ratsinformationssysteme und Amtsportale.",
        "landschaft": "Große Freiflächen ermöglichen Projekte mit erheblicher Größe.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in Mecklenburg-Vorpommern?",
        "faq3_a": "Mecklenburg-Vorpommern ermöglicht großflächige PV-Projekte. Die geringe Siedlungsdichte und extensive Landwirtschaft bieten gute Voraussetzungen.",
        "faq4_q": "In welchen Regionen MVs ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Erfahrungsgemäß zeigen die Landkreise Vorpommern-Greifswald und die Mecklenburgische Seenplatte hohe Aktivität."
    },
    "Rheinland-Pfalz": {
        "kommunen_soft": "über 2.000 Kommunen",
        "h2_problem": "Über 2.000 Gemeinden im Fokus.",
        "problem_intro": "Die extrem kleinteilige Verwaltungsstruktur in Rheinland-Pfalz macht die manuelle Suche fast unmöglich. Wir bündeln diese Informationen für Sie.",
        "besonderheit": "Rheinland-Pfalz hat eine der kleingliedrigsten Verwaltungsstrukturen Deutschlands.",
        "herausforderung": "Die hohe Anzahl an Ortsgemeinden erfordert umfassendes Monitoring.",
        "ratssystem": "Rheinland-Pfalz nutzt Verbandsgemeinde-Strukturen mit eigenen Portalen.",
        "landschaft": "Von der Eifel bis zur Pfalz – vielfältige Standortbedingungen.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in Rheinland-Pfalz?",
        "faq3_a": "Rheinland-Pfalz hat durch die Verbandsgemeinde-Struktur besondere Planungsebenen. Viele Beschlüsse werden auf Verbandsgemeinde-Ebene gefasst.",
        "faq4_q": "In welchen Regionen von Rheinland-Pfalz ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Erfahrungsgemäß zeigen die Westpfalz und der Hunsrück hohe PV-Planungsaktivität."
    },
    "Schleswig-Holstein": {
        "kommunen_soft": "über 1.000 Kommunen",
        "h2_problem": "Wind und Sonne effizient vernetzt.",
        "problem_intro": "Zwischen den Meeren müssen PV-Projekte oft mit Windparks abgestimmt werden. Die entsprechenden gemeindlichen Beschlüsse finden Sie hier zuerst.",
        "besonderheit": "Schleswig-Holstein ergänzt seine starke Windkraft zunehmend durch PV-Freiflächen.",
        "herausforderung": "Die Koordination mit bestehenden Windparks und Netzkapazitäten ist wichtig.",
        "ratssystem": "Schleswig-Holsteinische Kommunen nutzen verschiedene Ratsinformationssysteme.",
        "landschaft": "Von der Nordseeküste bis zur Lauenburgischen Seenplatte.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in Schleswig-Holstein?",
        "faq3_a": "Schleswig-Holstein kombiniert als Windkraft-Vorreiter zunehmend Wind und Solar. Die Landesregierung fördert Hybrid-Parks.",
        "faq4_q": "In welchen Regionen Schleswig-Holsteins ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Erfahrungsgemäß zeigen die Kreise Dithmarschen und Nordfriesland hohe Aktivität."
    },
    "Thüringen": {
        "kommunen_soft": "über 600 Kommunen",
        "h2_problem": "Ländlicher Raum. Großes Potenzial.",
        "problem_intro": "In Thüringen entwickeln sich viele Projekte im ländlichen Raum, wo die Informationswege oft kurz, aber digital schwer auffindbar sind.",
        "besonderheit": "Thüringen hat den PV-Ausbau als strategisches Ziel definiert.",
        "herausforderung": "Die heterogene Landschaft erfordert differenzierte Analysen.",
        "ratssystem": "Thüringische Kommunen nutzen etablierte Ratsinformationssysteme.",
        "landschaft": "Vom Thüringer Wald bis zum Thüringer Becken.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in Thüringen?",
        "faq3_a": "Thüringen bietet mit dem Thüringer Becken gute Bedingungen. Die Landesregierung unterstützt beschleunigte Genehmigungsverfahren.",
        "faq4_q": "In welchen Regionen Thüringens ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Erfahrungsgemäß zeigen die Landkreise im Thüringer Becken hohe Planungsaktivität."
    },
    "Sachsen": {
        "kommunen_soft": "über 400 Kommunen",
        "h2_problem": "Strukturwandel als Chance.",
        "problem_intro": "Gerade in den ehemaligen Revieren Sachsens entstehen neue Energielandschaften. Die kommunalen Planungsprozesse dazu sind komplex und verteilen sich auf viele Träger.",
        "besonderheit": "Sachsen nutzt verstärkt ehemalige Braunkohle-Flächen für PV-Projekte.",
        "herausforderung": "Die Transformation von Tagebauflächen erfordert komplexe Abstimmungen.",
        "ratssystem": "Sächsische Kommunen nutzen etablierte Ratsinformationssysteme.",
        "landschaft": "Vom Erzgebirge bis zur Oberlausitz – Tagebau-Rekultivierung bietet Chancen.",
        "faq3_q": "Welche Besonderheiten gelten für PV-Projekte in Sachsen?",
        "faq3_a": "Sachsen bietet durch die Braunkohle-Rekultivierung besondere Großflächen-Potentiale. Die Landesregierung fördert die Umwandlung ehemaliger Bergbauflächen.",
        "faq4_q": "In welchen Regionen Sachsens ist die Planungsaktivität besonders hoch?",
        "faq4_a": "Erfahrungsgemäß zeigen die Landkreise Leipzig und Nordsachsen durch die Tagebau-Nähe hohe Aktivität."
    }
}

database = []

for kw in base_keywords:
    for region, data in regional_data.items():
        full_kw = f"{kw} {region}"
        
        # FAQ 1: Prozess und Technik (OHNE harte Zahlen)
        faq_a1 = (
            f"Unser Tool analysiert {full_kw} durch automatisierte Auswertung von Ratsdokumenten. "
            f"In {region} durchsuchen wir {data['kommunen_soft']} nach Aufstellungsbeschlüssen. "
            f"{data['ratssystem']} So können Projektentwickler potenzielle Standorte frühzeitig identifizieren."
        )

        # FAQ 2: Datenquellen und Regionalität
        faq_a2 = (
            f"Für {region} greift die Software auf Feldblockkataster, XPlanung-Daten und Gemeinderatsprotokolle zu. "
            f"{data['besonderheit']} "
            f"{data['landschaft']}"
        )
        
        entry = {
            "keyword": full_kw,
            "slug": slugify(full_kw),
            "page_title": f"{full_kw} | Professionelle Lösung für PV-Projektentwickler",
            "meta_description": f"Suchen Sie {full_kw}? Unsere Software durchsucht {data['kommunen_soft']} nach Aufstellungsbeschlüssen in {region}. Jetzt testen!",
            "h1": f"Optimale {kw} in {region}",
            "regional_context": f"{data['besonderheit']}",
            "region": region,
            "kommunen_soft": data["kommunen_soft"],
            "h2_problem": data["h2_problem"],
            "problem_intro": data["problem_intro"],
            "regional_challenge": data["herausforderung"],
            "faq_question_1": f"Wie funktioniert {full_kw}?",
            "faq_answer_1": faq_a1,
            "faq_question_2": f"Welche Datenquellen werden für {region} genutzt?",
            "faq_answer_2": faq_a2,
            "faq_question_3": data["faq3_q"],
            "faq_answer_3": data["faq3_a"],
            "faq_question_4": data["faq4_q"],
            "faq_answer_4": data["faq4_a"]
        }
        database.append(entry)

with open('src/data/keywords.json', 'w', encoding='utf-8') as f:
    json.dump(database, f, ensure_ascii=False, indent=4)

print(f"Erfolg! {len(database)} Datensätze UNIQUE Content erstellt.")
