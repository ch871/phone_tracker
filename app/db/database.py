from neo4j import GraphDatabase
from app.settings.config import URL, USER, PASSWORD

driver = GraphDatabase.driver(
    URL,
    auth=(USER, PASSWORD)
)
