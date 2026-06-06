from rich.console import Console

console = Console()

def find_decision_makers(company):
    console.print(f"[blue]Step 2: Finding decision maker for {company['domain']}...[/blue]")

    # Dummy data for now. Later this will be replaced with Prospeo API.
    first_name = company["name"].lower()

    return [
        {
            "name": f"{company['name']} Manager",
            "title": "VP Sales",
            "company": company["name"],
            "domain": company["domain"],
            "linkedin": f"https://linkedin.com/in/{first_name}-manager"
        }
    ]