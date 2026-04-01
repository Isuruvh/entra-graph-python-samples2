# ⭐ **1️⃣ README.md Architecture Section**

Below is a polished, copy‑paste‑ready section for your GitHub README.  
It explains your IAM Automation Platform in a way that impresses recruiters, hiring managers, and senior engineers.

---

## 📘 **Architecture Overview**

The IAM Automation Platform is a modular, event‑driven system that integrates:

- **Workday (HR events)**
- **SCIM provisioning**
- **Microsoft Graph (identity + M365)**
- **Azure Resource Manager (ARM)**
- **FastAPI backend**
- **Streamlit Web UI**
- **Entra ID authentication**

The platform automates **Joiner–Mover–Leaver (JML)** lifecycle events and provides a secure, web‑based interface for identity operations.

---

## 🧠 **High‑Level Architecture**

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

## 🔐 **Authentication & Authorization**

The platform uses **Entra ID** for:

- User login (OIDC)
- MFA
- Conditional Access
- Token issuance (Graph + ARM)
- Role‑based access control (RBAC)

Two token types are used:

| Token Type | Used For | API |
|------------|----------|------|
| **Graph Token** | Identity + M365 | `graph.microsoft.com` |
| **ARM Token** | Azure resources | `management.azure.com` |

---

## 🔄 **Lifecycle Automation (JML)**

The orchestrator handles:

- **Joiner** → SCIM create → Graph sync → license + group assignment  
- **Mover** → attribute updates → group/role re‑evaluation  
- **Leaver** → disable → license removal → group cleanup  

---

## 🧩 **Technology Stack**

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

## 🚀 **Key Features**

- Automated provisioning (Workday → SCIM → Entra ID)
- Graph‑based identity automation
- Azure ARM integration (optional)
- Secure login with Entra ID
- CSV bulk provisioning
- Admin tools for identity operations
- Modular, extensible architecture

```mermaid
flowchart TB

A[Streamlit Web UI<br>(User Login, Forms, Admin Tools)]
B[Entra ID<br>(OIDC Login, MFA, Conditional Access)]
C[FastAPI Backend<br>/hr /scim /graph Endpoints]
D[IAM Orchestrator<br>Workday → SCIM → Graph<br>Licenses, Groups, Disable]
E[Microsoft Graph API<br>Identity + M365 Control Plane]
F[Azure Resource Manager (ARM)<br>Azure Infrastructure Control Plane]
G[SCIM Provisioning<br>Workday → Entra ID]
H[Azure Resources<br>VMs, Storage, VNets, Key Vault]

A -->|OIDC Login| B
A -->|REST Calls| C
C --> D

D -->|Graph Token| E
D -->|ARM Token| F
D -->|SCIM Calls| G

F --> H
```
