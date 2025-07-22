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
os.environ['OTEL_SDK_DISABLED'] = 'true'

import traceback
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.pretty import Pretty
from rich import box

from system.setup import do_setup
from models.chat_completion import ChatRequest
from services.database import DatabaseManager
from services.index_documents import DocumentIndexingManager
from services.chat_completion import ChatCompletionService

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
    console.print("--------------------------------")
    console.print("1. Chat with documents")
    # console.print("")
    console.print("2. View names of all indexed documents")
    console.print("3. Index documents")
    console.print("4. Test vector store connection")
    console.print("5. Reset vector store")
    console.print("6. View configuration")
    # console.print("")
    console.print("7. Exit")
    option = Prompt.ask("\nEnter your choice", choices=["1", "2", "3", "4", "5", "6", "7"])
    return option

def chat_with_documents(config):
    console.clear()
    show_title()
    console.print("\nChat with documents:")
    console.print("----------------------")
    console.print("Enter 'exit' to return to menu.")
    console.print("----------------------\n")
    
    chat_completion_service = ChatCompletionService()
    chat_request = ChatRequest(model="ollama", messages=[])

    while True:
        user_input = Prompt.ask("You")
        if user_input.lower() == "exit":
            break
        chat_request.messages.append({"role": "user", "content": user_input})
        
        try:
            console.print("AI: [bold]Processing...[/bold]")
            
            response = chat_completion_service.chat_completion(chat_request)
            response_to_display = response.get("choices")[0].get("message", {}).get("content", "")

            console.print(response_to_display)
            chat_request.messages.append({"role": "assistant", "content": response_to_display})
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

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
            chat_with_documents(config)
        elif option == "2":
            view_indexed_documents()
        elif option == "3":
            index_documents(index_documents_manager)
        elif option == "4":
            test_vector_store_connection(config)
        elif option == "5":
            reset_vector_store(config)
        elif option == "6":
            view_config(config)
        elif option == "7":
            console.print("[bold green]Goodbye![/bold green]")
            sys.exit(0)


if __name__ == "__main__":
    main()
