from rich.console import Console
from core.email_generator import generate_email
from dotenv import load_dotenv
import os
import requests

load_dotenv()
console = Console()

def send_email(contact):
    subject, body = generate_email(contact)

    sender_email = os.getenv("SENDER_EMAIL")
    sender_name = os.getenv("SENDER_NAME", "Ritika")
    brevo_api_key = os.getenv("BREVO_API_KEY")
    dry_run = os.getenv("DRY_RUN", "true").lower() == "true"

    console.print("\n[cyan]Preparing email...[/cyan]")
    console.print(f"[bold]To:[/bold] {contact['email']}")
    console.print(f"[bold]Subject:[/bold] {subject}")
    console.print("[bold]Body:[/bold]")
    console.print(body)

    if dry_run:
        console.print(f"[yellow]DRY RUN is ON. Email preview completed for {contact['email']}[/yellow]")
        return True

    if not brevo_api_key:
        console.print("[red]BREVO_API_KEY missing in .env[/red]")
        return False

    if not sender_email:
        console.print("[red]SENDER_EMAIL missing in .env[/red]")
        return False

    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": sender_name,
            "email": sender_email
        },
        "to": [
    {
        "email": "vritika042@gmail.com",
        "name": contact["name"]
    }
],
        "subject": subject,
        "textContent": body
    }

    headers = {
        "accept": "application/json",
        "api-key": brevo_api_key,
        "content-type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code in [200, 201, 202]:
            console.print(f"[green]Email sent successfully to {contact['email']}[/green]")
            return True

        console.print(f"[red]Failed to send email to {contact['email']}[/red]")
        console.print(f"[red]Status code: {response.status_code}[/red]")
        console.print(response.text)
        return False

    except Exception as e:
        console.print(f"[red]Brevo error: {e}[/red]")
        return False