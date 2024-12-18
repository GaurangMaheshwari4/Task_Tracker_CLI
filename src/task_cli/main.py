import typer
from rich.console import Console
from rich.table import Table
from .crud_utils import CRUDUtils

# Create a typer app instance
app = typer.Typer()

# Optionally, create a rich console instance for better output
console = Console()

@app.command()
def add(description: str = typer.Argument(..., help="Description of the task")):
    """
    Adds task to the task list. By default, status of task is todo.
    """
    id = CRUDUtils.add_task(description)
    console.print(f"[green]Task added successfully (ID: {id})[/]")

@app.command()
def update(id: int = typer.Argument(..., help="ID of the task to be updated"), description: str = typer.Argument(..., help="Updated description of the task")):
    """
    Update Description of the task using ID
    """
    response = CRUDUtils.update_task(id, description)
    console.print(response)

@app.command()
def delete(id: int = typer.Argument(..., help="ID of the task to be deleted")):
    """
    Delete the task from task list using ID
    """
    response = CRUDUtils.delete_task(id)
    console.print(response)

@app.command()
def mark_in_progress(id: int = typer.Argument(..., help="ID of the task whose status needs to be changed to in-progress")):
    """
    Update status of the task to in-progress using ID
    """
    response = CRUDUtils.update_task_status(id, 'in-progress')
    console.print(response)

@app.command()
def mark_done(id: int = typer.Argument(..., help="ID of the task whose status needs to be changed to done")):
    """
    Update status of the task to done using ID
    """
    response = CRUDUtils.update_task_status(id, 'done')
    console.print(response)

@app.command()
def list(status: str = typer.Argument('All', help="Status of the task that needs to be fetched, By default 'All' ( Optional ). Available options: [ todo / in-progress / done ]")):
    """
    List the tasks based on status
    """
    data = CRUDUtils.list_tasks(status)
    if not len(data):
        console.print('[red]No tasks available ![/]')
    else:
        table = Table(title="Task List", show_lines=True)
        cols = ['ID', 'Description', 'Status', 'Created at', 'Updated at']
        row_color = {
            'todo': 'blue',
            'in-progress': 'yellow',
            'done': 'green'
        }
        # Define table columns
        for col in cols:
            table.add_column(col, no_wrap=True)

        for row_data in data:
            table.add_row(row_data['id'], row_data['description'], row_data['status'], row_data['createdAt'], row_data['updatedAt'], style=row_color[row_data['status']])
        
        # Display the table
        console.print(table)
        



if __name__ == "__main__":
    app()
