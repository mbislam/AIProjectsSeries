print("=" * 60)
print("Welcome to the AI Resume Builder!")
print("=" * 60)

name = input("Full name: ")
email = input("Email address: ")
phone = input("Phone number: ")
education = input("Education or grade level: ")
skills = input("Skills (comma separated): ")
project = input("Favorite project: ")
activities = input("Activities, clubs, or volunteer work: ")
career_goal = input("Career goal or interest: ")
opportunity = input("Opportunity you are applying for: ")

def student_resume():
    summary = (
        f"{name} is a motivated student interested in "
        f"{career_goal.lower()}. {name} enjoys learning, "
        f"building projects, and developing practical skills."
    )

    resume = f"""
============================================================
{name}
Email: {email}
Phone: {phone}
============================================================

STUDENT PROFILE
{summary}

EDUCATION
{education}

SKILLS
{skills}

PROJECT HIGHLIGHT
{project}

ACTIVITIES
{activities}

CAREER OBJECTIVE
To continue learning and gain experience in {career_goal}.
"""
    return resume

def skills_focused_resume():
    summary = (
        f"{name} is a skill-focused learner with interests in "
        f"{career_goal.lower()}. This resume highlights technical "
        f"skills, project experience, and learning motivation."
    )

    resume = f"""
============================================================
{name}
Email: {email}
Phone: {phone}
============================================================

SUMMARY
{summary}

TECHNICAL AND PERSONAL SKILLS
{skills}

KEY PROJECT
Project Title: {project}
Description: Developed a hands-on project that demonstrates
problem solving, creativity, and technology skills.

EDUCATION
{education}

ACTIVITIES AND LEADERSHIP
{activities}

TARGET OPPORTUNITY
{opportunity}
"""
    return resume

def creative_resume():
    summary = (
        f"Meet {name}, a creative technology learner who enjoys "
        f"using ideas, code, and problem solving to build meaningful "
        f"projects. {name}'s current goal is to explore {career_goal}."
    )

    resume = f"""
============================================================
{name}
Creative Technology Resume
Email: {email}
Phone: {phone}
============================================================

ABOUT ME
{summary}

WHAT I CAN DO
{skills}

PROJECT I AM PROUD OF
{project}

LEARNING BACKGROUND
{education}

BEYOND THE CLASSROOM
{activities}

MY NEXT GOAL
I am interested in {opportunity} because it connects with my
goal of learning more about {career_goal}.
"""
    return resume

def cover_letter():
    letter = f"""
Dear Selection Committee,

My name is {name}, and I am excited to apply for {opportunity}.
I am currently studying at or involved in {education}. I am
interested in {career_goal} and have been developing skills in
{skills}.

One project I am proud of is {project}. Through this project, I
practiced problem solving, creativity, and technical thinking. I
am also involved in {activities}, which has helped me grow as a
learner and team member.

Thank you for considering my application. I would be grateful for
the opportunity to continue learning and contributing.

Sincerely,
{name}
"""
    return letter

print("\nChoose a resume template:")
print("1. Student Resume")
print("2. Skills-Focused Resume")
print("3. Creative Technology Resume")

choice = input("Enter 1, 2, or 3: ")

if choice == "1":
    resume = student_resume()
    template_name = "student_resume"
elif choice == "2":
    resume = skills_focused_resume()
    template_name = "skills_focused_resume"
elif choice == "3":
    resume = creative_resume()
    template_name = "creative_resume"
else:
    print("Invalid choice. Using Student Resume.")
    resume = student_resume()
    template_name = "student_resume"

letter = cover_letter()

print("\nGenerated Resume:")
print(resume)

print("\nGenerated Cover Letter:")
print(letter)

safe_name = name.lower().replace(" ", "_")

resume_filename = f"{safe_name}_{template_name}.txt"
letter_filename = f"{safe_name}_cover_letter.txt"

with open(resume_filename, "w", encoding="utf-8") as file:
    file.write(resume)

with open(letter_filename, "w", encoding="utf-8") as file:
    file.write(letter)

print("Resume saved to:", resume_filename)
print("Cover letter saved to:", letter_filename)