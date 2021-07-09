from product.models import Category, Product, Review
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from random import randint

class VirtueleTestBase(TestCase):
    random_word_list = ['apostils', 'estivate', 'rioted', 'doze', 'lexicalizing', 'driftier', 'reinjection', 'musician', 'endosperms', 'cummerbunds', 'masculinizing', 'fabbest', 'semicolonialism', 'fabulous', 'clearstory', 'rared', 'lawmaking', 'confronts', 'conquians', 'morulae', 'pinto', 'dropkicker', 'antisex', 'euryokous', 'outyell', 'reinvigorations', 'brainstormers', 'ogrish', 'grails', 'heaume', 'apollos', 'morselling', 'gausses', 'exostoses', 'degreed', 'castellans', 'gridlocking', 'twirling', 'ordures', 'glum', 'capitulate', 'skill', 'brigandines', 'hustles', 'monolayers', 'forceless', 'felsic', 'procurator', 'fetas', 'conventionalist', 'bitchier', 'hypothecators', 'sniffishnesses', 'resembling', 'wastefully', 'audaciousnesses', 'handfasting', 'woodnotes', 'checkreins', 'corduroys', 'airstrip', 'torturing', 'testify', 'frenziedly', 'iguanian', 'gluten', 'opuntia', 'renitent', 'caprocks', 'nonenergy', 'centralities', 'inamoratas', 'mischanneled', 'morale', 'psychologises', 'abridgment', 'cerebrating', 'tautness', 'stigmatizes', 'endothecium', 'doux', 'contusing', 'dystrophy', 'desirableness', 'hewers', 'putschists', 'financiered', 'roturiers', 'emotionalizes', 'stonewaller', 'measles', 'chertier', 'lignites', 'cosmopolitism', 'bridesmaids', 'sashing', 'denouncements', 'intellect', 'prototyping', 'sociologese']
    
    def user_admin_factory(self):
        get_user_model().objects.create_user(email='admin@admin.com',
                                             password='admin',
                                             first_name='admin',
                                             username='adminGod',
                                             is_active=True,
                                             is_superuser=True)

        get_user_model().objects.create_user(email='user@user.com',
                                             password='user',
                                             first_name='user',
                                             username='punyUser',
                                             is_active=True)

    def account_factory(self, n=3):
        users_count = get_user_model().objects.all().count() + 1
        for i in range(0, n):
            get_user_model().objects.create_user(email=f'user{i+users_count}@user.com',
                                                 password=f'user{i+users_count}',
                                                 first_name='user',
                                                 last_name={i+1},
                                                 username=f'USER{i+users_count}',
                                                 is_active=True)

    def product_factory(self, n=5, category: list=None, with_reviews=False):
        if not category:
            category = [Category.objects.create(name='Placeholder Category').id]

        if with_reviews:
            self.user_admin_factory()

        category_count = len(category)

        for i in range(n):
            p = Product.objects.create(name=' '.join([self.random_word_list[randint(0, 99)] for i in range(2)]).title(),
                                       description=' '.join([self.random_word_list[randint(0, 99)] for i in range(10)]).capitalize(),
                                       price=randint(1000, 1000000),
                                       material=' '.join([self.random_word_list[randint(0, 99)] for i in range(2)]).upper(),
                                       is_featured=(0 == i%2))
            p.category.add(Category.objects.get(id=randint(1, category_count)))
            p.save()

            if with_reviews:
                self.review_factory(product=[p], user=[user for user in get_user_model().objects.all()])

    def review_factory(self, product: list=None, user: list=None):
        if not product:
            self.product_factory(n=5)
            product = [product for product in Product.objects.all()]

        if not user:
            self.user_admin_factory()
            user = [user for user in get_user_model().objects.all()]
        user_count = len(user)
        
        for product in product:
            Review.objects.create(user=user[randint(0, user_count-1)],
                                  product=product,
                                  rating=randint(1, 5),
                                  review=' '.join([self.random_word_list[randint(0, 99)] for i in range(10)]).capitalize())

    def category_factory(self, n=5):
        for i in range(n):
            Category.objects.create(name=' '.join([self.random_word_list[randint(0, 99)] for i in range(2)]).title())

    @property
    def admin_jwt(self):
        user = get_user_model().objects.get(username='adminGod')
        token = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION':f'JWT {token.access_token}'}

    @property
    def user_jwt(self):
        user = get_user_model().objects.get(username='punyUser')
        token = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION':f'JWT {token.access_token}'}

    def account_jwt(self, id):
        user = get_user_model().objects.get(id=id)
        token = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION':f'JWT {token.access_token}'}
