from src.infraestructures.mongodb.infraestructure import MongoDBInfra


class RepositoryBaseMongo:
    def __init__(self):
        self.cluster = MongoDBInfra().get_client()
        self.data_base = self.cluster.get_database("site_pokemons")
        self.collection_adm = self.data_base.get_collection("adm")
        self.result_cursor = self.collection_adm.find({})
        for x in self.result_cursor:
            self.x = x

    def get_public_key(self):
        return self.x['public_key']

    def get_private_key(self):
        return self.x['private_key']

    def get_signature(self):
        return self.x['signature']

    def get_jwt_key(self):
        return self.x['jwt']

    def get_jwt_key_adm(self):
        return self.x['jwtAdm']
