# Outreach Automation Pipeline

This is a command-line automation tool that takes one company domain as input and runs a cold outreach pipeline.

## Workflow

1. User enters one company domain
2. System finds similar companies
3. System finds decision makers
4. System resolves work emails
5. System shows final summary
6. User confirms before emails are sent

## Current Status

This version contains a working pipeline structure with:

* CLI input
* Similar company finder
* Decision-maker finder
* Email resolver
* Safety checkpoint
* CSV export
* Duplicate removal
* Email template generator
* Dry-run mode
* API keys configured through `.env`

## How to Run

```bash
python main.py
```

Then enter a company domain:

```text
iamkeerthivasan.in
```

## Safety Feature

This project includes a safety checkpoint before sending emails.

The user must confirm:

```text
Do you want to send emails? yes/no
```

Also, `DRY_RUN=true` is enabled in the `.env` file, so emails are previewed safely during testing and demo.

## API Integrations

The project is structured for these integrations:

* Ocean.io for lookalike companies
* Prospeo for decision makers
* EazyReach for verified work emails
* Brevo for sending outreach emails

Current demo runs in dry-run/mock mode where required.

## Output

The final recipients are saved in:

```text
output/final_recipients.csv
```

## Integration Status

- Ocean.io API is attempted first for lookalike company search.
- Since Ocean.io returned no companies in the current account, Prospeo Search Company API is used as an alternative.
- Prospeo Search Person API is used to find real decision-makers with job titles and LinkedIn details.
- As per the updated FAQ, EazyReach is not required. Prospeo is used as the main replacement for EazyReach, and Hunter.io is used as an additional email resolving API when email data is unavailable.
- Brevo API is configured for outreach email sending.
- A safety checkpoint is included before emails are sent.
- `DRY_RUN=true` previews emails safely, and `DRY_RUN=false` enables real sending.


## Author

Ritika Verma
