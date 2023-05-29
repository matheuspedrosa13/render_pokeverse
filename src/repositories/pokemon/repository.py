import random
from uuid import uuid4

import requests
from src.infraestructures.mongodb.infraestructure import MongoDBInfra
from src.infraestructures.pokeapi.infraestructure import PokeapiInfra
from src.domain.models.pokeballs.model import PokeballModel
from src.domain.enums.pokeball_name.enum import PokeballName
from src.domain.models.fruits.model import FruitModel
from src.domain.enums.fruit_name.enum import FruitName


class PokeRepo:
    def __init__(self):
        self.infra = MongoDBInfra.get_client()
        self.dbPokemons = self.infra['Trainers']
        self.find = self.dbPokemons['wild pokemons']
        self.catch = self.dbPokemons['caught pokemons']
        self.cliente = self.dbPokemons['registered trainers']
        self.caught = self.dbPokemons['caught pokemons']

    def search_poke(self, id: int):
        if self.find.find_one({'id': id}):
            info = self.find.find_one({'id': id}, {'_id': 0})
            print("banco")
        else:
            request = PokeapiInfra.get(id).json()
            name = request['name']
            types = [x['type']['name'] for x in request['types']]
            speed = request['stats'][5]['base_stat']
            xp = request['base_experience']
            imagem = request['sprites']['front_default']
            info = {
                'name': name,
                'id': id,
                'type': types,
                'speed': speed,
                'xp': xp,
                'imagem': imagem
            }
            self.catch.insert_one(info.copy())
            print("api")
        return info

    def pag_poke(self, start_id, limit_page):
        return [PokeapiInfra.get(f"?offset={start_id}&limit={limit_page}").json()]

    def capture_poke(self, name_poke, nickname, owner_email, name_pokeball, experience, name_fruit, item_pokeball,
                     item_fruit):
        strengh_pokeball = ''
        strengh_fruit = ''

        for pokeballs in PokeballName:
            if pokeballs.value == name_pokeball:
                strengh_pokeball = pokeballs
        for fruits in FruitName:
            if fruits.value == name_fruit:
                strengh_fruit = fruits

        chance_capture = self.calculate_chance_capture(strengh_pokeball, experience, strengh_fruit)


        have_items = self.remove_item(owner_email, item_pokeball, item_fruit)
        if have_items != 1:
            return [{'status': 'sem items'}]

        if random.uniform(0, 100) <= chance_capture:
            unique_id = str(uuid4())
            pokemon = PokeapiInfra().get(f"/{name_poke}").json()

            owner_email = owner_email.split(".")[0]
            if self.catch.find_one({"owner_email": owner_email}):
                new_owner = {
                    "name": pokemon['name'],
                    "nickname": nickname,
                    "id": pokemon["id"],
                    "type": "",
                    "speed": "",
                    "experience": pokemon["base_experience"],
                    "image_front": pokemon["sprites"]["front_default"],
                    "image_back": pokemon["sprites"]["front_default"],
                    "unique_id": unique_id
                }

                self.catch.update_one(
                    {"owner_email": owner_email},
                    {"$push": {owner_email: new_owner}}
                )
            else:
                new_pokemon = {
                    "owner_email": owner_email,
                    owner_email: [
                        {
                            "name": pokemon['name'],
                            "nickname": nickname,
                            "id": pokemon["id"],
                            "type": "",
                            "speed": "",
                            "experience": pokemon["base_experience"],
                            "image_front": pokemon["sprites"]["front_default"],
                            "image_back": pokemon["sprites"]["front_default"],
                            "unique_id": unique_id
                        }
                    ]
                }

                self.catch.insert_one(new_pokemon)
            return [{'status': True}]
        else:
            return [{'status': False}]

    def search_poke_caught(self, owner_email):
        owner_email = owner_email.split(".")[0]
        if self.caught.find_one({"owner_email": owner_email}):
            dictionarys = (self.caught.find_one({"owner_email": owner_email}, {'owner_email': 0, '_id': 0}))[owner_email]
            all_dictionarys = {}
            for i, dictionary in enumerate(dictionarys):
                print("a")
                all_dictionarys[i] = dictionary
            return [all_dictionarys]
        else:
            return False

    def random_pokemon(self):
        pokemon = PokeapiInfra.get(f"/{random.randint(1, 1010)}").json()
        return [pokemon]

    def calculate_chance_capture(self, pokeball, experience_pokemon, fruit):
        strength_pokeball = self.calculate_strength_pokeball(pokeball)
        strength_fruit = self.calculate_strength_fruit(fruit)
        capture_difficulty = self.calculate_difficulty(experience_pokemon)

        chance = self.calculate_chance(
            experience_pokemon, strength_pokeball, capture_difficulty)
        chance_in_percentage_format = (
                ((capture_difficulty / (strength_pokeball - strength_fruit)) * (10 ** 5)) * chance)
        return chance_in_percentage_format

    def calculate_strength_pokeball(self, pokeball):
        pokeball_value = PokeballModel().pokeball_map.get(pokeball)
        return pokeball_value

    def calculate_strength_fruit(self, fruit):
        fruit_value = FruitModel().fruit_map.get(fruit)
        return fruit_value

    def calculate_difficulty(self, experience_pokemon):
        if experience_pokemon < 35 or experience_pokemon > 325:
            difficulty_value = 0
        else:
            difficulty_value = (experience_pokemon * 255) / 12
            difficulty_value = (1 if (experience_pokemon / 4) ==
                                     0 else experience_pokemon / 4) / difficulty_value
        return difficulty_value

    def calculate_chance(self, experience_pokemon, strength_pokeball, strength_fruit):
        chance_value = ((strength_pokeball * strength_fruit) /
                        experience_pokemon) * 100
        return chance_value

    def remove_item(self, user_name, pokeball, fruit):
        query_find_user = {"email": user_name}
        user__cur = self.cliente.find(query_find_user, {"_id": 0})

        user = [users for users in user__cur][0]

        items_of_user = list(user["items"])

        for items in items_of_user:
            if pokeball[0]['name'] in items:
                if items[1] == 0:
                    return [{'name': 'Sem pokebolas'}]
                else:
                    items[1] = items[1] - 1

        if not fruit == []:
            for items in items_of_user:
                if fruit[0]['name'] in items:
                    if items[1] == 0:
                        return [{'name': 'Sem frutas'}]
                    else:
                        items[1] = items[1] - 1

        self.cliente.update_one(query_find_user,
                                {"$set":
                                    {
                                        "items": items_of_user
                                    }
                                }
                                )
        return 1

