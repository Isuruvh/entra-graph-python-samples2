# 📘 IAM Automation Platform — Architecture Overview

The IAM Automation Platform is a modular, event‑driven system that integrates:

- Workday (HR events)
- SCIM provisioning
- Microsoft Graph (identity + M365)
- Azure Resource Manager (ARM)
- FastAPI backend
- Streamlit Web UI
- Entra ID authentication

The platform automates **Joiner–Mover–Leaver (JML)** lifecycle events and provides a secure, web‑based interface for identity operations.

---

# 🧠 High‑Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Streamlit Web UI                         │
│     (New Hire, Update, Termination, CSV Upload, Admin Tools) │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                       FastAPI Backend                        │
│  /hr/*   /scim/*   /graph/*   (REST API for all operations)  │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                     IAM Orchestrator                         │
│  - Workday event parsing                                      │
│  - SCIM provisioning                                           │
│  - Graph automation                                            │
│  - License + group assignment                                  │
│  - Termination workflows                                       │
└──────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┴────────────────────┐
         ▼                                           ▼
┌──────────────────────────┐            ┌──────────────────────────┐
│     Microsoft Graph      │            │ Azure Resource Manager   │
│ Identity + M365 Control  │            │ Azure Infrastructure API │
│ Users, Groups, Roles     │            │ VMs, Storage, VNets      │
└──────────────────────────┘            └──────────────────────────┘
         │                                           │
         ▼                                           ▼
┌──────────────────────────┐            ┌──────────────────────────┐
│         SCIM API         │            │      Azure Resources     │
│ Workday → Entra ID Sync  │            │ (Optional automation)    │
└──────────────────────────┘            └──────────────────────────┘
```

---

# 🔐 Authentication & Authorization

The platform uses **Entra ID** for:

- User login (OIDC)
- MFA
- Conditional Access
- Token issuance (Graph + ARM)
- Role‑based access control (RBAC)

### **Token Types**

| Token Type | Used For | API |
|------------|----------|------|
| **Graph Token** | Identity + M365 | `graph.microsoft.com` |
| **ARM Token** | Azure resources | `management.azure.com` |

---

# 🔄 Lifecycle Automation (JML)

The IAM Orchestrator handles:

- **Joiner** → SCIM create → Graph sync → license + group assignment  
- **Mover** → attribute updates → group/role re‑evaluation  
- **Leaver** → disable → license removal → group cleanup  

---

# 🧩 Technology Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| Backend | FastAPI |
| Identity | Entra ID (OIDC) |
| Provisioning | SCIM 2.0 |
| Directory | Microsoft Graph |
| Infra | Azure ARM |
| Auth Library | MSAL |
| Language | Python |

---

# 🚀 Key Features

- Automated provisioning (Workday → SCIM → Entra ID)
- Graph‑based identity automation
- Azure ARM integration (optional)
- Secure login with Entra ID
- CSV bulk provisioning
- Admin tools for identity operations
- Modular, extensible architecture

---

# 🧩 JML Lifecycle Flow

## **JOINER (New Hire)**

1. Workday Event: *Hire* or *Pre‑Hire*  
2. Workday sends SCIM → Entra ID (user created in provisioning state)  
3. IAM Orchestrator receives event via `/hr/new-hire`  
4. Orchestrator performs:  
   - SCIM Create (if needed)  
   - Graph user creation (if SCIM not authoritative)  
   - Attribute population (title, department, manager)  
   - Group assignment (dynamic + static)  
   - License assignment (M365, Teams, SharePoint, Intune)  
   - Role assignment  
5. Notifications / logging  
6. User becomes Active in Entra ID  
7. User signs in (MFA + Conditional Access)  

---

## **MOVER (Update)**

1. Workday Event: *Job Change*, *Department Change*, *Manager Change*  
2. Workday sends SCIM → Entra ID (user updated)  
3. IAM Orchestrator receives event via `/hr/update`  
4. Orchestrator performs:  
   - Attribute updates  
   - Group re‑evaluation  
   - License re‑evaluation  
   - Role re‑evaluation  
   - Manager‑based access updates  
5. Notifications / logging  
6. User continues with updated access  

---

## **LEAVER (Termination)**

1. Workday Event: *Termination* or *End Employment*  
2. Workday sends SCIM → Entra ID (user disabled in provisioning)  
3. IAM Orchestrator receives event via `/hr/termination`  
4. Orchestrator performs:  
   - Disable account in Entra ID  
   - Remove all licenses  
   - Remove all group memberships  
   - Remove all roles  
   - Reset password / block sign‑in  
   - Archive mailbox / OneDrive (optional)  
   - Notify manager / HR (optional)  
5. Notifications / logging  
6. User becomes Disabled / Deleted (based on retention policy)  

---

# 🧩 Supporting Systems

- Streamlit Web UI (manual overrides, admin tools)  
- FastAPI Backend (API gateway)  
- IAM Orchestrator (business logic)  
- Microsoft Graph (identity + M365)  
- SCIM (Workday → Entra ID provisioning)  
- Azure ARM (optional infra automation)  
- Entra ID (authentication, MFA, CA)  

---

# 🔐 Token Flow Architecture

## **USER → STREAMLIT UI LOGIN**

1. User opens Streamlit UI  
2. Streamlit redirects to Entra ID (OIDC Authorization Code Flow)  
3. User completes:  
   - Password  
   - MFA  
   - Conditional Access  
4. Entra ID returns:  
   - **ID Token**  
   - **Authorization Code**  
5. Streamlit exchanges code for:  
   - ID Token  
   - Access Token (optional)  
   - Refresh Token (optional)  

---

## **STREAMLIT → FASTAPI BACKEND**

6. Streamlit sends API requests to FastAPI  
7. FastAPI validates the token  
8. FastAPI does **not** use the user’s token for automation  
   - It uses its **own service principal**  

---

## **FASTAPI → ENTRA ID (MSAL)**

9. FastAPI requests:

### **A. Graph Access Token**  
Scope: `https://graph.microsoft.com/.default`

### **B. ARM Access Token**  
Scope: `https://management.azure.com/.default`

10. Entra ID returns:  
- Access Token (Graph)  
- Access Token (ARM)  
- Refresh Token (service principal)  

---

## **IAM ORCHESTRATOR → GRAPH / ARM / SCIM**

### **Graph Token used for:**  
- Create / update / disable user  
- Assign licenses  
- Assign groups  
- Assign roles  

### **ARM Token used for:**  
- Azure resource automation  
- RBAC assignments  
- Key Vault operations  
- Storage operations  

### **SCIM used for:**  
- Workday → Entra ID provisioning  

---

# 🔑 Token Types Summary

### **ID Token**
- Used by Streamlit UI  
- Identifies the logged‑in user  

### **Access Token (Graph)**
- Used by backend to call Microsoft Graph  

### **Access Token (ARM)**
- Used by backend to call Azure Resource Manager  

### **Refresh Token**
- Used by backend service principal to silently renew tokens  

---
