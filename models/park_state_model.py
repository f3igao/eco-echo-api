from db import db

class ParkStateModel(db.Model):
    __tablename__ = "park_state"

    park_state_id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('park.park_id'), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'), nullable=False)

    def json(self):
        return {
            "park_state_id": self.park_state_id,
            "park_id": self.park_id,
            "state_id": self.state_id
        }

    @classmethod
    def find_by_park_id_and_state_id(cls, park_id, state_id):
        return cls.query.filter_by(park_id=park_id, state_id=state_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
