def calculate_match_score(student_profile, internship_post):
    """
    Calculates a simple match score based on shared skills.
    This can be replaced with a more advanced algorithm later.
    """
    student_skills = {skill.strip().lower() for skill in student_profile.skills.split(',')}
    required_skills = {skill.strip().lower() for skill in internship_post.required_skills.split(',')}
    
    common_skills = student_skills.intersection(required_skills)
    
    if not required_skills:
        return 0.0
        
    score = len(common_skills) / len(required_skills)
    return round(score, 2)