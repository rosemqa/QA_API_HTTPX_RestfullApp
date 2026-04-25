import random

from faker import Faker


class Fake:
    def __init__(self, faker: Faker):
        self.faker = faker

    def username(self) -> str:
        return self.faker.user_name()

    def password(self) -> str:
        return self.faker.password()

    def phone(self) -> str:
        return self.faker.msisdn()

    def email(self) -> str:
        return self.faker.email()

    def city(self) -> str:
        return self.faker.city()

    def street(self) -> str:
        return self.faker.street_name()

    def home_number(self) -> str:
        return self.faker.building_number()

    def price(self) -> str:
        return str(random.randint(10, 500))

    def item_description(self) -> str:
        return self.faker.text(70)

    def image_url(self) -> str:
        return self.faker.image_url()

    def user_balance(self) -> int:
        return self.faker.random_number(digits=3)


fake = Fake(faker=Faker())
