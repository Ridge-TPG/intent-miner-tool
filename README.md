# Intent Miner JSON Generator

A simple browser-based tool to transform utterances or Genesys Cloud exports into the JSON format required for **Genesys Intent Miner**.

No installation required. Simply open the HTML file in your web browser and start generating Intent Miner-ready JSON.

---

## Features

- Convert **plain text utterances** into Intent Miner format
- Support for **Genesys CSV exports**
- Supports **Genesys-style exported tables**
- Handles **multi-turn conversations** using customer and agent turns
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

Paste utterances, one per line:

```text
pay my bill
check balance
cancel subscription
```

Each line becomes a separate conversation with one customer turn.

---

### 2. CSV Input

Supports flexible column names such as:

#### Conversation ID

- `conversation_id`
- `Conversation ID`
- `Conversation Id`
- `id`
- `Session ID`

#### Customer Text

- `utterance`
- `Utterance`
- `User Utterance`
- `Customer Utterance`
- `text`
- `message`
- `transcript`

#### Agent Text

- `prompt`
- `Prompt`
- `Agent Prompt`
- `Bot Prompt`
- `Agent Response`
- `Response`
- `Reply`

Example:

```csv
Conversation ID,Utterance,Prompt
id_1,I want to pay my bill,Please let me know your account number
id_1,123456,Thanks. What amount would you like to pay?
```

This generates:

```json
{
  "locale": "en-us",
  "conversations": [
    {
      "id": "id_1",
      "turns": [
        {
          "participant": "customer",
          "transcript": "I want to pay my bill"
        },
        {
          "participant": "agent",
          "transcript": "Please let me know your account number"
        },
        {
          "participant": "customer",
          "transcript": "123456"
        },
        {
          "participant": "agent",
          "transcript": "Thanks. What amount would you like to pay?"
        }
      ]
    }
  ]
}
```

---

### 3. Genesys Table / Markdown Table Input

The tool also supports exported Genesys-style tables like this:

| Conversation ID | Session ID | Date       | Utterance             | Prompt                                  | Ask Action Number | Ask Action Name | Ask Action Type | Ask Action Outcome | Intent      |
|-----------------|------------|------------|-----------------------|-----------------------------------------|-------------------|-----------------|-----------------|--------------------|-------------|
| id_1            | s1         | 2024-01-01 | I want to pay my bill | Please let me know your account number  | 1                 | AskAccount      | Slot            | Success            | BillPayment |
| id_1            | s1         | 2024-01-01 | 123456                | What amount would you like to pay?      | 2                 | AskAmount       | Slot            | Success            | BillPayment |

The following columns are intentionally ignored:

- `Ask Action Number`
- `Ask Action Name`
- `Ask Action Type`
- `Ask Action Outcome`

The tool uses:

- `Conversation ID` as the conversation ID
- `Utterance` as the `customer` transcript
- `Prompt` as the `agent` transcript

---

## How to Export / Get Data from Genesys

To prepare data for this tool, export conversation data from the bot or flow you want to analyze in Genesys Cloud.

### 1. Open the Bot or Flow

1. Log in to **Genesys Cloud**.
2. Go to the bot or digital flow you want data from.
3. Open the related **Optimization Dashboard**.

### 2. Export Conversation Data

From the Optimization Dashboard:

1. Locate the conversation/session data.
2. Export the data as a CSV file.
3. Save the exported file locally.

Depending on the export, your file may include columns such as:

| Conversation ID | Session ID | Date       | Utterance             | Prompt                                  | Ask Action Number | Ask Action Name | Ask Action Type | Ask Action Outcome | Intent      |
|-----------------|------------|------------|-----------------------|-----------------------------------------|-------------------|-----------------|-----------------|--------------------|-------------|
| id_1            | s1         | 2024-01-01 | I want to pay my bill | Please let me know your account number  | 1                 | AskAccount      | Slot            | Success            | BillPayment |
| id_1            | s1         | 2024-01-01 | 123456                | What amount would you like to pay?      | 2                 | AskAmount       | Slot            | Success            | BillPayment |

### 3. Load the Export into This Tool

You can either:

- Upload the exported CSV/TXT file
- Or paste the exported table or utterances directly into the text area

The tool reads the useful conversation fields and ignores export-only metadata.

| Export Field     | Used As                       |
|-----------------|-------------------------------|
| Conversation ID | Conversation `id`             |
| Utterance       | `customer` transcript         |
| Prompt          | `agent` transcript            |

The following fields are ignored:

- `Ask Action Number`
- `Ask Action Name`
- `Ask Action Type`
- `Ask Action Outcome`

### 4. Preview and Generate JSON

After loading the data:

1. Click **Preview** to verify the JSON.
2. Review the conversation count.
3. Review warnings, if any.
4. Click **Generate JSON**.
5. Upload the generated JSON file into **Genesys Intent Miner**.

---

## Genesys Intent Miner JSON Template

Genesys provides an example JSON file in Intent Miner that can be used as a recommended template for formatting conversation data.

The expected structure is:

- A top-level `locale`
- A top-level `conversations` array
- Each conversation has:
  - `id`
  - `turns`
- Each turn has:
  - `participant`
  - `transcript`

Example format:

```json
{
  "locale": "en-us",
  "conversations": [
    {
      "id": "id_1",
      "turns": [
        {
          "participant": "customer",
          "transcript": "set up a payment for my electricity bill"
        },
        {
          "participant": "agent",
          "transcript": "Please let me know the last 4 digits of your card number"
        },
        {
          "participant": "customer",
          "transcript": "7894"
        },
        {
          "participant": "agent",
          "transcript": "Did you mean that your last 4 digits of your card is 7894?"
        }
      ]
    }
  ]
}
```

This tool generates JSON in this same structure, using:

- `customer` for user utterances
- `agent` for prompts or bot/agent responses
- `transcript` for the text of each turn
- `id` for each conversation identifier

---

## Output Format

The generated JSON is compatible with the Intent Miner conversation format:

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

For multi-turn data, the tool outputs customer and agent turns in order:

```json
{
  "locale": "en-us",
  "conversations": [
    {
      "id": "id_1",
      "turns": [
        {
          "participant": "customer",
          "transcript": "I want to pay my bill"
        },
        {
          "participant": "agent",
          "transcript": "Please let me know your account number"
        },
        {
          "participant": "customer",
          "transcript": "123456"
        },
        {
          "participant": "agent",
          "transcript": "What amount would you like to pay?"
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

- Transcript exceeded 500 characters and was trimmed
- Conversation ID exceeded 100 characters and was truncated
- Conversation count exceeded the recommended file limit

This helps you quickly identify and troubleshoot problematic rows in your dataset.

---

## How to Use

1. Go to Genesys Cloud and export your data:
   - Open the bot or flow you want data from
   - Go to the Optimization Dashboard
   - Export the conversation/session data

2. Download the HTML file for this tool.

3. Open the HTML file in any modern web browser:
   - Chrome
   - Edge
   - Firefox
   - Safari

4. Load your data:
   - Upload a TXT/CSV file
   - Or paste utterances/table data into the text area

5. Review:
   - Conversation count
   - Warning count

6. Click **View Warnings** to inspect any issues.

7. Click **Preview** to review JSON output.

8. Click **Generate JSON**.

9. Upload the generated JSON file into Genesys Intent Miner.

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

- No Genesys API required because this is a formatting tool
- Works entirely on your local machine
- No data is uploaded to external services
- Works with most Genesys export formats
- If your CSV is not recognized, check column names
- Warnings do not block generation — they are informational
- The generated output should be reviewed before uploading to Intent Miner

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