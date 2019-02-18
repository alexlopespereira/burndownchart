from flask_login import UserMixin
# silly user model
class User(UserMixin):
    def __init__(self, id, email=None, password=None):
        self.id = id
        self.email = email
        self.password = password

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.email, self.password)

users = [User('1', 'teste2', 'teste123456'), User('2', 'teste@teste.com', 'teste')]
