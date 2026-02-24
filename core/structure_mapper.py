def map_pos_to_structure(pos_sequence):
    structure = []
    n = len(pos_sequence)

    for i, (_, upos) in enumerate(pos_sequence):

        # SUBJ hanya jika:
        # - posisi awal
        # - NOUN/PROPN/PRON
        # - token setelahnya VERB
        if (
            i == 0
            and upos in {"NOUN", "PROPN", "PRON"}
            and n > 1
            and pos_sequence[1][1] == "VERB"
        ):
            structure.append("SUBJ")

        elif upos == "VERB":
            structure.append("PRED")

        elif upos in {"NOUN", "PROPN"}:
            structure.append("OBJ")

        elif upos in {"ADJ", "ADV"}:
            structure.append("COMP")

    return structure

