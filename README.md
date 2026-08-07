# Intent Miner JSON Generator

A simple browser-based tool to transform utterances or Genesys Cloud exports into the JSON format required for **Genesys Intent Miner**.

No installation required. Simply open the HTML file in your web browser and start generating Intent Miner-ready JSON.

---

## Features

- Convert **plain text utterances** into Intent Miner format
- Support for **Genesys CSV exports**
- Handles **multi-turn conversations** (customer + agent)
- Live **conversation counter**
- Built-in **warnings panel (toggle view)**
- Enforces Genesys limits:
  - Max **30,000 conversations**
  - Max **500 characters per transcript**
  - Max **100 characters per conversation ID**
- Auto:
  - Split large datasets into multiple files
  - Trim long transcripts
  - Trim long conversation IDs
- Built-in **JSON preview**
- Browser-based UI
- Works offline after download
- No installation required

---

## Supported Inputs

### 1. Text Input

Paste utterances (one per line):

```text
pay my bill
check balance
cancel subscription
```

---

### 2. CSV Input (Genesys Export)

Supports flexible column names such as:

#### Conversation ID
- `conversation_id`
- `Conversation Id`
- `id`

#### Participant
- `participant`
- `Participant Purpose`
- `role`

#### Text
- `transcript`
- `utterance`
- `text`
- `message`
- `body`
- `segment text`

Example:

```csv
conversation_id,participant,transcript
id_1,customer,I want to pay my bill
id_1,agent,Sure, how would you like to pay?
```

---

## Output Format

Generates JSON compatible with Genesys Intent Miner:

```json
{
  "locale": "en-us",
  "conversations": [
    {
      "id": "id_1",
      "turns": [
        {
          "participant": "customer",
          "transcript": "pay my bill"
        }
      ]
    }
  ]
}
```

---

## Validation Rules (Genesys Limits)

This tool automatically enforces:

- Max 30,000 conversations per file
- Max 500 characters per transcript
- Max 100 characters per conversation ID

If limits are exceeded:

- Long transcripts are **automatically trimmed**
- Long conversation IDs are **automatically truncated**
- Large datasets can be **split into multiple files**

---

## Warnings Panel

The tool tracks and displays data issues in a dedicated **Warnings panel**.

Click **"View Warnings"** to toggle visibility.

Examples of warnings:

- Transcript exceeded 500 characters (trimmed)
- Conversation ID exceeded 100 characters (truncated)

This helps you quickly identify and troubleshoot problematic rows in your dataset.

---

## How to Use

1. Download the HTML file.
2. Open it in any modern web browser:
   - Chrome
   - Edge
   - Firefox
   - Safari
3. Either:
   - Paste utterances
   - OR upload TXT/CSV file
4. Review:
   - Conversation count
   - Warning count
5. Click **View Warnings** (optional) to inspect issues
6. Click **Preview** to review JSON output
7. Click **Generate JSON**
8. Upload output file(s) into Genesys Intent Miner

---

## Requirements

### Recommended

Simply open the HTML file in your browser.

No installation, Python setup, or additional dependencies are required.

### Supported Browsers

- Microsoft Edge
- Google Chrome
- Mozilla Firefox
- Safari

---

## Notes

- No Genesys API required (this is a formatting tool)
- Works entirely on your local machine
- No data is uploaded to external services
- Works with most Genesys export formats
- If your CSV is not recognized, check column names
- Warnings do not block generation — they are informational

---

## Users

Designed for:

- Conversation Designers
- NLP / Intent Training Teams
- Genesys Cloud Administrators
- Business Analysts preparing Intent Miner datasets

---

## Summary

This tool removes manual work, enforces platform limits, and provides visibility into data issues to prevent upload errors when preparing datasets for Genesys Intent Miner.

---