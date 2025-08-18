Perfect 👌 — I’ll draft a **detailed, recruiter-friendly README.md** that:

* Explains the project in **simple language** (so even non-tech people can get it).
* Highlights **business value** (time saved, consistency, automation).
* Documents **technical setup** (so anyone can reproduce it).
* Includes your note about Hugging Face vs OpenAI.

Here’s the full draft:

---

# 📩 AI Email Classifier & Auto-Responder

An **automation project** that reads unread emails from Gmail, classifies them into categories (Billing Issue, Technical Support, or General Query), and automatically replies with a **professional, pre-defined response** — all while keeping a log for reporting.

This project demonstrates how **AI + automation** can save time by handling repetitive email workflows, freeing teams to focus on high-value work.

---

## 🌟 Features

* **Fetch unread emails** from Gmail inbox (secure OAuth2 authentication).
* **AI-powered classification** of emails into categories:

  * Billing Issue
  * Technical Support
  * General Query
* **Automated replies** sent in the same Gmail thread.
* **Custom reply templates** for each category.
* **Audit logging**: every email and action is stored in a CSV file.
* **Safety checks**: skips auto-senders (`no-reply`, newsletters) to prevent loops.
* **Dry-run mode**: preview classifications before sending real replies.
* **Labeling**: replied emails are tagged `AUTO_REPLIED` in Gmail.

---

## 🎯 Why This Project Matters

Many businesses receive **hundreds of repetitive emails daily**. Sorting, categorizing, and responding manually takes hours.

This automation:

* Saves time ⏳ (no more manual sorting).
* Ensures consistency 📝 (everyone gets a professional reply).
* Provides visibility 📊 (logs and summary reports for managers).
* Reduces human error ❌ (no email gets forgotten).

Think of it as a **virtual assistant** for your Gmail inbox.

---

## 🛠️ Tech Stack

* **Python** (core scripting).
* **Hugging Face Transformers** → free AI model (`facebook/bart-large-mnli`) for classification.
* **Google Gmail API** → secure access to emails + sending replies.
* **Pandas** → log and analyze results.

> **Note:** This project currently uses Hugging Face’s free zero-shot model.
> In production, it can be easily swapped with **OpenAI GPT, Cohere, or Anthropic APIs** for even higher accuracy.

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/YOURUSERNAME/email-automation-bot.git
cd email-automation-bot
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

pip install -r requirements.txt
```

*(If `requirements.txt` not yet created, run `pip freeze > requirements.txt` after installing packages.)*

### 3. Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project → Enable **Gmail API**.
3. Create OAuth 2.0 credentials → Download `credentials.json`.
4. Place it inside the project folder.

### 4. First Run (Authorize Gmail)

When you run for the first time:

```bash
python main.py
```

It will open a browser → ask you to log in to Gmail → and create `token.json` for future runs.

---

## ▶️ Usage

### Dry Run (Safe Mode – No Emails Sent)

```bash
python main.py
```

* Fetches emails.
* Classifies them into categories.
* Shows what replies *would* be sent.
* Logs results into `logs/classified_emails.csv`.

### Real Run (Auto-Reply Mode)

In `main.py`, change:

```python
results = reply_flow(dry_run=True, max_results=10)
```

to

```python
results = reply_flow(dry_run=False, max_results=10)
```

Now replies are actually sent! ✅

---

## 📊 Example Output

**Console Summary:**

```
=== Volume by Category ===
Billing Issue    3
Technical Support 1
SKIPPED          2

=== Volume by Day ===
2025-08-18    6
```

**Log File (CSV):**

| ts                | from                                | subject        | category      | replied |
| ----------------- | ----------------------------------- | -------------- | ------------- | ------- |
| 2025-08-18 12:30Z | [user@abc.com](mailto:user@abc.com) | Payment Failed | Billing Issue | True    |
| 2025-08-18 12:32Z | no-reply\@xyz                       | Newsletter     | SKIPPED       | False   |

**Gmail Inbox:**

* Emails replied with templates.
* Labeled `AUTO_REPLIED`.
* Marked as read.

---

## 📌 Safety Features

* **Dry run mode**: prevents accidental mass replies.
* **Blocklist**: ignores senders like `no-reply`, `mailer-daemon`.
* **Labels**: replied emails are tagged for easy tracking.
* **Audit log**: CSV file stores history of every action.

---

## 🚀 Future Improvements

* Add more categories (e.g., Sales Query, Feedback, Spam).
* Integrate with Slack/CRM for team notifications.
* Use OpenAI GPT for smarter, context-aware replies.
* Build a dashboard to visualize email volumes and trends.

---

## 👨‍💻 Author

* **Keshav Singh Rajpoot**
* Project built as part of learning **AI + workflow automation** for real-world use cases.

