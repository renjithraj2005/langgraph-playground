import click
from .langgraph.workflow import SearchWorkflow

@click.group()
def cli():
    """Salonist CLI"""
    pass

@cli.command()
@click.argument('query')
def search(query: str):
    """Search for information using the AI agent."""
    try:
        workflow = SearchWorkflow()
        response, processing_time = workflow.run(query)
        click.echo("\nResponse:")
        click.echo(response)
        click.echo(f"\nProcessing time: {round(processing_time, 2)}s")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    cli() 