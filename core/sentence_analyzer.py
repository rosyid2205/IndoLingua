import os, pickle
from core.pos_extractor import extract_pos
from core.structure_mapper import map_pos_to_structure

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PATTERN_PATH = os.path.join(BASE_DIR, "data", "pattern_bank.pkl")

with open(PATTERN_PATH, "rb") as f:
    PATTERN_BANK = pickle.load(f)

def mark_tokens(pos_seq, nominalized_word):
    marked = []
    for word, pos in pos_seq:
        if nominalized_word and word == nominalized_word:
            marked.append((word, "error"))
        else:
            marked.append((word, "ok"))
    return marked


def analyze(sentence: str):
    pos_seq = extract_pos(sentence)
    structure = map_pos_to_structure(pos_seq)

    pattern_match = tuple(structure) in PATTERN_BANK
    has_pred = "PRED" in structure
    nominalized = detect_nominalized_verb(pos_seq)

    # === SCORING ===
    if pattern_match:
        score = 100
        status = "Struktur kalimat baku"

    elif has_pred and nominalized:
        score = 80
        status = "Struktur hampir baku (terdapat ambiguitas kata)"

    elif has_pred:
        score = 60
        status = "Struktur kalimat tidak baku"

    else:
        score = 40
        status = "Kalimat tidak memiliki predikat yang jelas"

    feedback = generate_feedback(structure, pattern_match)

    if nominalized:
        feedback += f" Kata '{nominalized}' terdeteksi sebagai kata benda, padahal biasanya berfungsi sebagai kata kerja."

    token_marks = mark_tokens(pos_seq, nominalized)

    return {
        "sentence": sentence,
        "tokens": [w for w, _ in pos_seq],
        "pos": [p for _, p in pos_seq],
        "structure": structure,
        "score": score,
        "status": status,
        "feedback": feedback,
        "token_marks": token_marks
    }
def generate_feedback(structure, is_baku):
    if is_baku:
        return "Struktur kalimat sudah sesuai dengan pola baku bahasa Indonesia."

    if "PRED" not in structure:
        return "Kalimat tidak memiliki predikat (kata kerja) yang jelas."

    if structure and structure[0] != "SUBJ":
        return "Kalimat seharusnya diawali dengan subjek sebelum predikat."

    return "Urutan unsur kalimat tidak sesuai dengan pola baku bahasa Indonesia."

def detect_nominalized_verb(pos_seq):
    if len(pos_seq) >= 2:
        first_word, first_pos = pos_seq[0]
        second_pos = pos_seq[1][1]

        if first_pos == "NOUN" and second_pos != "VERB":
            return first_word
    return None
