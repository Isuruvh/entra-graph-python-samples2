# 📘 **README Section: Unified Main Script**

## 🚀 Unified Entry Point: `main.py`

The `main.py` script serves as the **central command hub** for the Microsoft Graph IAM Automation Toolkit.  
Instead of running individual Python modules, you can launch all IAM operations from a single interactive menu.

### ✅ Features

- Clean, menu‑driven CLI  
- Centralized error handling  
- Calls all IAM modules (export, update, delete, group operations, etc.)  
- Easy to extend with new IAM functions  
- Perfect for demos, recruiters, and real‑world automation workflows  

### ▶️ How to Run

```bash
python main.py
```

### 📋 Available Operations

| Option | Operation |
|--------|-----------|
| 1 | Export all Groups |
| 2 | Export Group Membership |
| 3 | Export User Access |
| 4 | Add User to Group |
| 5 | List Group Members |
| 6 | Remove User from Group |
| 7 | Delete User |
| 8 | Disable User |
| 9 | Force User Sign‑Out |
| 10 | Update User Display Name |
| 0 | Exit |

---

# 📁 **Folder Structure Diagram**

```
iam-automation/
│
├── main.py
├── config.py
│
├── export_groups.py
├── export_group_membership.py
├── export_user_access.py
│
├── add_to_group.py
├── list_group_members.py
├── remove_from_group.py
│
├── delete_user.py
├── disable_user.py
├── force_signout.py
├── update_user.py
│
├── requirements.txt
└── README.md
```

