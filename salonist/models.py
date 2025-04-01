from datetime import datetime
from salonist.database import db

class Service(db.Model):
    """Insurance service model."""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with packages
    packages = db.relationship('Package', back_populates='service', lazy='dynamic')
    
    def __init__(self, name: str, duration: int, price: float):
        self.name = name
        self.duration = duration
        self.price = price
    
    def __repr__(self):
        return f'<Service {self.name}>'

class Package(db.Model):
    """Service package model."""
    __tablename__ = 'packages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    coverage_amount = db.Column(db.Float, nullable=False)
    premium = db.Column(db.Float, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with service
    service = db.relationship('Service', back_populates='packages')
    
    def __repr__(self):
        return f'<Package {self.name}>'

class ServiceRequest(db.Model):
    """Model to store user service inquiries."""
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    service = db.relationship('Service')
    package = db.relationship('Package')
    
    def __repr__(self):
        return f'<ServiceRequest {self.user_name} - {self.service.name}>' 