from typing import Literal, get_args

Topic = Literal[
    "Simple literal math expression",
    "Simple Output",
    "String class methods",
    "Simple Boolean Logic",
    "Math class methods",
    "Simple variable expression",
    "Conditionals",
    "Simple output loop",
    "1D primitive array",
    "input concepts",
    "accumulation loop",
    "order of operations",
    "java specific data type concepts",
    "ArrayList",
]

TOPIC_LIST: list[str] = list(get_args(Topic))


ContestLevel = Literal["invA", "invB", "District", "Region", "State"]
CONTEST_LEVELS: list[str] = list(get_args(ContestLevel))


def normalize_topics() -> list[str]:
    f = lambda t: t.lower().replace(" ", "_")
    topic_normalized = map(f, TOPIC_LIST)
    return list(topic_normalized)