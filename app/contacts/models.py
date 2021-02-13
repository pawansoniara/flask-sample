from datetime import datetime

from app.database import db


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=20), unique=True, index=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    emails = db.relationship(
        "ContactEmail",
        back_populates="contact",
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "order_by": created_at
    }
    __tablename__ = 'contact'

    def __repr__(self):
        return (
            '<{class_name}('
            'contact_id={self.id}, '
            'username="{self.username}")>'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )


class ContactEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship("Contact")
    email = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    __mapper_args__ = {
        "order_by": created_at
    }
    __tablename__ = 'contact_email'

    def __repr__(self):
        return (
            '<{class_name}('
            'contact_id={self.id}, '
            'username="{self.contact.username}")'
            'email="{self.email}">'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
