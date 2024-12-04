class Config:
    NEO4J_URI = "neo4j://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "neo4j_password"
    SUPPORTED_FORMATS = ["pdf", "docx", "jpg", "png", "json", "csv"]
    LOG_FILE = "logs/wobb_ai.log"
    LOGGING_LEVEL = "DEBUG"
    NER_MODEL = "en_core_web_sm"