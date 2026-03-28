from graph_groups import create_group, list_groups

print("=== Testing Group Functions ===")

# Create a static group
create_group(
    "SG-Test-Static",
    "Static test group"
)

# Create a dynamic group
create_group(
    "SG-Test-Dynamic",
    "Dynamic test group",
    '(user.department -eq "Engineering")'
)

# List groups
print("\n=== All Groups ===")
list_groups()
