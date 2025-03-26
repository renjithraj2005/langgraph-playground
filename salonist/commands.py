import click
from flask.cli import with_appcontext
from .database import db
from .models import Service, Policy

@click.command('clean-db')
@with_appcontext
def clean_db():
    """Remove all data from the database."""
    try:
        Policy.query.delete()
        Service.query.delete()
        db.session.commit()
        click.echo('Successfully cleaned the database.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error cleaning database: {str(e)}')

@click.command('seed-db')
@with_appcontext
def seed_db():
    """Seed the database with initial data."""
    try:
        # Create services
        health_insurance = Service(**{'name': 'Health Insurance'})
        vehicle_insurance = Service(**{'name': 'Vehicle Insurance'})
        
        db.session.add_all([health_insurance, vehicle_insurance])
        db.session.flush()  # This will assign IDs to services
        
        # Create policies
        policies = [
            Policy(**{
                'name': 'Basic Health Cover',
                'description': 'Basic health insurance coverage for individuals',
                'coverage_amount': 100000.00,
                'premium': 5000.00,
                'service_id': health_insurance.id
            }),
            Policy(**{
                'name': 'Premium Health Cover',
                'description': 'Comprehensive health insurance with additional benefits',
                'coverage_amount': 500000.00,
                'premium': 15000.00,
                'service_id': health_insurance.id
            }),
            Policy(**{
                'name': 'Third Party Vehicle Insurance',
                'description': 'Basic vehicle insurance covering third party damages',
                'coverage_amount': 50000.00,
                'premium': 2000.00,
                'service_id': vehicle_insurance.id
            }),
            Policy(**{
                'name': 'Comprehensive Vehicle Insurance',
                'description': 'Full coverage vehicle insurance including own damages',
                'coverage_amount': 200000.00,
                'premium': 8000.00,
                'service_id': vehicle_insurance.id
            })
        ]
        
        # Add to session and commit
        db.session.bulk_save_objects(policies)
        db.session.commit()
        
        click.echo('Successfully added insurance services and policies to database.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error seeding database: {str(e)}')

@click.command('list-services')
@with_appcontext
def list_services():
    """List all services in the database."""
    services = Service.query.all()
    if not services:
        click.echo('No services found in database.')
        return
    
    for service in services:
        click.echo(f'\nService - ID: {service.id}, Name: {service.name}')
        policies = service.policies.all()
        if policies:
            click.echo('Policies:')
            for policy in policies:
                click.echo(f'  - {policy.name} (₹{policy.premium:.2f}/year, Coverage: ₹{policy.coverage_amount:.2f})') 