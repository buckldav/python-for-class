import sqlite3
from .utils import list_to_string, list_to_string_sql
from .migrations import database

def insert_into_pokedex(pokemon_model):
	# https://www.sqlitetutorial.net/sqlite-insert/
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(f"""\
INSERT INTO pokedex ({list_to_string(pokemon_model.__dict__.keys()).lower()})
VALUES({list_to_string_sql(pokemon_model.__dict__.values())}); \
	""")
    conn.commit()
    conn.close()

class PokemonModel():
    """
    Do all of this together
    Variables and Functions = Fields and Methods
    __init__ to instantiate
    """
    def __init__(self, id, name, types, flavor_text):
        self.id = id
        self.name = name.title()
        self.types = list_to_string(types)
        self.flavor_text = flavor_text.replace('\n', ' ').replace('\f', '\n')
    
    def __str__(self):
        return f"""
{self.id}: {self.name}
Type(s): {self.types}
{self.flavor_text}        
        """

    def save(self):
        insert_into_pokedex(self)

class PokemonSerializer():
    """
    Takes Pokemon JSON and converts it to a PokemonModel object (stored in self.instance)
    """
    def __init__(self, json):
        types = [ typ["type"]["name"] for typ in json["types"]]
        flavor_text = ""
        for ft in json["flavor_text_entries"]:
            if ft["language"]["name"] == "en":
                flavor_text = ft["flavor_text"]
                break
        self.instance = PokemonModel(json["id"], json["name"], types, flavor_text)

    def save(self):
        self.instance.save()

"""
# PokemonModel example
print(PokemonModel(
    41, 
    "zubat", 
    ["flying", "poison"],
    "He lives in a cave"
))
"""