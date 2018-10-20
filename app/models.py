from app import db

class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_contact = db.Column(db.Integer, db.ForeignKey('citizen.id'))
    last_contact = db.Column(db.DateTime)

    def __repr__(self):
        return '<Party {}>'.format(self.id)


class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'))
    location = db.Column(db.Integer, db.ForeignKey('location.id'))
    is_mobile = db.Column(db.Boolean)
    is_safe = db.Column(db.Boolean)

    def __repr__(self):
        return '<Citizen {}>'.format(self.name)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128))
    zip = db.Column(db.Integer)

    def __repr__(self):
        return '<Location {}>'.format(self.id)


class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)


class PartySupply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'))
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'))
    have = db.Column(db.Boolean)
