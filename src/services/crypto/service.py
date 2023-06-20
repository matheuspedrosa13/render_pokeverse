import base64
import datetime
import json

import jwt
import requests

from src.repositories.base_mongo.repository import RepositoryBaseMongo
from src.domain.poke_routes.enum import PokemonRoute


class ServiceCrypto:

    def __init__(self):
        self.repository_base_mongo = RepositoryBaseMongo()

    def encrypting(self, password):
        try:
            password_utf_8 = ServiceCrypto().utf_8(password)
        except:
            password_utf_8 = password
        public_key = str(self.repository_base_mongo.get_public_key())
        private_key = str(self.repository_base_mongo.get_private_key())

        password_crypto = ""

        for letter in password_utf_8:
            value = ord(letter)
            value_cripto = value ^ ord(private_key[0])
            value_cripto = value_cripto ^ ord(public_key[0])
            password_crypto += chr(value_cripto)

        return password_crypto

    def descrypting(self, password_crypto):
        public_key = str(self.repository_base_mongo.get_public_key())
        private_key = str(self.repository_base_mongo.get_private_key())
        password_descrypto = ""
        for letter in password_crypto:
            value = ord(letter)
            value_cripto = value ^ ord(public_key[0])
            value_cripto = value_cripto ^ ord(private_key[0])
            password_descrypto += chr(value_cripto)
        return password_descrypto

    def create_jwt(self, password_cripto, password, email):
        password_cripto_base64 = base64.b64encode(password_cripto.encode()).decode()
        if password_cripto_base64 == password:
            today = datetime.date.today()
            #colocar + 1 no day, no month e no year
            try:
                date = (datetime.date(year=today.year,
                                      month=today.month,
                                      day=today.day).isoformat())
            except:
                try:
                    date = (datetime.date(year=today.year,
                                          month=today.month,
                                          day=1).isoformat())
                except:
                    date = (datetime.date(year=today.year,
                                          month=1,
                                          day=1).isoformat())

            email_encriptado = self.encrypting(email)
            stuff = {
                "signature": self.encrypting(
                    self.repository_base_mongo.get_signature()),
                "expiration_date": self.encrypting(date),
                "email": email_encriptado,
                "roles": [
                    f"view_{email}",
                    f"edit_{email}"
                ]
            }
            return jwt.encode(stuff, key=self.repository_base_mongo.get_jwt_key(), algorithm="HS256")
        else:
            return "senha incorreta"

    def confirm_jwt(self, token_jwt, rota):
        print("apareceu")
        print(rota)
        jwta = self.descrypting_jwt(token_jwt)
        true_signature = self.descrypting(self.repository_base_mongo.get_signature())
        expiration = self.isExpiration(jwta['expiration_date'])
        jwta_password = self.descrypting(jwta['email'])

        for key, value in PokemonRoute.__members__.items():
            print(key)
            if key.split('.')[-1].lower() == rota:
                if expiration.days > 0:
                    if jwta['signature'] == true_signature:
                        permissao_necessaria = value.value[0] + "_" + jwta_password
                        roles_do_usuario = jwta.get("roles")
                        if permissao_necessaria in roles_do_usuario:
                            print("a")
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        return False

    def descrypting_jwt(self, token_jwt):
        return jwt.decode(token_jwt, self.repository_base_mongo.get_jwt_key(), algorithms="HS256")

    def isExpiration(self, date_jwt):
        today = datetime.date.today()
        true_date = self.descrypting(date_jwt).split('-')
        result = datetime.datetime(int(true_date[0]), int(true_date[1]), int(true_date[2])) - datetime.datetime(
            today.year, today.month, today.day)
        return result

    def utf_8(self, password):
        return (base64.b64decode(password.encode('ascii'))).decode('ascii')
