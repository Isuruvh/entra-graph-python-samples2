# 🚀 Microsoft Graph IAM Automation Toolkit  
### **Now with Full Workday → Entra → SCIM Provisioning Pipeline**

This project is a modular, enterprise‑grade **Identity Automation Platform** built in Python.  
It integrates:

- **Microsoft Graph API**  
- **Local SCIM 2.0 Server (FastAPI)**  
- **Workday‑style HR feed simulation**  
- **User lifecycle automation**  
- **Group, license, and role management**  
- **End‑to‑end provisioning demo script**

It mirrors real‑world identity engineering workflows used in:

- Workday → Entra ID → SaaS provisioning  
- HR‑driven lifecycle automation  
- SCIM‑based SaaS integrations  
- Enterprise IAM engineering roles  

---

# 📌 Features Overview

### 🔐 Entra ID Automation
- Create, update, disable, delete users  
- Assign/remove groups  
- Assign/remove licenses  
- Assign/remove directory roles  
- Export users, groups, and access reports  

### 🧩 SCIM 2.0 Integration
- Local FastAPI SCIM server  
- SCIM `/Users` endpoint  
- Create, update, deactivate SCIM users  
- Identity mapping (Entra → SCIM)  
- SCIM client with logging  

### 🏢 Workday‑Style HR Feed Processing
- New Hire → Entra → SCIM provisioning  
- Job Change → Entra update + SCIM PATCH  
- Termination → Disable Entra user + deactivate SCIM user  
- HR event detection engine  

### 🎛️ Unified CLI (main.py)
- Menu‑driven IAM operations  
- Centralized error handling  
- Easy to extend  
- Perfect for demos and interviews  

# 🧱 SCIM Architecture Diagram

```
                 ┌──────────────────────────┐
                 │      IAM Toolkit         │
                 │  (Python + Graph API)    │
                 └─────────────┬────────────┘
                               │
                               │ SCIM Client (POST/PATCH/DELETE)
                               ▼
                 ┌──────────────────────────┐
                 │     SCIM 2.0 Server      │
                 │     (FastAPI Local)      │
                 ├──────────────────────────┤
                 │  /Users                  │
                 │  /Users/{id}             │
                 │  JSON datastore          │
                 └─────────────┬────────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │   scim_storage.json      │
                 │   (Local SCIM DB)        │
                 └──────────────────────────┘
```

# 🏢 Workday → Entra → SCIM Pipeline Diagram

```
┌────────────────────┐
│   Workday Feed      │
│  (HR JSON/CSV)      │
└──────────┬──────────┘
           │
           ▼
┌────────────────────┐
│ Event Detection     │
│ NewHire / Update /  │
│ Termination         │
└──────────┬──────────┘
           │
           ▼
┌────────────────────┐
│  Entra Provisioning │
│  (Graph API)        │
│  - Create User      │
│  - Update User      │
│  - Disable User     │
│  - Groups/Licenses  │
└──────────┬──────────┘
           │
           ▼
┌────────────────────┐
│   SCIM Provisioning │
│   (Local FastAPI)   │
│   - POST /Users     │
│   - PATCH /Users    │
│   - Deactivate User │
└──────────┬──────────┘
           │
           ▼
┌────────────────────┐
│ Identity Mapping    │
│ entra → scim        │
└────────────────────┘
```

# 🧭 Roadmap

### ✅ Completed
- Entra user lifecycle automation  
- SCIM 2.0 server (FastAPI)  
- SCIM client  
- Identity mapping  
- Workday feed simulation  
- New Hire provisioning  
- Update flow (job change, department change)  
- Termination flow  
- End‑to‑end demo script  
- Unified CLI  

### 🔜 Coming Next
- SCIM `/Groups` endpoint  
- Group membership sync  
- SCIM filtering (`filter=userName eq "x"`)  
- SCIM pagination  
- Web dashboard (FastAPI + HTML)  
- Scheduler (cron‑style HR feed processing)  
- Replay mode for historical HR feeds  
- Multi‑tenant SCIM support  
- SaaS connector templates (Slack, Zoom, Atlassian)  

---

# 📁 Folder Structure

```
iam-automation/
│
├── main.py
├── run_demo.py
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
├── scim/
│   ├── scim_server.py
│   ├── scim_client.py
│   ├── scim_mapper.py
│   └── scim_storage.json
│
├── hr/
│   ├── workday_feed.py
│   ├── workday_events.py
│   ├── provision_new_hire.py
│   ├── provision_update.py
│   └── provision_termination.py
│
├── workday_feed.json
├── requirements.txt
└── README.md
```
