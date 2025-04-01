import click
from flask.cli import with_appcontext
from .database import db
from .models import Service, Package
from .booking.workflow import BookingWorkflow
from .agent.graph import graph as agent_graph
import os

@click.command('clean-db')
@with_appcontext
def clean_db():
    """Remove all data from the database."""
    try:
        Package.query.delete()
        Service.query.delete()
        db.session.commit()
        click.echo('Successfully cleaned the database.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error cleaning database: {str(e)}')

@click.command('seed-db')
@with_appcontext
def seed_db():
    """Seed the database with initial salon data."""
    try:
        # Create services
        haircut = Service(
            name='Haircut',
            duration=30,
            price=25.0
        )
        hair_coloring = Service(
            name='Hair Coloring',
            duration=120,
            price=100.0
        )
        facial = Service(
            name='Facial',
            duration=60,
            price=70.0
        )
        manicure = Service(
            name='Manicure',
            duration=45,
            price=35.0
        )
        pedicure = Service(
            name='Pedicure',
            duration=60,
            price=45.0
        )
        
        db.session.add_all([haircut, hair_coloring, facial, manicure, pedicure])
        db.session.flush()  # This will assign IDs to services
        
        # Create packages
        packages = [
            Package(**{
                'name': 'Basic Hair Care Package',
                'description': 'Basic haircut and styling',
                'coverage_amount': 25.0,
                'premium': 25.0,
                'service_id': haircut.id
            }),
            Package(**{
                'name': 'Premium Hair Care Package',
                'description': 'Haircut, coloring, and styling',
                'coverage_amount': 125.0,
                'premium': 125.0,
                'service_id': hair_coloring.id
            }),
            Package(**{
                'name': 'Facial Treatment Package',
                'description': 'Complete facial treatment with cleansing and massage',
                'coverage_amount': 70.0,
                'premium': 70.0,
                'service_id': facial.id
            }),
            Package(**{
                'name': 'Hand & Foot Care Package',
                'description': 'Manicure and pedicure treatment',
                'coverage_amount': 80.0,
                'premium': 80.0,
                'service_id': manicure.id
            }),
            Package(**{
                'name': 'Luxury Spa Package',
                'description': 'Complete spa experience including all services',
                'coverage_amount': 275.0,
                'premium': 275.0,
                'service_id': facial.id
            })
        ]
        
        db.session.add_all(packages)
        db.session.commit()
        click.echo('Successfully seeded the database with salon services and packages.')
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
        packages = service.packages.all()
        if packages:
            click.echo('Packages:')
            for package in packages:
                click.echo(f'  - {package.name} (₹{package.premium:.2f}, Duration: {service.duration} minutes)')

@click.command('visualize-graph')
def visualize_graph():
    """Visualize the booking workflow graph."""
    try:
        click.echo("Creating workflow instance...")
        workflow = BookingWorkflow()
        graph = workflow.graph
        
        click.echo("Creating output directory...")
        os.makedirs('output', exist_ok=True)
        output_path = 'output/workflow_graph.png'
        
        click.echo("Generating visualization...")
        # Get PNG bytes
        png_bytes = graph.get_graph().draw_mermaid_png()
        
        # Save to file
        with open(output_path, 'wb') as f:
            f.write(png_bytes)
            
        click.echo(f"Graph visualization saved to {output_path}")
    except Exception as e:
        click.echo(f"Error visualizing graph: {str(e)}")
        import traceback
        click.echo(traceback.format_exc())


@click.command('visualize-agent')
def visualize_agent():
    """Visualize the booking workflow graph."""
    try:
        click.echo("Creating workflow instance...")

        click.echo("Creating output directory...")
        os.makedirs('output', exist_ok=True)
        output_path = 'output/agent_workflow_graph.png'

        click.echo("Generating visualization...")
        # Get PNG bytes
        png_bytes = agent_graph.get_graph().draw_mermaid_png()

        # Save to file
        with open(output_path, 'wb') as f:
            f.write(png_bytes)

        click.echo(f"Graph visualization saved to {output_path}")
    except Exception as e:
        click.echo(f"Error visualizing graph: {str(e)}")
        import traceback
        click.echo(traceback.format_exc())