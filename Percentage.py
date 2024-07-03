def skill_config(file):
    # content = file.read().decode("utf-8")
    # skills = [skill.strip() for skill in content.splitlines()]
    # return skills
    with open(file, 'r') as f:
        content = f.read()
        skills = [skill.strip() for skill in content.splitlines()]
        return skills


def matched_skills(text, skill_file):
    return [skill for skill in skill_file if skill.lower().strip() in text.lower().strip()]


def matching_skills(text, skill_file):
    total_skills = sum(1 for skill in skill_file if skill.lower().strip() in text.lower().strip())
    percentage = (total_skills / len(skill_file)) * 100
    return f"Skills found: {percentage:.2f}%"


