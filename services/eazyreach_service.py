from rich.console import Console
from dotenv import load_dotenv
import os
import requests

load_dotenv()
console = Console()


def resolve_email(contact):
    console.print(f"Step 3: Resolving email for {contact['name']} using Hunter.io...")

    hunter_api_key = os.getenv("HUNTER_API_KEY")

    if not hunter_api_key:
        console.print("[yellow]HUNTER_API_KEY missing. Using fallback email.[/yellow]")
        return fallback_email(contact)

    name_parts = contact["name"].split()
    first_name = name_parts[0] if len(name_parts) > 0 else ""
    last_name = name_parts[-1] if len(name_parts) > 1 else ""

    domain = contact.get("domain")

    if not first_name or not domain:
        console.print("[yellow]Missing name/domain. Using fallback email.[/yellow]")
        return fallback_email(contact)

    url = "https://api.hunter.io/v2/email-finder"

    params = {
        "domain": domain,
        "first_name": first_name,
        "last_name": last_name,
        "api_key": hunter_api_key
    }

    try:
        response = requests.get(url, params=params, timeout=30)

        if response.status_code != 200:
            console.print("[yellow]Hunter API failed. Using fallback email.[/yellow]")
            console.print(f"[red]Status code: {response.status_code}[/red]")
            console.print(response.text)
            return fallback_email(contact)

        data = response.json()
        result = data.get("data", {})

        email = result.get("email")
        score = result.get("score")

        if email:
            contact["email"] = email
            contact["verified"] = True
            contact["email_confidence"] = score
            console.print(f"[green]Hunter found email: {email} | confidence: {score}[/green]")
            return contact

        console.print("[yellow]Hunter returned no email. Using fallback email.[/yellow]")
        return fallback_email(contact)

    except Exception as e:
        console.print(f"[red]Hunter error: {e}[/red]")
        return fallback_email(contact)


def fallback_email(contact):
    first_name = contact["name"].split()[0].lower()
    domain = contact.get("domain", "").replace("www.", "")

    contact["email"] = f"{first_name}@{domain}"
    contact["verified"] = False
    contact["email_confidence"] = None

    return contact