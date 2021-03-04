import requests
import random
import sys
from app.migrations import create_table_migration
from app.orm import PokemonSerializer

def get_habitat():
    """
    Gets all available Pokemon habitats from PokeAPI
    Prompts the user to pick a habitat
    While user input is invalid, reprompt
    Return user's habitat choice
    """
    habitat_json = requests.get("https://pokeapi.co/api/v2/pokemon-habitat/").json()
    # type(habitat_json) == dict, type(habitat_json["results"]) == list
    habitat_names = [obj["name"] for obj in habitat_json["results"]]
    habitat_choice = None
    while habitat_choice not in habitat_names:
        if habitat_choice != None:
            print("Invalid input")
        print("Where would you like to catch a Pokemon?")
        print(habitat_names)
        habitat_choice = input("> ")
    return habitat_choice

def get_pokemon_from_habitat(habitat):
    """
    Get the API URLs of all Pokemon in the habitat
    Use random.choice() to pick a URL and get the json for that Pokemon
    Print "You caught a <insert mon here>!" with an fstring
    Return the JSON of that pokemon
    """
    available_pokemon_json = requests.get(f"https://pokeapi.co/api/v2/pokemon-habitat/{habitat}").json()
    available_pokemon_urls = [obj["url"] for obj in available_pokemon_json["pokemon_species"]]
    # Pick a random mon
    pokemon_json = requests.get(random.choice(available_pokemon_urls)).json()
    # Use pdb and pokemon_json.keys() to see the keys
    print(f"You caught a {pokemon_json['name'].title()}!")
    # Get more mon info
    pokemon_json.update(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_json['id']}").json())
    return pokemon_json

if __name__ == "__main__":
    if len(sys.argv) == 1:
        habitat = get_habitat()
        pokemon = get_pokemon_from_habitat(habitat)
        
        serializer = PokemonSerializer(pokemon)
        try:
            serializer.save()
            print(f"{serializer.instance.name} has been added to the PokeDex")
            print(serializer.instance)
        except:
            print(f"You already have a {serializer.instance.name}, no new PokeDex entry needed")
        
    elif len(sys.argv) == 2 and sys.argv[1] == "migrate":
        create_table_migration()
    
    else:
        print(f"Usage: \n python main.py\n python main.py migrate")