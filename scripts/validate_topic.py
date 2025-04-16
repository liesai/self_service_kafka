import re
import os
import sys

MAX_PARTITIONS = 12
MAX_RETENTION_DAYS = 7
ALLOWED_PREFIXES = ['team1.', 'team2.']
MAX_TOPICS_PER_TEAM = {
    'team1': 5,
    'team2': 10
}

def parse_topic_from_tf():
    topics = []
    path = "topics/"
    for file in os.listdir(path):
        if file.endswith(".tf"):
            with open(os.path.join(path, file)) as f:
                content = f.read()
                match = re.search(r'topic_name\s+=\s+"([^"]+)"', content)
                if match:
                    topics.append(match.group(1))
    return topics

def validate_topic_name(name):
    return re.match(r'^[a-z0-9]+\.[a-z0-9]+\.[a-z0-9]+\.(dev|qa|prod)$', name) is not None

def validate_prefix(name):
    return any(name.startswith(p) for p in ALLOWED_PREFIXES)

def main():
    topics = parse_topic_from_tf()
    errors = []

    for topic in topics:
        if not validate_topic_name(topic):
            errors.append(f"❌ Topic '{topic}' does not match naming convention.")
        if not validate_prefix(topic):
            errors.append(f"❌ Topic '{topic}' does not start with an allowed prefix.")

        team_prefix = topic.split('.')[0]
        team_limit = MAX_TOPICS_PER_TEAM.get(team_prefix, 0)
        team_topics = [t for t in topics if t.startswith(team_prefix + '.')]
        if len(team_topics) > team_limit:
            errors.append(f"❌ Team '{team_prefix}' exceeds topic quota ({len(team_topics)}/{team_limit})")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)
    else:
        print("✅ All validations passed.")

if __name__ == "__main__":
    main()
