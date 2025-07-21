# =============================================================================
# © 2025 Kashif Ali Siddiqui, Pakistan
# Developed by: Kashif Ali Siddiqui 
# Github: https://github.com/ksiddiqui
# LinkedIn: https://www.linkedin.com/in/ksiddiqui
# Email: kashif.ali.siddiqui@gmail.com
# Dated: July, 2025 
# -----------------------------------------------------------------------------
# This source code is the property of Kashif Ali Siddiqui and is confidential.
# Unauthorized copying or distribution of this file, via any medium, is strictly prohibited.
# =============================================================================

import sys
import os

# Add current directory to sys.path
sys.path.append(os.path.dirname(__file__))

import traceback
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.pretty import Pretty
from rich import box

from system.setup import do_setup
from services.database import DatabaseManager
from services.index_documents import DocumentIndexingManager

config, logger = None, None
console = None

def show_title():    
    console.print(Panel("[bold magenta]Agentic AI Document Search[/bold magenta]", expand=False, box=box.DOUBLE))
    console.print("[bold]Developer:[/bold] Kashif Ali Siddiqui")
    console.print("[bold]LinkedIn:[/bold] https://www.linkedin.com/in/ksiddiqui\n")

def main_menu():
    console.clear()

    show_title()
    
    console.print("[cyan]Menu Options:[/cyan]")
    console.print("1. View names of all indexed documents")
    console.print("2. Index documents")
    console.print("3. Test vector store connection")
    console.print("4. Reset vector store")
    console.print("5. View configuration")
    console.print("6. Exit")
    option = Prompt.ask("\nEnter your choice", choices=["1", "2", "3", "4", "5", "6"])
    return option

def view_indexed_documents():
    table = Table(title="Indexed Documents")
    table.add_column("Name")
    table.add_column("Path")
    table.add_column("Created At")
    table.add_column("Num of Nodes")

    documents = DatabaseManager().view_documents()
    console.print("\nDocuments:")
    for doc in documents:
        # Format creation datetime if it's a datetime object
        created_at = doc.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(doc.created_at, 'strftime') else str(doc.created_at)
        table.add_row(str(doc.name), str(doc.path), created_at, str(doc.num_of_nodes))

    console.clear()
    show_title()
    console.print(table)
    console.input("\nPress Enter to return to menu...")

def index_documents(index_documents_manager:DocumentIndexingManager):
    index_documents_manager.start_indexing_from_directory()
    
    console.input("\nPress Enter to return to menu...")

def test_vector_store_connection(config):
    try:
        DatabaseManager().check_connection()
        console.print("[green]Vector store (PostgreSQL) connection successful![/green]")
    except Exception as e:
        console.print(f"[red]Failed to connect to vector store: {e}[/red]")
    console.input("\nPress Enter to return to menu...")

def reset_vector_store(config):
    try:
        DatabaseManager().delete_all_documents(delete_indices_also=True)
        console.print("[green]Vector store tables dropped/reset![/green]")
    except Exception as e:
        console.print(f"[red]Failed to reset vector store: {e}[/red]")
    console.input("\nPress Enter to return to menu...")

def view_config(config):
    console.print(Panel(Pretty(config), title="Current Configuration", expand=False))
    console.input("\nPress Enter to return to menu...")

def main():
    global config, logger, console
    console = Console()
    try:
        config, logger = do_setup()
    except Exception as e:
        console.print(f"[red]Failed to load configuration. Exception occurred: {e}[/red]")
        traceback.print_exc()
        sys.exit(1)
    finally:
        if not config:
            console.print("[red]Failed to load configuration![/red]")
            sys.exit(1)

    index_documents_manager = DocumentIndexingManager()
    
    while True:
        option = main_menu()
        if option == "1":
            view_indexed_documents()
        elif option == "2":
            index_documents(index_documents_manager)
        elif option == "3":
            test_vector_store_connection(config)
        elif option == "4":
            reset_vector_store(config)
        elif option == "5":
            view_config(config)
        elif option == "6":
            console.print("[bold green]Goodbye![/bold green]")
            sys.exit(0)


if __name__ == "__main__":
    main()
