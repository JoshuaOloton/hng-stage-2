from api import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.Integer, primary_key=True, unique=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(15))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'userId': self.userId,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'password': self.password_hash,
            'phone': self.phone
        }
    
    def __repr__(self) -> str:
        return f'<User {self.userId} -> {self.firstName}>'


class Organization(db.Model):
    __tablename__ = 'organizations'
    orgID = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self) -> str:
        return f'<Organization -> {self.name}>'