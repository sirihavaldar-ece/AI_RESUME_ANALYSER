"""Turn missing role skills into a simple weekly learning plan."""


def make_roadmap(missing_skills: list[str]) -> list[str]:
    if not missing_skills:
        return ["Review the role requirements and build a small project that demonstrates your current skills."]
    return [f"Week {number}: Learn {skill} and practise it in a small project." for number, skill in enumerate(missing_skills, start=1)]
