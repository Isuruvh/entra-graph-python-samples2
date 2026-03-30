# 🚀 Unified Entry Point: `main.py`

The `main.py` script is the **central command hub** for the Microsoft Graph IAM Automation Toolkit.  
Instead of running individual Python modules, you can launch **all IAM operations** from a single, interactive, menu‑driven CLI.

This unified entry point makes the toolkit ideal for:

- Demonstrations  
- Recruiter walkthroughs  
- Real‑world IAM automation workflows  
- Modular extension and future growth  

---

# ✅ Features

- Clean, menu‑driven command‑line interface  
- Centralized error handling  
- Calls all IAM modules (users, groups, licenses, roles, etc.)  
- Easy to extend with new IAM functions  
- Config‑driven architecture (via `config.json`)  
- Full audit logging (via `logger.py`)  
- Perfect for portfolio projects and real enterprise automation  

---

# ▶️ How to Run

```bash
python main.py
```

The menu will appear and guide you through all available IAM operations.

---

# 📋 Available Operations

Below is the current set of operations exposed through the unified CLI.

| Option | Operation |
|--------|-----------|
| 1 | Create User |
| 2 | Get User |
| 3 | List Users |
| 4 | Update User |
| 5 | Disable User |
| 6 | Delete User |
| 7 | Create Group |
| 8 | List Groups |
| 9 | Add User to Group |
| 10 | Remove User from Group |
| 11 | Delete Group |
| 12 | List License SKUs |
| 13 | Get User Licenses |
| 14 | Assign License to User |
| 15 | Remove License from User |
| 16 | List Directory Roles |
| 17 | Get Role Members |
| 18 | Assign Role to User |
| 19 | Remove Role from User |
| 20 | User Creation Wizard (guided onboarding) |
| 0 | Exit |

---

# 📁 Folder Structure Diagram

```
iam-automation/
│
├── main.py
├── config.py
├── config.json
├── logger.py
├── utils.py
│
├── graph_auth.py
├── graph_users.py
├── graph_groups.py
├── graph_licenses.py
├── graph_roles.py
│
├── user_wizard.py
│
├── requirements.txt
└── README.md
```

This structure reflects a **modular, enterprise‑grade IAM automation platform**, with clear separation of concerns and clean extensibility.

---

If you want, I can also generate:

- A **full README.md** (complete file)  
- A **badges section** (Python version, license, etc.)  
- A **“Getting Started”** section  
- A **“Roadmap”** section  
- A **“Screenshots / Demo GIF”** section  
- A **“Why This Project Matters”** section for recruiters  

Just tell me and I’ll craft it.
