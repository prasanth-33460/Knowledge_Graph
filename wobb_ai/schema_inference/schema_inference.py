import spacy

class SchemaInference:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def extract_entities_and_relationships(self, text):
        doc = self.nlp(text)
        entities=[]
        for x in doc.ents:
            entities.append({"text": x.text, "label":x.label_})
            
        relationships=[]
        for y in doc.noun_chunks:
            for z in doc.noun_chunks:
                if y!=z:
                    relationships.append({"entity1":y.text, "entity2":z.text, "relationship":"related_to"})
        return entities, relationships        