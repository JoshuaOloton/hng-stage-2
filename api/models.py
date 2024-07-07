from api import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.String(256), primary_key=True, unique=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(15))
    organisations = db.relationship('Organisation', secondary='user_organisations', backref=db.backref('users', lazy='dynamic'))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
        
    def has_common_organisation(self, user):
        """Check if this user has any common organisation with another user."""
        return any(org in user.organisations for org in self.organisations)

    def to_json(self):
        return {
            "userId": self.userId,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "phone": self.phone
        }
    
    def __repr__(self) -> str:
        return f'<User {self.userId} -> {self.firstName}>'


class Organisation(db.Model):
    __tablename__ = 'organisations'
    orgId = db.Column(db.String(256), primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    def to_json(self):
        return {
            "orgId": self.orgId,
            "name": self.name,
            "description": self.description
        }

    def __repr__(self) -> str:
        return f'<Organisation -> {self.name}>'


user_organisations = db.Table('user_organisations',
    db.Column('userId', db.String(256), db.ForeignKey('users.userId')),
    db.Column('orgId', db.String(256), db.ForeignKey('organisations.orgId'))
)