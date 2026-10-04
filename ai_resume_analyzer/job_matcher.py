"""Compare detected resume skills with the skills listed for each role."""


def rank_roles(resume_skills: list[str], roles: list[dict[str, str]]) -> list[dict]:
    """Rank roles by the percentage of their required skills found."""
    resume_set = {skill.lower() for skill in resume_skills}
    results = []
    for role in roles:
        required = [skill.strip() for skill in role["required_skills"].split("|") if skill.strip()]
        matched = [skill for skill in required if skill.lower() in resume_set]
        missing = [skill for skill in required if skill.lower() not in resume_set]
        score = round(100 * len(matched) / len(required)) if required else 0
        results.append({**role, "score": score, "matched": matched, "missing": missing})
    return sorted(results, key=lambda result: (-result["score"], result["role"]))
