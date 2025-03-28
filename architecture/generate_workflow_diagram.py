from graphviz import Digraph

def create_workflow_diagram():
    dot = Digraph(comment='Salon Booking Workflow')
    dot.attr(rankdir='TB')
    
    # Add nodes
    dot.node('A', 'User Query')
    dot.node('B', 'Supervisor Agent')
    dot.node('C', 'Service Selection Agent')
    dot.node('D', 'Policy Selection Agent')
    dot.node('E', 'Date Selection Agent')
    dot.node('F', 'Slot Selection Agent')
    dot.node('G', 'Final Booking')
    
    # Add edges with labels
    dot.edge('A', 'B', 'Initial Query')
    dot.edge('B', 'C', 'Service Not Selected')
    dot.edge('C', 'B', 'Service Selection')
    dot.edge('B', 'D', 'Policy Not Selected')
    dot.edge('D', 'B', 'Policy Selection')
    dot.edge('B', 'E', 'Date Not Selected')
    dot.edge('E', 'B', 'Date Selection')
    dot.edge('B', 'F', 'Slot Not Selected')
    dot.edge('F', 'B', 'Slot Selection')
    dot.edge('B', 'G', 'All Selected')
    
    # Save the diagram
    dot.render('architecture/workflow_diagram', format='png', cleanup=True)

if __name__ == '__main__':
    create_workflow_diagram() 