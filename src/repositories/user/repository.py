from src.domain.models.items.model import ItemModel
from src.infraestructures.mongodb.infraestructure import MongoDBInfra
<<<<<<< HEAD
from src.domain.models.user.model import UserModel


class UserRepo:

    def __init__(self):
        self.client = MongoDBInfra.get_client()
        self.database = self.client.get_database("Trainers")
        self.collection = self.database.get_collection("registered trainers")
        self.base_projection = {"_id": 0}

    def find(self, query: dict, projection: dict | None = None):
        if projection is None:
            projection = self.base_projection
        query = self.collection.find(query, projection)
        return [i for i in query]

    def list_all_trainer(self):
        query = {}
        trainers = self.find(query)
        return trainers

    def insert(self, info: dict):
        if self.collection.find_one({"email": info['email']}):
            return [{"Erro": "Email em uso"}]
        else:
            if UserModel(**info):
                self.collection.insert_one(info.copy())
                return [info]
            else:
                return [{}]

    def update(self, changed: dict, email: str):
        self.collection.update_one({"email": email}, {"$set": changed})
        return [self.collection.find_one({"email": email}, {"_id": 0})]

    def delete(self, email: str):
        try:
            if self.collection.find_one({"email": email}):
                self.collection.delete_one({"email": email})
                return [{"Status": "Deletado com sucesso"}]
            else:
                return [{"Status": "Email não existe"}]
        except:
            return [{"Status": "Num funfou"}]


    def login(self, email: str, password: str):
        user = self.collection.find_one({"$and": [{"email": email}, {"password": password}]}, {"_id": 0})
        if user:
            return [{"Usuario logado": user}]
        else:
            return [{"Erro": "Credenciais invalidas"}]


=======


class UsersRepository:

    def __init__(self):
        self.client = MongoDBInfra.get_client()
        self.database = self.client.get_database("user_microservice")
        self.collection = self.database.get_collection("users")
        self.base_projection = {"_id": 0}

        # self.collection_users = self.data_base.get_collection("user")

    def buy_item_from_store(self, user_name, item):
        query_find_user = {"name": user_name}
        user__cur = self.collection.find(query_find_user, {"_id": 0})
        user = [users for users in user__cur][0]

        items_of_user = list(user["items"])

        if (user["money"] - item["price"]) > 0:
            if not items_of_user:
                items_of_user.append([item['name'], 1])
            else:
                not_in_items = True
                for items in items_of_user:
                    if item['name'] in items:
                        items[1] = items[1] + 1
                        not_in_items = False
                if not_in_items:
                    items_of_user.append([item['name'], 1])

            self.collection.update_one(query_find_user,
                                       {"$set":
                                           {
                                               "money": (user["money"] - item["price"])
                                           }
                                       })

            self.collection.update_one(query_find_user,
                                       {"$set":
                                           {
                                               "items": items_of_user
                                           }
                                       }
                                       )

            user_updated = self.collection.find_one(query_find_user, {"_id": 0})
            return [user_updated]
        else:
            return [{"Status": "Sem saldo amigão"}]
>>>>>>> 27c10acf01476f4b78fbb69ed015dc78d3ca4ce4

