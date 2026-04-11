from typing import Any, Dict, List, Optional

INTENT_KEYWORDS = {
    "authentication": ["login", "auth", "signin", "signup", "token", "password"],
    "billing": ["payment", "checkout", "invoice", "billing", "charge", "subscription"],
    "performance": ["optimize", "performance", "latency", "speed"],
    "security": ["security", "vulnerability", "encrypt", "secure"],
    "ui": ["ui", "ux", "interface", "dashboard", "layout"],
    "api": ["api", "endpoint", "request", "response", "graphql"],
    "database": ["db", "database", "query", "migration", "schema"],
}


def _get_value(source: Any, key: str):
    if isinstance(source, dict):
        return source.get(key)
    return getattr(source, key, None)


def extract_intent(commit_message: Optional[str]) -> str:
    if not commit_message:
        return "general"
    normalized = commit_message.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized:
                return intent
    return "general"


def module_from_file(file_name: str) -> str:
    if "/" in file_name:
        return file_name.split("/")[0]
    if "\\" in file_name:
        return file_name.split("\\")[0]
    return file_name


def analyze_intent_collisions(activities: List[Dict]) -> List[Dict]:
    module_groups: Dict[str, Dict[str, List[str]]] = {}
    for activity in activities:
        file_name = _get_value(activity, "file_name")
        module = module_from_file(file_name if file_name else "root")
        intent = extract_intent(_get_value(activity, "commit_message"))
        developer_id = _get_value(activity, "developer_id")
        module_groups.setdefault(module, {}).setdefault(intent, []).append(developer_id)

    collisions = []
    for module, intents in module_groups.items():
        if len(intents) > 1:
            unique_developers = sorted({dev for devs in intents.values() for dev in devs if dev})
            collisions.append({
                "module": module,
                "developer_ids": unique_developers,
                "intents": sorted(intents.keys()),
                "overlap_type": "intent-collision",
                "severity": "MEDIUM",
                "reason_tags": ["same_module", "intent_collision"],
            })
    return collisions
