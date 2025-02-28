class Constants:
    COMPANY_SUFFIX_EXHAUSTIVE_LIST = ",".join(c_suf.lower() for c_suf in [
        "Pvt. Ltd", "Private Limited", "Ltd", "Pvt.", "Limited", "Inc.", "Incorporated", "LLC",
        "GmbH", "S.A.", "S.A.S.", "P.L.C.", "Corp", "Corporation",
        "Co.", "Company", "Holdings", "Group", "Enterprises", "Ventures", "FZCO",
        "StartUpWaves", "Innovations", "Careem", "Solutions"
    ])

    JOB_TITLES_EXHAUSTIVE_LIST = ",".join(title.lower() for title in [
        # Executive & Leadership Titles
        "CEO", "COO", "CFO", "CTO", "CMO", "CSO", "CPO",
        "President", "Vice President", "Director", "Managing Director",
        "General Manager", "Founder", "Co-Founder", "Partner",

        # Management Titles
        "Head of Department", "Senior Manager", "Associate Manager", "Team Lead",
        "Lead Engineer", "Lead Designer", "Supervisor", "Coordinator", "Administrator",

        # Technical & Engineering Titles
        "Software Engineer", "Software Developer", "Backend Engineer", "Backend Developer", "Frontend Engineer",
        "Frontend Developer", "Full Stack Engineer", "DevOps Engineer", "Cloud Engineer", "Machine Learning Engineer",
        "Data Scientist", "AI Engineer", "Data Engineer", "Cybersecurity Engineer", "Embedded Systems Engineer",
        "Network Engineer", "Systems Architect", "Solutions Architect", "Technical Lead", "Software Developer Intern",
        "Principal Engineer", "Staff Engineer", "Tech Lead", "VP of Engineering", "Senior Software Engineer",
        "Senior Software Developer", "Senior Backend Engineer", "Senior Backend Developer", "Senior Frontend Engineer",
        "Senior Frontend Developer", "Product Manager", "Senior Product Manager", "Associate Product Manager"

        # Marketing & Sales Titles
        "Marketing Manager", "Growth Marketer", "Digital Marketing Specialist", "Brand Manager",
        "Content Strategist", "SEO Specialist", "Social Media Manager", "Public Relations Manager",
        "Advertising Manager", "Account Manager", "Sales Executive", "Business Development Manager",
        "Customer Success Manager", "Inside Sales Representative", "Field Sales Representative", "Head of Marketing",
        "Senior Brand Marketer"

        # Human Resources (HR) Titles
        "HR Manager", "HR Business Partner", "Talent Acquisition Specialist", "Recruiter",
        "Training & Development Manager", "Compensation & Benefits Specialist", "Employee Relations Manager",

        # Creative & Design Titles
        "UX Designer", "UI Designer", "Graphic Designer", "Product Designer",
        "Art Director", "Creative Director", "Motion Graphics Designer", "Animator",

    ]
                                          )
