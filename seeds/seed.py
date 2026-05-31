import random

from flask_seeder import Seeder, Faker, generator

from my_app.blog import models as blog_models
from my_app.auth import models as auth_models
from my_app.documents import models as doc_models
from my_app.tasks import models as task_models

class CategorySeeder(Seeder):
    def run(self):
        faker = Faker(
            cls=blog_models.Category,
            init={
                "name": generator.Name(),
            }
        )

        for category in faker.create(15):
            print("Adding category %s" % category)
            self.db.session.add(category)

class TagSeeder(Seeder):
    def run(self):
        faker = Faker(
            cls=blog_models.Tag,
            init={
                "name": generator.Name(),
            }
        )

        for tag in faker.create(15):
            print("Adding tag %s" % tag)
            self.db.session.add(tag)

class DocumentSeeder(Seeder):
    def run(self):
        names = ['avatar_1', 'avatar_2', 'avatar_3', 'doc_1', 'doc_2']
        exts = ['png', 'jpg', 'jpg', 'pdf', 'docx']
        for name, ext in zip(names, exts):
            doc = doc_models.Document(name=name, ext=ext)
            print("Adding document %s" % doc)
            self.db.session.add(doc)

class AddressSeeder(Seeder):
    def run(self):
        addresses = [
            '123 Main St, New York, NY',
            '456 Oak Ave, Los Angeles, CA',
            '789 Pine Rd, Chicago, IL',
            '321 Elm St, Houston, TX',
            '654 Maple Dr, Phoenix, AZ',
        ]
        for addr in addresses:
            a = auth_models.Address(address=addr)
            print("Adding address %s" % a)
            self.db.session.add(a)

class SocialNetworkSeeder(Seeder):
    def run(self):
        networks = ['Facebook', 'Twitter', 'Instagram', 'LinkedIn', 'GitHub']
        for name in networks:
            sn = auth_models.SocialNetwork(name=name)
            print("Adding social network %s" % sn)
            self.db.session.add(sn)

class RolesSeeder(Seeder):
    def run(self):
        roles = ['Admin', 'Editor', 'Author', 'Contributor', 'Subscriber']
        for name in roles:
            role = auth_models.Roles(name=name)
            print("Adding role %s" % role)
            self.db.session.add(role)

class UserSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 3

    def run(self):
        users_data = [
            {'username': 'admin2@admin.com', 'email': 'admin2@admin.com', 'password': 'admin', 'first_name': 'Admin', 'last_name': 'User', 'lang': auth_models.LangChoices.EN, 'role': 'Admin'},
            {'username': 'john@example.com', 'email': 'john@example.com', 'password': '123456', 'first_name': 'John', 'last_name': 'Doe', 'lang': auth_models.LangChoices.EN, 'role': 'Editor'},
            {'username': 'maria@example.com', 'email': 'maria@example.com', 'password': '123456', 'first_name': 'Maria', 'last_name': 'Garcia', 'lang': auth_models.LangChoices.ES, 'role': 'Author'},
            {'username': 'bob@example.com', 'email': 'bob@example.com', 'password': '123456', 'first_name': 'Bob', 'last_name': 'Smith', 'lang': auth_models.LangChoices.EN, 'role': 'Contributor'},
            {'username': 'ana@example.com', 'email': 'ana@example.com', 'password': '123456', 'first_name': 'Ana', 'last_name': 'Lopez', 'lang': auth_models.LangChoices.ES, 'role': 'Subscriber'},
        ]

        addresses = auth_models.Address.query.all()
        docs = doc_models.Document.query.all()

        for i, data in enumerate(users_data):
            user = auth_models.User(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.lang = data['lang']
            if addresses:
                user.address_id = addresses[i % len(addresses)].id
            if docs:
                user.avatar_id = docs[i % len(docs)].id

            self.db.session.add(user)
            self.db.session.flush()

            role = auth_models.Roles.query.filter_by(name=data['role']).first()
            if role:
                ur = auth_models.UserRoles(user_id=user.id, role_id=role.id)
                self.db.session.add(ur)

            print("Adding user %s" % data['username'])

class UserSocialNetworkSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 4

    def run(self):
        users = auth_models.User.query.all()
        networks = auth_models.SocialNetwork.query.all()
        for user in users:
            selected = random.sample(networks, random.randint(1, min(3, len(networks))))
            for sn in selected:
                usn = auth_models.UserSocialNetwork(
                    user_id=user.id,
                    social_network_id=sn.id,
                    url='https://example.com/%s' % sn.name.lower()
                )
                self.db.session.add(usn)
                print("Adding social network %s for user %s" % (sn.name, user.username))

class TaskSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 5

    def run(self):
        users = auth_models.User.query.all()
        categories = blog_models.Category.query.all()
        tags = blog_models.Tag.query.all()
        docs = doc_models.Document.query.all()

        task_names = [
            'Review homepage design',
            'Write blog post about Flask',
            'Fix login bug',
            'Update database schema',
            'Refactor API endpoints',
            'Write unit tests',
            'Deploy to production',
            'Optimize queries',
            'Add search feature',
            'Update dependencies',
        ]

        for name in task_names:
            task = task_models.Task(
                name=name,
                category_id=random.choice(categories).id if categories else 1,
                user_id=random.choice(users).id if users else 1,
            )
            if docs and random.random() > 0.5:
                task.document_id = random.choice(docs).id

            self.db.session.add(task)
            self.db.session.flush()

            for t in random.sample(tags, random.randint(1, min(3, len(tags)))):
                task.tags.append(t)

            self.db.session.add(task)
            print("Adding task %s" % name)

class PostSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 6

    def run(self):
        faker = Faker(
            cls=blog_models.Post,
            init={
                "name": generator.Name(),
                "description": generator.Name(),
                "content": "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Sint saepe accusamus nesciunt reiciendis in temporibus asperiores dolores veniam, velit ad repellat perferendis similique corporis, natus voluptate, officiis vel neque at.",
                "category_id": generator.Integer(start=1, end=15)
            }
        )

        tags = blog_models.Tag.query.all()

        for post in faker.create(20):
            print("Adding post %s" % post)
            self.db.session.add(post)
            self.db.session.commit()
            self.db.session.refresh(post)

            for i in range(0, random.randint(1, 4)):
                tag = random.choice(tags)
                post.tags.append(tag)

            self.db.session.add(post)
