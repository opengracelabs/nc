import os

places_data = [
    ["Kyoto (Washoku)", "(iii), (v), (vi)", "N/A"],
    ["Kerala (Yoga)", "(iii), (iv), (vi)", "N/A"],
    ["Oaxaca (Traditional Mexican Cuisine)", "(ii), (v)", "N/A"],
    ["Raja Ampat", "(vii), (ix), (x)", "IV"],
    ["Yellowstone", "(vii), (viii), (ix), (x)", "II"],
    ["Great Barrier Reef", "(vii), (viii), (ix), (x)", "VI"],
    ["Serengeti", "(vii), (x)", "II"],
    ["Machu Picchu", "(i), (iii), (vii), (ix)", "V"],
    ["Yosemite", "(vii), (viii)", "II"],
    ["Pantanal", "(vii), (ix), (x)", "IV"],
    ["Namibrand", "(vii), (viii)", "Ib"],
    ["Andalusia (Flamenco)", "(iii), (vi)", "N/A"],
    ["Okavango Delta", "(vii), (ix), (x)", "II"],
    ["Komodo", "(vii), (x)", "II"],
    ["Cape West Coast", "(ix), (x)", "IV"],
    ["Ngorongoro Lengai", "(vii), (viii), (ix), (x)", "VI"],
    ["Aoraki Mackenzie", "(vii), (viii)", "II"],
    ["Marrakech (Falconry)", "(v), (vi)", "N/A"],
    ["Bali (Wayang)", "(iii), (vi)", "N/A"],
    ["Palau", "(vii), (ix), (x)", "VI"],
    ["Galápagos Islands", "(vii), (viii), (ix), (x)", "Ia"],
    ["Monarch Butterfly BR", "(vii)", "IV"],
    ["Sian Ka'an", "(vii), (x)", "II"],
    ["Clayoquot Sound", "(ix), (x)", "IV"],
    ["Reykjanes", "(vii), (viii)", "III"],
    ["Naples (Mediterranean Diet)", "(ii), (iv), (v)", "N/A"],
    ["Kingston (Reggae)", "(vi)", "N/A"],
    ["Bahia (Capoeira)", "(vi)", "N/A"],
    ["Buenos Aires (Tango)", "(vi)", "N/A"],
    ["Kilimanjaro", "(vii)", "II"],
    ["Everglades", "(viii), (ix), (x)", "II"],
    ["Mekong Delta", "(ix), (x)", "V"],
    ["Nilgiri", "(ix), (x)", "IV"],
    ["Arganeraie", "(ix), (x)", "VI"],
    ["Katla", "(vii), (viii)", "III"],
    ["Pic du Midi", "(vii)", "V"],
    ["Kakadu", "(i), (vi), (vii), (ix), (x)", "II"],
    ["Ha Long Bay", "(vii), (viii)", "II"],
    ["Iguazu", "(vii), (x)", "II"],
    ["Itoigawa", "(viii)", "III"],
    ["Batur", "(vii), (viii)", "V"],
    ["Central Idaho", "(vii)", "II"],
    ["Ross Sea", "(vii), (ix), (x)", "Ia"],
    ["Marae Moana", "(ix), (x)", "VI"],
    ["Kerry", "(vii)", "V"],
    ["Brecon Beacons", "(vii), (viii)", "V"],
    ["Camargue", "(ix), (x)", "IV"],
    ["Doñana", "(vii), (ix), (x)", "II"],
    ["Lake Baikal", "(vii), (viii), (ix), (x)", "II"],
    ["Mount Kenya", "(vii), (ix)", "II"],
    ["Dana", "(ix), (x)", "IV"],
    ["Lesvos", "(viii)", "III"],
    ["Mont-Mégantic", "(vii)", "V"],
    ["Tubbataha", "(vii), (ix), (x)", "II"],
    ["Sundarbans", "(ix), (x)", "II"],
    ["Wadden Sea", "(viii), (ix), (x)", "IV"],
    ["Danube Delta", "(vii), (ix), (x)", "II"],
    ["Mudeungsan", "(vii), (viii)", "V"],
    ["Cherry Springs", "(vii)", "V"],
    ["Exmoor", "(vii), (viii)", "V"],
    ["Qeshm", "(vii), (viii)", "VI"],
    ["Papahānaumokuākea", "(iii), (vi), (viii), (ix), (x)", "Ia"],
    ["Oki Islands", "(vii), (viii)", "V"],
    ["Marble Arch Caves", "(viii)", "III"],
    ["Zselic", "(vii)", "V"],
    ["Bañados del Este", "(ix), (x)", "IV"],
    ["Chagos", "(vii), (ix), (x)", "Ia"],
    ["Kermadec", "(vii), (ix), (x)", "Ia"],
    ["Phoenix Islands", "(vii), (ix), (x)", "Ia"],
    ["Ascension Island", "(vii), (ix), (x)", "VI"]
]

def derive_scores(unesco, iucn):
    cultural_criteria = ["(i)", "(ii)", "(iii)", "(iv)", "(v)", "(vi)"]
    natural_criteria = ["(vii)", "(viii)", "(ix)", "(x)"]
    
    is_cultural = any(c in unesco for c in cultural_criteria)
    is_natural = any(n in unesco for n in natural_criteria) or iucn != "N/A"
    
    dwc = "Low"
    if is_natural:
        dwc = "High"
    elif is_cultural:
        dwc = "Medium"
        
    cidoc = "Low"
    if is_cultural:
        cidoc = "High"
    elif is_natural:
        cidoc = "Medium"
        
    return dwc, cidoc

output_path = "/home/nathan/OpenGrace/nc/docs/curation/portfolio_standards_matrix.md"

def generate_markdown():
    with open(output_path, "w") as f:
        f.write("# Portfolio Standards Matrix\n\n")
        f.write("| Name | UNESCO | IUCN | DwC Applicability | CIDOC CRM Applicability | IIIF Applicability | Schema.org Applicability |\n")
        f.write("|------|--------|------|-------------------|--------------------------|--------------------|---------------------------|\n")
        
        for place in places_data:
            name, unesco, iucn = place
            dwc_score, cidoc_score = derive_scores(unesco, iucn)
            
            f.write(f"| {name} | {unesco} | {iucn} | {dwc_score} | {cidoc_score} | High | High |\n")

if __name__ == "__main__":
    generate_markdown()
    print(f"Successfully generated {output_path}")
