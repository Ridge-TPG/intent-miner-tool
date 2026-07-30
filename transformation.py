import json
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

MAX_CONVERSATIONS = 30000
WARNING_THRESHOLD = 25000


# ----------------------------
# Data Transformation
# ----------------------------

def transform_simple(utterances):
    conversations = []

    for i, utt in enumerate(utterances):
        utt = utt.strip()
        if not utt:
            continue

        conversations.append({
            "id": f"id_{i+1}",
            "turns": [
                {
                    "participant": "customer",
                    "transcript": utt
                }
            ]
        })

    return conversations


def transform_csv(file_path):
    conversations = {}

    with open(file_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        if not reader.fieldnames:
            return []

        def get_value(row, possible_names):
            for name in possible_names:
                for key in row:
                    if key.lower().strip() == name:
                        return row[key]
            return ""

        for row in reader:
            conv_id = get_value(row, ["conversation_id", "conversation id", "id"])
            participant = get_value(row, ["participant", "participant purpose", "role"])
            transcript = get_value(row, ["transcript", "utterance", "text", "message", "body", "segment text"])

            if not conv_id:
                conv_id = f"id_{len(conversations)+1}"

            if not participant:
                participant = "customer"

            if not transcript or not transcript.strip():
                continue

            if conv_id not in conversations:
                conversations[conv_id] = []

            conversations[conv_id].append({
                "participant": participant.lower(),
                "transcript": transcript.strip()
            })

    return [
        {"id": cid, "turns": turns}
        for cid, turns in conversations.items()
    ]


def build_conversations():
    if hasattr(root, "file_path") and root.file_path:
        return transform_csv(root.file_path)
    else:
        raw_text = text_box.get("1.0", tk.END)
        utterances = raw_text.splitlines()
        return transform_simple(utterances)


# ----------------------------
# Counter Logic
# ----------------------------

def update_counter(event=None):
    try:
        if hasattr(root, "file_path") and root.file_path:
            conversations = transform_csv(root.file_path)
            count = len(conversations)
        else:
            raw_text = text_box.get("1.0", tk.END)
            utterances = [u for u in raw_text.splitlines() if u.strip()]
            count = len(utterances)

        counter_label.config(text=f"Conversations: {count}")

        if count > MAX_CONVERSATIONS:
            counter_label.config(fg="red")
        elif count > WARNING_THRESHOLD:
            counter_label.config(fg="orange")
        else:
            counter_label.config(fg="green")

    except:
        counter_label.config(text="Conversations: ?", fg="black")


# ----------------------------
# File Saving
# ----------------------------

def save_single(conversations):
    output = {
        "locale": "en-us",
        "conversations": conversations
    }

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")]
    )

    if not file_path:
        return

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    messagebox.showinfo("Success", "JSON file created!")


def save_split(conversations):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")]
    )

    if not file_path:
        return

    base_name = file_path.replace(".json", "")

    chunks = [
        conversations[i:i + MAX_CONVERSATIONS]
        for i in range(0, len(conversations), MAX_CONVERSATIONS)
    ]

    for idx, chunk in enumerate(chunks):
        output = {
            "locale": "en-us",
            "conversations": chunk
        }

        chunk_file = f"{base_name}_part{idx+1}.json"

        with open(chunk_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

    messagebox.showinfo(
        "Success",
        f"Created {len(chunks)} files due to 30k limit."
    )


# ----------------------------
# UI Actions
# ----------------------------

def load_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text or CSV files", "*.txt *.csv")]
    )
    if not file_path:
        return

    file_label.config(text=f"Loaded: {file_path.split('/')[-1]}", fg="black")

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, f.read())
        root.file_path = None

    else:
        root.file_path = file_path
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, "[CSV loaded — using structured data]")

    update_counter()


def generate_json():
    try:
        conversations = build_conversations()

        if not conversations:
            messagebox.showwarning("Warning", "No data found")
            return

        count = len(conversations)

        if count > MAX_CONVERSATIONS:
            choice = messagebox.askyesno(
                "Limit Exceeded",
                f"{count} conversations detected.\n\n"
                f"Genesys limit is {MAX_CONVERSATIONS}.\n\n"
                f"Do you want to split into multiple files?"
            )

            if choice:
                save_split(conversations)
            return

        save_single(conversations)

    except Exception as e:
        messagebox.showerror("Error", str(e))
        
        import json
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

MAX_CONVERSATIONS = 30000
WARNING_THRESHOLD = 25000
MAX_TRANSCRIPT_LENGTH = 500


# ----------------------------
# Helpers
# ----------------------------

def trim_transcript(text):
    return text[:MAX_TRANSCRIPT_LENGTH]


def preview_json():
    try:
        conversations = build_conversations()

        if not conversations:
            messagebox.showwarning("Warning", "No data to preview")
            return

        # Apply same validation as generate (important!)
        long_count = validate_transcripts(conversations)
        if long_count > 0:
            trim_all_transcripts(conversations)

        output = {
            "locale": "en-us",
            "conversations": conversations
        }

        # Create preview window
        preview_win = tk.Toplevel(root)
        preview_win.title("JSON Preview")
        preview_win.geometry("700x500")

        text = tk.Text(preview_win, wrap=tk.NONE, font=("Consolas", 10))
        text.pack(fill=tk.BOTH, expand=True)

        # Add scrollbars
        y_scroll = tk.Scrollbar(preview_win, orient="vertical", command=text.yview)
        y_scroll.pack(side="right", fill="y")
        text.config(yscrollcommand=y_scroll.set)

        x_scroll = tk.Scrollbar(preview_win, orient="horizontal", command=text.xview)
        x_scroll.pack(side="bottom", fill="x")
        text.config(xscrollcommand=x_scroll.set)

        formatted_json = json.dumps(output, indent=2)
        text.insert(tk.END, formatted_json)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ----------------------------
# Data Transformation
# ----------------------------

def transform_simple(utterances):
    conversations = []

    for i, utt in enumerate(utterances):
        utt = utt.strip()
        if not utt:
            continue

        conversations.append({
            "id": f"id_{i+1}",
            "turns": [
                {
                    "participant": "customer",
                    "transcript": utt
                }
            ]
        })

    return conversations


def transform_csv(file_path):
    conversations = {}

    with open(file_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        if not reader.fieldnames:
            return []

        def get_value(row, possible_names):
            for name in possible_names:
                for key in row:
                    if key.lower().strip() == name:
                        return row[key]
            return ""

        for row in reader:
            conv_id = get_value(row, ["conversation_id", "conversation id", "id"])
            participant = get_value(row, ["participant", "participant purpose", "role"])
            transcript = get_value(row, ["transcript", "utterance", "text", "message", "body", "segment text"])

            if not conv_id:
                conv_id = f"id_{len(conversations)+1}"

            if not participant:
                participant = "customer"

            if not transcript or not transcript.strip():
                continue

            if conv_id not in conversations:
                conversations[conv_id] = []

            conversations[conv_id].append({
                "participant": participant.lower(),
                "transcript": transcript.strip()
            })

    return [
        {"id": cid, "turns": turns}
        for cid, turns in conversations.items()
    ]


def build_conversations():
    if hasattr(root, "file_path") and root.file_path:
        return transform_csv(root.file_path)
    else:
        raw_text = text_box.get("1.0", tk.END)
        utterances = raw_text.splitlines()
        return transform_simple(utterances)


# ----------------------------
# Validation
# ----------------------------

def validate_transcripts(conversations):
    long_count = 0

    for conv in conversations:
        for turn in conv["turns"]:
            if len(turn["transcript"]) > MAX_TRANSCRIPT_LENGTH:
                long_count += 1

    return long_count


def trim_all_transcripts(conversations):
    for conv in conversations:
        for turn in conv["turns"]:
            if len(turn["transcript"]) > MAX_TRANSCRIPT_LENGTH:
                turn["transcript"] = trim_transcript(turn["transcript"])


# ----------------------------
# Counter
# ----------------------------

def update_counter(event=None):
    try:
        if hasattr(root, "file_path") and root.file_path:
            conversations = transform_csv(root.file_path)
            count = len(conversations)
        else:
            raw_text = text_box.get("1.0", tk.END)
            utterances = [u for u in raw_text.splitlines() if u.strip()]
            count = len(utterances)

        counter_label.config(text=f"Conversations: {count}")
        
        warning_label.config(text="")

        if count > MAX_CONVERSATIONS:
            counter_label.config(fg="red")
            warning_label.config(text="Too many conversations (will split)")
        elif count > WARNING_THRESHOLD:
            counter_label.config(fg="orange")
            warning_label.config(text="Approaching limit")
        else:
            counter_label.config(fg="green")
    except:
        counter_label.config(text="Conversations: ?", fg="black")


# ----------------------------
# Saving
# ----------------------------

def save_single(conversations):
    output = {
        "locale": "en-us",
        "conversations": conversations
    }

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")]
    )

    if not file_path:
        return

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    messagebox.showinfo("Success", "JSON file created!")


def save_split(conversations):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")]
    )

    if not file_path:
        return

    base_name = file_path.replace(".json", "")

    chunks = [
        conversations[i:i + MAX_CONVERSATIONS]
        for i in range(0, len(conversations), MAX_CONVERSATIONS)
    ]

    for idx, chunk in enumerate(chunks):
        output = {
            "locale": "en-us",
            "conversations": chunk
        }

        chunk_file = f"{base_name}_part{idx+1}.json"

        with open(chunk_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

    messagebox.showinfo(
        "Success",
        f"Created {len(chunks)} files due to 30k limit."
    )


# ----------------------------
# Main Action
# ----------------------------

def generate_json():
    try:
        conversations = build_conversations()

        if not conversations:
            messagebox.showwarning("Warning", "No data found")
            return

        # transcript length validation
        long_count = validate_transcripts(conversations)

        if long_count > 0:
            choice = messagebox.askyesno(
                "Transcript Too Long",
                f"{long_count} transcripts exceed {MAX_TRANSCRIPT_LENGTH} characters.\n\n"
                f"Do you want to automatically trim them?"
            )

            if choice:
                trim_all_transcripts(conversations)
            else:
                return

        count = len(conversations)

        if count > MAX_CONVERSATIONS:
            choice = messagebox.askyesno(
                "Limit Exceeded",
                f"{count} conversations detected.\n\n"
                f"Genesys limit is {MAX_CONVERSATIONS}.\n\n"
                f"Do you want to split into multiple files?"
            )

            if choice:
                save_split(conversations)
            return

        save_single(conversations)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ----------------------------
# UI Layout (Improved)
# ----------------------------

root = tk.Tk()
root.title("Intent Miner JSON Generator")
root.geometry("750x600")
root.configure(bg="#f5f5f5")

# Header
header = tk.Label(root, text="Intent Miner JSON Generator", font=("Arial", 14, "bold"), bg="#f5f5f5")
header.pack(pady=10)

# Top buttons
top_frame = tk.Frame(root, bg="#f5f5f5")
top_frame.pack(pady=5)

load_btn = tk.Button(top_frame, text="Load TXT/CSV", width=15, command=load_file)
load_btn.grid(row=0, column=0, padx=5)

clear_btn = tk.Button(top_frame, text="Clear", width=10, command=lambda: text_box.delete("1.0", tk.END))
clear_btn.grid(row=0, column=1, padx=5)

# File info
file_label = tk.Label(root, text="No file loaded", fg="gray", bg="#f5f5f5")
file_label.pack()

# Text input box
text_box = tk.Text(root, wrap=tk.WORD, height=18, font=("Consolas", 10))
text_box.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

text_box.bind("<KeyRelease>", update_counter)

# Status panel
status_frame = tk.Frame(root, bg="#f5f5f5")
status_frame.pack(pady=5)

counter_label = tk.Label(status_frame, text="Conversations: 0", fg="green", bg="#f5f5f5")
counter_label.grid(row=0, column=0, padx=10)

warning_label = tk.Label(status_frame, text="", fg="orange", bg="#f5f5f5")
warning_label.grid(row=0, column=1, padx=10)

# Bottom buttons
btn_frame = tk.Frame(root, bg="#f5f5f5")
btn_frame.pack(pady=15)

preview_btn = tk.Button(btn_frame, text="Preview JSON", width=15, command=preview_json)
preview_btn.grid(row=0, column=0, padx=10)

gen_btn = tk.Button(btn_frame, text="Generate JSON", width=20, bg="#4CAF50", fg="white", command=generate_json)
gen_btn.grid(row=0, column=1, padx=10)

root.mainloop()