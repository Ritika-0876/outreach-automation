from rich.console import Console

console = Console()

def find_similar_companies(seed_domain):
    console.print("\n[blue]Step 1: Finding similar companies...[/blue]")

    # Dummy data for now. Later this will be replaced with Ocean.io API.
    return [
        {"name": "Freshworks", "domain": "freshworks.com"},
        {"name": "Zoho", "domain": "zoho.com"},
        {"name": "HubSpot", "domain": "hubspot.com"},
    ]