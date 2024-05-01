from db import db

class ActivityModel(db.Model):
    __tablename__ = "activity"

    activity_id = db.Column(db.Integer, primary_key=True)
    park_id = db.Column(db.Integer, db.ForeignKey('park.park_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.Float, nullable=False)
    require_special_equipment = db.Column(db.Boolean, nullable=False)

    # park = db.relationship("ParkModel", back_populates="activities")

    def json(self):
        return {
            "activity_id": self.activity_id,
            "park_id": self.park_id,
            "name": self.name,
            "description": self.description,
            "duration": self.duration,
            "difficulty": self.difficulty,
            "require_special_equipment": self.require_special_equipment
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
