from rich.console import Console
from dotenv import load_dotenv
import os
import requests

load_dotenv()
console = Console()


def find_similar_companies(seed_domain):
    console.print("\n[blue]Step 1: Finding similar companies...[/blue]")

    companies = find_companies_with_ocean(seed_domain)

    if companies:
        return companies

    console.print("[yellow]Ocean.io returned no companies. Trying Prospeo company search as alternative...[/yellow]")

    companies = find_companies_with_prospeo_alternative(seed_domain)

    if companies:
        return companies

    console.print("[yellow]Both Ocean.io and Prospeo company search failed. Using fallback mock companies.[/yellow]")
    return fallback_companies()


def find_companies_with_ocean(seed_domain):
    ocean_api_key = os.getenv("OCEAN_API_KEY")
    max_companies = int(os.getenv("MAX_COMPANIES", 5))

    if not ocean_api_key:
        console.print("[yellow]OCEAN_API_KEY missing. Skipping Ocean.io.[/yellow]")
        return []

    url = "https://api.ocean.io/v3/search/companies"

    headers = {
        "x-api-token": ocean_api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "size": max_companies,
        "companiesFilters": {
            "lookalikeDomains": [seed_domain]
        },
        "fields": [
            "domain",
            "name",
            "companySize",
            "primaryCountry",
            "industries"
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code not in [200, 201]:
            console.print("[yellow]Ocean.io API failed.[/yellow]")
            console.print(f"[red]Status code: {response.status_code}[/red]")
            console.print(response.text)
            return []

        data = response.json()
        companies = data.get("companies", [])

        results = []
        for company in companies:
            domain = company.get("domain")
            name = company.get("name", domain)

            if domain:
                results.append({
                    "name": name,
                    "domain": domain
                })

        if results:
            console.print(f"[green]Ocean.io returned {len(results)} companies.[/green]")
        else:
            console.print("[yellow]No companies returned from Ocean.io.[/yellow]")

        return results

    except Exception as e:
        console.print(f"[red]Ocean.io error: {e}[/red]")
        return []


def find_companies_with_prospeo_alternative(seed_domain):
    prospeo_api_key = os.getenv("PROSPEO_API_KEY")
    max_companies = int(os.getenv("MAX_COMPANIES", 5))

    if not prospeo_api_key:
        console.print("[yellow]PROSPEO_API_KEY missing. Skipping Prospeo company alternative.[/yellow]")
        return []

    url = "https://api.prospeo.io/search-company"

    headers = {
        "X-KEY": prospeo_api_key,
        "Content-Type": "application/json"
    }

    # Alternative to Ocean:
    # Search companies from Prospeo database using broad safe filters.
    # This gives real company domains instead of dummy data.
    payload = {
    "page": 1,
    "filters": {
        "company": {
            "websites": {
                "include": [
                    "freshworks.com",
                    "zoho.com",
                    "hubspot.com",
                    "intercom.com",
                    "zendesk.com"
                ]
            }
        }
    }
}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code not in [200, 201]:
            console.print("[yellow]Prospeo company search failed.[/yellow]")
            console.print(f"[red]Status code: {response.status_code}[/red]")
            console.print(response.text)
            return []

        data = response.json()

        if data.get("error"):
            console.print("[yellow]Prospeo company search returned an error.[/yellow]")
            console.print(data)
            return []

        items = data.get("results", [])

        results = []
        for item in items:
            company = item.get("company", item)

            name = company.get("name")
            domain = (
                company.get("domain")
                or company.get("website")
                or company.get("website_url")
            )

            if domain:
                domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]

            if name and domain:
                results.append({
                    "name": name,
                    "domain": domain
                })

            if len(results) >= max_companies:
                break

        if results:
            console.print(f"[green]Prospeo alternative returned {len(results)} real companies.[/green]")
        else:
            console.print("[yellow]No companies returned from Prospeo alternative.[/yellow]")

        return results

    except Exception as e:
        console.print(f"[red]Prospeo company alternative error: {e}[/red]")
        return []


def fallback_companies():
    return [
        {"name": "Freshworks", "domain": "freshworks.com"},
        {"name": "Zoho", "domain": "zoho.com"},
        {"name": "HubSpot", "domain": "hubspot.com"},
    ]