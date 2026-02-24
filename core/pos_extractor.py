import stanza

nlp = stanza.Pipeline(
    "id",
    processors="tokenize,pos",
    tokenize_no_ssplit=True,
    verbose=False
)

def extract_pos(sentence: str):
    doc = nlp(sentence)
    words = doc.sentences[0].words
    return [(w.text, w.upos) for w in words]
