from enum import Enum


class PokemonRoute(Enum):
    SEARCH_POKEMON = ["view"]
    SEARCH_USER_ID = ["view"]
    PAGINATION_OF_POKEMONS = ["view"]
    CAPTURE_POKEMONS = ["edit"]
    SEARCH_ALL_CAPTURED_POKEMONS = ["view"]
    SELECT_RANDOM_POKEMON = ["view"]
    UPDATE_USER = ["edit"]
    VIEW_USER = ["view"]
    DISABLE_USER = ["edit"]
    USER_PAGINATION = ["adm"]
    SIGN_IN = ["view"]
    LOGIN = ["view"]
    SHOW_ALL_ITEMS_BACKPACK = ["view"]
    ALTER_TRAINER = ["edit"]
    DELETE_TRAINER = ["edit"]
    FIND_ALL_TRAINER = ["adm"]
    FIND_TRAINER_WITH_QUERY = ["view"]
    FIND_TRAINER_FIELD = ["adm"]
    LIST_STORE_ITEMS = ["view"]
    BUY_ITEM_FROM_STORE = ["edit"]
    REGISTRAR_POKE = ["view"]
    CHANGE_PLACE = ["edit"]
    CHANGE_NICKNAME = ["edit"]


