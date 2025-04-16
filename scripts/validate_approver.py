import yaml
import os
import sys

APPROVER_EMAIL = os.environ.get("APPROVER_EMAIL")
SUBSCRIPTION_FILE = "subscriptions/subscription_request.yaml"
TOPIC_CATALOG = "catalog/topics.yaml"

# Charger la demande d’abonnement
with open(SUBSCRIPTION_FILE) as f:
    request = yaml.safe_load(f)["subscription_request"]
    topic_name = request["topic"]

# Charger le catalogue de topics
with open(TOPIC_CATALOG) as f:
    topics = yaml.safe_load(f)["topics"]

# Recherche du topic concerné
matching = next((t for t in topics if t["name"] == topic_name), None)

if not matching:
    print(f"❌ Topic {topic_name} not found in catalog.")
    sys.exit(1)

approvers = matching.get("approvers", [])

if APPROVER_EMAIL in approvers:
    print(f"✅ {APPROVER_EMAIL} is authorized to approve.")
else:
    print(f"❌ {APPROVER_EMAIL} is not authorized to approve topic '{topic_name}'.")
    sys.exit(1)
