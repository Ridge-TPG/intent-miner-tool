# Intent Miner JSON Generator

A simple desktop tool to transform utterances or Genesys Cloud exports into the JSON format required for **Genesys Intent Miner**.

Built with Python + Tkinter. Designed for non-technical users.

---

## 🚀 Features

- Convert **plain text utterances** into Intent Miner format
- Support for **Genesys CSV exports**
- Handles **multi-turn conversations** (customer + agent)
- Live **conversation counter**
- Enforces Genesys limits:
  - Max **30,000 conversations**
  - Max **500 characters per transcript**
- Auto:
  - ✅ Split large datasets into multiple files
  - ✅ Trim long transcripts
- Built-in **JSON preview**
- Simple desktop UI (no install required if using `.exe`)

---

## 📂 Supported Inputs

### 1. Text Input
Paste utterances (one per line):

pay my bill  
check balance  
cancel subscription  

---

### 2. CSV Input (Genesys Export)

Supports flexible column names such as:

- Conversation ID:
  - `conversation_id`, `Conversation Id`, `id`
- Participant:
  - `participant`, `Participant Purpose`, `role`
- Text:
  - `transcript`, `utterance`, `text`, `message`, `body`, `segment text`

Example:

conversation_id,participant,transcript  
id_1,customer,I want to pay my bill  
id_1,agent,Sure, how would you like to pay?  

---

## 📦 Output Format

Generates JSON compatible with Genesys Intent Miner:

```
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

## ⚠️ Validation Rules (Genesys Limits)

This tool automatically handles:

- ✅ Max 30,000 conversations per file  
- ✅ Max 500 characters per transcript  

If limits are exceeded:
- You will be prompted to **auto-split files**
- Long transcripts will be **trimmed automatically**

---

## 🖥️ How to Use

1. Launch the app
2. Either:
   - Paste utterances  
   - OR click **Load TXT/CSV**
3. Review:
   - Conversation count
   - Warnings (if any)
4. (Optional) Click **Preview JSON**
5. Click **Generate JSON**
6. Upload output file(s) into Genesys Intent Miner

---

## ⚙️ Setup (Recommended)

It’s recommended to run this tool inside a virtual environment.

### 1. Create a virtual environment

```
python -m venv venv
```

### 2. Activate the virtual environment

**Windows:**
```
venv\Scripts\activate
```

**Mac/Linux:**
```
source venv/bin/activate
```

### 3. Install dependencies

A `requirements.txt` file is already included:

```
pip install -r requirements.txt
```

---

## ▶️ Run the App

```
python transformation.py
```

---

## 🏗️ Build EXE (for team distribution)

Install PyInstaller:

```
pip install pyinstaller
```

Build:

```
pyinstaller --onefile --windowed transformation.py
```

Output will be in:

```
dist/transformation.exe
```

---

## 🧠 Notes

- No Genesys API required (this is a formatting tool)
- Works with most Genesys export formats
- If your CSV is not recognized, check column names

---

## 🔧 Future Improvements

- Column mapping UI (for unknown CSV formats)
- Drag & drop file support
- Editable JSON preview
- Schema validation before export
- Conversation grouping by intent

---

## 👤 Users

Designed for:
- Conversation designers
- NLP / Intent training teams
- Genesys Cloud admins

---

## ✅ Summary

This tool removes manual work and prevents common upload errors when preparing data for Intent Miner.

---