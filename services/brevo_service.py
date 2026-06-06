from rich.console import Console
from core.email_generator import generate_email

console = Console()

def send_email(contact):
    # Dummy sending for now. Later this will be replaced with Brevo API.
    subject, body = generate_email(contact)

    console.print("\n[cyan]Preparing email...[/cyan]")
    console.print(f"[bold]To:[/bold] {contact['email']}")
    console.print(f"[bold]Subject:[/bold] {subject}")
    console.print("[bold]Body:[/bold]")
    console.print(body)

    console.print(f"[green]Email preview completed for {contact['email']}[/green]")