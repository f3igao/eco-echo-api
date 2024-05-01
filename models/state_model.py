from db import db

class StateModel(db.Model):
    __tablename__ = "state"

    state_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255), nullable=False)

    # parks = db.relationship("ParkModel", back_populates="state", secondary="park_state")

    def json(self):
        return {
            "state_id": self.state_id,
            "name": self.name,
            "region": self.region
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
