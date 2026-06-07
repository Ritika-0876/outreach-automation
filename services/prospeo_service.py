from rich.console import Console
from dotenv import load_dotenv
import os
import requests

load_dotenv()
console = Console()

TARGET_SENIORITIES = [
    "Founder/Owner",
    "C-Level",
    "VP",
    "Director",
    "Head"
]

def find_decision_makers(company):
    console.print(f"[blue]Step 2: Finding decision makers using Prospeo for {company['domain']}...[/blue]")

    prospeo_api_key = os.getenv("PROSPEO_API_KEY")
    max_contacts = int(os.getenv("MAX_CONTACTS_PER_COMPANY", 2))

    if not prospeo_api_key:
        console.print("[yellow]PROSPEO_API_KEY missing. Using fallback mock contact.[/yellow]")
        return fallback_contacts(company)

    url = "https://api.prospeo.io/search-person"

    headers = {
        "X-KEY": prospeo_api_key,
        "Content-Type": "application/json"
    }

    payload = {
    "page": 1,
    "filters": {
        "company": {
            "websites": {
                "include": [
                    company["domain"]
                ]
            }
        }
    }
}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code not in [200, 201]:
            console.print("[yellow]Prospeo API failed. Using fallback mock contact.[/yellow]")
            console.print(f"[red]Status code: {response.status_code}[/red]")
            console.print(response.text)
            return fallback_contacts(company)

        data = response.json()

        console.print("[cyan]Prospeo raw response received.[/cyan]")
        
        # Prospeo response structure may contain data/results/people depending on plan/version.
        people = (
    data.get("items")
    or data.get("people")
    or data.get("results")
    or data.get("data")
    or []
)

        contacts = []

        for item in people[:max_contacts]:
            person = item.get("person", item)

            first_name = person.get("first_name") or person.get("firstName") or ""
            last_name = person.get("last_name") or person.get("lastName") or ""
            full_name = person.get("full_name") or person.get("name") or f"{first_name} {last_name}".strip()

            title = (
                person.get("current_job_title")
                or person.get("job_title")
                or person.get("title")
                or person.get("position")
                or "Decision Maker"
    )

            linkedin = (
                person.get("linkedin_url")
                or person.get("linkedin")
                or person.get("linkedinUrl")
                or ""
    )

            if full_name:
                contacts.append({
                "name": full_name,
                "title": title,
                "company": company["name"],
                "domain": company["domain"],
                "linkedin": linkedin
        })

        if not contacts:
            console.print("[yellow]No decision makers returned from Prospeo. Using fallback mock contact.[/yellow]")
            return fallback_contacts(company)

        console.print(f"[green]Prospeo returned {len(contacts)} decision maker(s).[/green]")
        return contacts

    except Exception as e:
        console.print(f"[red]Prospeo error: {e}[/red]")
        console.print("[yellow]Using fallback mock contact.[/yellow]")
        return fallback_contacts(company)


def fallback_contacts(company):
    first_name = company["name"].lower().replace(" ", "-")

    return [
        {
            "name": f"{company['name']} Manager",
            "title": "VP Sales",
            "company": company["name"],
            "domain": company["domain"],
            "linkedin": f"https://linkedin.com/in/{first_name}-manager"
        }
    ]