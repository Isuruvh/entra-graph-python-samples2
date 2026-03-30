# 🚀 Microsoft Graph IAM Automation Toolkit  
### **Now with Full Workday → Entra → SCIM Provisioning Pipeline**

This project is a **modular, enterprise‑grade Identity Automation Platform** built in Python.  
It integrates:

- **Microsoft Graph API**  
- **Local SCIM 2.0 Server (FastAPI)**  
- **Workday‑style HR feed simulation**  
- **User lifecycle automation**  
- **Group, license, and role management**  
- **End‑to‑end provisioning demo script**

It is designed to mirror real‑world identity engineering workflows used in:

- Workday → Entra ID → SaaS provisioning  
- HR‑driven lifecycle automation  
- SCIM‑based SaaS integrations  
- Enterprise IAM engineering roles  

This is a complete, portfolio‑ready IAM automation platform.

---

# 📌 Features Overview

### 🔐 **Entra ID Automation**
- Create, update, disable, and delete users  
- Assign/remove group membership  
- Assign/remove licenses  
- Assign/remove directory roles  
- Export users, groups, and access reports  

### 🧩 **SCIM 2.0 Integration**
- Local FastAPI SCIM server  
- SCIM `/Users` endpoint  
- Create, update, deactivate SCIM users  
- Identity mapping (Entra → SCIM)  
- SCIM client module with logging  

### 🏢 **Workday‑Style HR Feed Processing**
- New Hire → Entra → SCIM provisioning  
- Job Change → Entra update + SCIM PATCH  
- Termination → Disable Entra user + deactivate SCIM user  
- HR event detection engine  

### 🎛️ **Unified CLI (main.py)**
- Menu‑driven IAM operations  
- Centralized error handling  
- Easy to extend with new modules  
- Perfect for demos and interviews  

### 🎬 **End‑to‑End Demo Script**
Run the entire Workday → Entra → SCIM pipeline with:

```bash
python run_demo.py
```

---

# ▶️ How to Run

### 1. Start the SCIM Server

```bash
uvicorn scim.scim_server:app --reload --port 8000
```

### 2. Run the IAM Toolkit

```bash
python main.py
```

### 3. Run the Full Workday → Entra → SCIM Demo

```bash
python run_demo.py
```

---

# 📋 Unified CLI Operations

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
| 14 | Assign License |
| 15 | Remove License |
| 16 | List Directory Roles |
| 17 | Get Role Members |
| 18 | Assign Role |
| 19 | Remove Role |
| 20 | User Creation Wizard |
| 30 | Process Workday HR Feed (SCIM Provisioning) |
| 0 | Exit |

---

# 🧱 SCIM Architecture

### **SCIM Server (FastAPI)**
Implements:

- `POST /Users`  
- `GET /Users`  
- `PATCH /Users/{id}`  
- `DELETE /Users/{id}`  

Stores users in a local JSON datastore.

### **SCIM Client**
Handles:

- Create SCIM user  
- Update SCIM user  
- Deactivate SCIM user  
- Logging + error handling  

### **Identity Mapping**
Tracks:

- Workday employeeId → Entra user ID  
- Entra user ID → SCIM user ID  

---

# 🏢 Workday → Entra → SCIM Provisioning Pipeline

### **New Hire**
1. Create user in Entra  
2. Assign groups, licenses, roles  
3. Provision user into SCIM  
4. Store identity mapping  
5. Log event  

### **Update**
1. Detect changed attributes  
2. Update Entra user  
3. PATCH SCIM user  
4. Log event  

### **Termination**
1. Disable Entra user  
2. Deactivate SCIM user  
3. Log event  

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