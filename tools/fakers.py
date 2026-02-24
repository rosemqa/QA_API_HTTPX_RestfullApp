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


fake = Fake(faker=Faker())
