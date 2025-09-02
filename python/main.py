from python.crunchbase.load_organizations import load_organizations
from python.crunchbase.load_people import load_people
from python.semantic_scholar.load_papers import load_semantic_scholar
from python.wikidata.load_cities import load_cities
from python.wikidata.load_countries import load_countries


"""
TRES LONG
"""

if __name__ == '__main__':
    """Attention c'est long"""
    load_countries()
    load_cities()
    load_semantic_scholar()
    load_organizations("../odm/organizations.csv")
    load_people("../../odm/people.csv")
