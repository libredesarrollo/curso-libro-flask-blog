import random

from flask_seeder import Seeder, Faker, generator

from my_app.blog import models

class CategorySeeder(Seeder):
    def run(self):

        faker = Faker(
            cls=models.Category,
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
            cls=models.Tag,
            init={
                "name": generator.Name(),
            }
        )

        for tag in faker.create(15):
            print("Adding tag %s" % tag)
            self.db.session.add(tag)



class PostSeeder(Seeder):
    def run(self):

        faker = Faker(
            cls=models.Post,
            init={
                "name": generator.Name(),
                "description": generator.Name() ,
                "content": "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Sint saepe accusamus nesciunt reiciendis in temporibus asperiores dolores veniam, velit ad repellat perferendis similique corporis, natus voluptate, officiis vel neque at.",
                "category_id": generator.Integer(start=1, end=15)
            }
        )

        for post in faker.create(20):
            print("Adding post %s" % post)
            self.db.session.add(post)
            self.db.session.commit()
            self.db.session.refresh(post)

            for i in range(0,random.randint(1,4)):
                tag = models.Tag.query.get_or_404(random.randint(1,15))
                post.tags.append(tag)
                
            self.db.session.add(post)
