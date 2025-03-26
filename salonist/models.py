from datetime import datetime
from salonist.database import db

class Service(db.Model):
    """Insurance service model."""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with policies
    policies = db.relationship('Policy', back_populates='service', lazy='dynamic')
    
    def __repr__(self):
        return f'<Service {self.name}>'

class Policy(db.Model):
    """Insurance policy model."""
    __tablename__ = 'policies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    coverage_amount = db.Column(db.Float, nullable=False)
    premium = db.Column(db.Float, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with service
    service = db.relationship('Service', back_populates='policies')
    
    def __repr__(self):
        return f'<Policy {self.name}>'

class ServiceRequest(db.Model):
    """Model to store user service inquiries."""
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    service = db.relationship('Service')
    policy = db.relationship('Policy')
    
    def __repr__(self):
        return f'<ServiceRequest {self.user_name} - {self.service.name}>' 