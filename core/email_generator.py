def generate_email(contact):
    first_name = contact["name"].split()[0]
    company_name = contact["company"]

    subject = f"Quick idea for {company_name}"

    body = f"""
Hi {first_name},

I came across {company_name} and noticed your work in the industry.

I built a small automation pipeline that helps companies reduce manual prospecting and improve outreach efficiency.

Would you be open to a quick 10-minute conversation this week?

Best,
Ritika
"""

    return subject, body