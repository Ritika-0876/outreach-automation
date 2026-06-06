from rich.console import Console

console = Console()

def resolve_email(contact):
    console.print(f"[blue]Step 3: Finding email for {contact['name']}...[/blue]")

    # Dummy email generation for now. Later this will be replaced with Eazyreach API.
    first_name = contact["name"].split()[0].lower()
    contact["email"] = f"{first_name}@{contact['domain']}"
    contact["verified"] = True

    return contact