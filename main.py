from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
import pandas as pd
import os
load_dotenv()

from services.ocean_service import find_similar_companies
from services.prospeo_service import find_decision_makers
from services.eazyreach_service import resolve_email
from services.brevo_service import send_email
from core.dedupe import remove_duplicates
console = Console()

def main():
    seed_domain = input("Enter company domain: ").strip()

    if not seed_domain:
        console.print("[red]Please enter a valid company domain.[/red]")
        return

    companies = find_similar_companies(seed_domain)

    all_contacts = []
    for company in companies:
        contacts = find_decision_makers(company)
        all_contacts.extend(contacts)

    verified_contacts = []
    for contact in all_contacts:
        contact = resolve_email(contact)
        if contact.get("verified"):
            verified_contacts.append(contact)
    verified_contacts = remove_duplicates(verified_contacts)
    table = Table(title="Final Outreach Summary")
    table.add_column("Name")
    table.add_column("Title")
    table.add_column("Company")
    table.add_column("Email")

    for contact in verified_contacts:
        table.add_row(
            contact["name"],
            contact["title"],
            contact["company"],
            contact["email"]
        )

    console.print("\n")
    console.print(table)

    os.makedirs("output", exist_ok=True)

    df = pd.DataFrame(verified_contacts)
    df.to_csv("output/final_recipients.csv", index=False)

    console.print("[green]CSV saved: output/final_recipients.csv[/green]")

    confirm = input("\nDo you want to send emails? yes/no: ").strip().lower()

    dry_run = os.getenv("DRY_RUN", "true").lower() == "true"

    if confirm == "yes":
        if dry_run:
            console.print("[yellow]DRY RUN mode is ON. Emails are previewed but not actually sent.[/yellow]")

        for contact in verified_contacts:
            send_email(contact)
    else:
        console.print("[yellow]Emails not sent.[/yellow]")

if __name__ == "__main__":
    main()