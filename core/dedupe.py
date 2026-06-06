def remove_duplicates(contacts):
    seen_emails = set()
    seen_linkedin = set()
    unique_contacts = []

    for contact in contacts:
        email = contact.get("email")
        linkedin = contact.get("linkedin")

        if email in seen_emails or linkedin in seen_linkedin:
            continue

        if email:
            seen_emails.add(email)

        if linkedin:
            seen_linkedin.add(linkedin)

        unique_contacts.append(contact)

    return unique_contacts