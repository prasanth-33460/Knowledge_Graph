import spacy
from typing import List, Tuple, Dict

class EntityRelationshipExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract(self, text: str) -> Dict[str, List]:
        doc = self.nlp(text)

        entities = []
        relationships = []
        
        for ent in doc.ents:
            entities.append({"entity": ent.text, "type": ent.label_})
        for token in doc:
            if token.dep_ in {"nsubj", "dobj"} and token.head.pos_ == "VERB":
                subject = token.text
                predicate = token.head.text
                object_ = [child.text for child in token.head.children if child.dep_ == "dobj"]
                if object_:
                    relationships.append({
                        "source": subject,
                        "relation": predicate,
                        "target": object_[0]
                    })
        return {"entities": entities, "relationships": relationships}

    def refine_extraction(self, entities: List[Dict], relationships: List[Dict]) -> Dict[str, List]:
        unique_entities = {e["entity"]: e for e in entities}.values()
        unique_relationships = {tuple(r.items()): r for r in relationships}.values()
        return {
            "entities": list(unique_entities),
            "relationships": list(unique_relationships)
        }