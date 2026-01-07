from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# ======================================================
# SAMPLE DATA (Mock Database)
# ======================================================

PROJECTS_DATA = [
    {
        "id": 1,
        "title": "AI-Powered Study Assistant",
        "description": "An intelligent assistant that helps students organize their study materials and schedule.",
        "technology": ["Python", "AI", "Web"],
        "price": 49.99,
        "difficulty": "Advanced",
        "rating": 5,
        "popularity": 95,
        "date_added": "2023-10-15",
        "seller": "TechStudent123",
        "image": "https://via.placeholder.com/300x200?text=AI+Assistant",
        "sales_count": 25
    },
    {
        "id": 2,
        "title": "Smart Campus Navigation",
        "description": "An app that helps students navigate campus with real-time updates.",
        "technology": ["Android", "IoT", "Maps"],
        "price": 29.99,
        "difficulty": "Intermediate",
        "rating": 4,
        "popularity": 87,
        "date_added": "2023-11-02",
        "seller": "CampusDev",
        "image": "https://via.placeholder.com/300x200?text=Campus+Nav",
        "sales_count": 18
    },
    {
        "id": 3,
        "title": "Eco-Friendly Shopping Platform",
        "description": "A web platform connecting consumers with sustainable products.",
        "technology": ["Web", "Python", "Data Science"],
        "price": 39.99,
        "difficulty": "Intermediate",
        "rating": 4,
        "popularity": 78,
        "date_added": "2023-11-10",
        "seller": "GreenTech",
        "image": "https://via.placeholder.com/300x200?text=Eco+Platform",
        "sales_count": 32
    },
    {
        "id": 4,
        "title": "Virtual Lab Simulator",
        "description": "A physics lab simulator for remote learning environments.",
        "technology": ["Web", "JavaScript", "Simulation"],
        "price": 59.99,
        "difficulty": "Advanced",
        "rating": 5,
        "popularity": 92,
        "date_added": "2023-10-28",
        "seller": "SciencePro",
        "image": "https://via.placeholder.com/300x200?text=Lab+Simulator",
        "sales_count": 15
    },
    {
        "id": 5,
        "title": "Mental Health Tracker",
        "description": "An app to track mood and provide mental wellness resources.",
        "technology": ["Android", "AI", "Health"],
        "price": 24.99,
        "difficulty": "Beginner",
        "rating": 4,
        "popularity": 83,
        "date_added": "2023-11-05",
        "seller": "WellnessDev",
        "image": "https://via.placeholder.com/300x200?text=Health+Tracker",
        "sales_count": 22
    },
    {
        "id": 6,
        "title": "Blockchain Voting System",
        "description": "A secure voting system using blockchain technology.",
        "technology": ["Blockchain", "Web", "Security"],
        "price": 79.99,
        "difficulty": "Advanced",
        "rating": 5,
        "popularity": 88,
        "date_added": "2023-10-20",
        "seller": "SecureVote",
        "image": "https://via.placeholder.com/300x200?text=Voting+System",
        "sales_count": 12
    }
]

CATEGORY_MAPPINGS = {
    "web_development": ["Web"],
    "app_development": ["Android"],
    "web_application": ["Web"],
    "data_science": ["Data Science"],
    "aiml": ["AI"],
    "blockchain": ["Blockchain"],
    "cyber_security": ["Security"],
    "cloud_computing": ["Cloud"]
}

# ======================================================
# HELPER FUNCTIONS
# ======================================================

def filter_projects(projects, categories, project_type, price_range, difficulties):
    filtered = projects.copy()

    # Category filter
    if categories:
        tech_filters = []
        for cat in categories:
            tech_filters.extend(CATEGORY_MAPPINGS.get(cat, []))
        filtered = [p for p in filtered if any(t in p["technology"] for t in tech_filters)]

    # Project type filter
    if project_type == "mini":
        filtered = [p for p in filtered if p["price"] < 40]
    elif project_type == "major":
        filtered = [p for p in filtered if p["price"] >= 40]

    # Price filter
    if price_range == "under_30":
        filtered = [p for p in filtered if p["price"] < 30]
    elif price_range == "30_60":
        filtered = [p for p in filtered if 30 <= p["price"] <= 60]
    elif price_range == "over_60":
        filtered = [p for p in filtered if p["price"] > 60]

    # Difficulty filter
    if difficulties:
        difficulty_map = {
            "beginner": "Beginner",
            "intermediate": "Intermediate",
            "advanced": "Advanced"
        }
        diff_levels = [difficulty_map[d] for d in difficulties]
        filtered = [p for p in filtered if p["difficulty"] in diff_levels]

    return filtered


def sort_projects(projects, sort_by):
    if sort_by == "newest":
        return sorted(projects, key=lambda x: x["date_added"], reverse=True)
    if sort_by == "price-low":
        return sorted(projects, key=lambda x: x["price"])
    if sort_by == "price-high":
        return sorted(projects, key=lambda x: x["price"], reverse=True)

    return sorted(projects, key=lambda x: (-x["popularity"], -x["sales_count"]))


# ======================================================
# ROUTES
# ======================================================

@app.route("/")
def index():
    trending = sort_projects(PROJECTS_DATA, "popularity")[:4]
    new_projects = sort_projects(PROJECTS_DATA, "newest")[:4]
    mini_projects = sorted(PROJECTS_DATA, key=lambda x: x["price"])[:4]
    top_selling = sorted(PROJECTS_DATA, key=lambda x: x["sales_count"], reverse=True)[:3]

    categories = [
        "Web Development",
        "Mobile App",
        "Web Application",
        "Data Science",
        "Artificial Intelligence",
        "Blockchain",
        "Cybersecurity",
        "Cloud Computing"
    ]

    return render_template(
        "index.html",
        trending_projects=trending,
        new_projects=new_projects,
        mini_projects=mini_projects,
        top_selling_projects=top_selling,
        categories=categories
    )


@app.route("/browse_all_projects")
def browse_all_projects():
    categories = request.args.getlist("categories")
    project_type = request.args.get("project_type", "")
    price_range = request.args.get("price_range", "")
    difficulties = request.args.getlist("difficulty")
    sort_by = request.args.get("sort", "popularity")

    filtered = filter_projects(PROJECTS_DATA, categories, project_type, price_range, difficulties)
    sorted_projects = sort_projects(filtered, sort_by)

    return render_template("browse_all_projects.html", projects=sorted_projects)


@app.route("/api/filter_projects")
def api_filter_projects():
    categories = request.args.getlist("categories")
    project_type = request.args.get("project_type", "")
    price_range = request.args.get("price_range", "")
    difficulties = request.args.getlist("difficulty")
    sort_by = request.args.get("sort", "popularity")

    filtered = filter_projects(PROJECTS_DATA, categories, project_type, price_range, difficulties)
    sorted_projects = sort_projects(filtered, sort_by)

    category_counts = {
        key: sum(1 for p in PROJECTS_DATA if any(t in p["technology"] for t in techs))
        for key, techs in CATEGORY_MAPPINGS.items()
    }

    return {
        "projects": sorted_projects,
        "total_count": len(sorted_projects),
        "category_counts": category_counts,
        "project_type_counts": {
            "mini": len([p for p in PROJECTS_DATA if p["price"] < 40]),
            "major": len([p for p in PROJECTS_DATA if p["price"] >= 40])
        }
    }


@app.route("/project/<int:project_id>")
def project_details(project_id):
    project = next((p for p in PROJECTS_DATA if p["id"] == project_id), None)
    if not project:
        flash("Project not found.", "error")
        return redirect(url_for("index"))
    return render_template("project_details.html", project=project)


@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    results = [
        p for p in PROJECTS_DATA
        if query in p["title"].lower()
        or query in p["description"].lower()
        or any(query in tech.lower() for tech in p["technology"])
    ]
    return render_template("browse_all_projects.html", projects=results)


@app.route("/sell_your_project", methods=["GET", "POST"])
def sell_your_project():
    if request.method == "POST":
        flash("Your project has been submitted successfully!", "success")
        return redirect(url_for("index"))
    return render_template("sell_your_project.html")


@app.route("/custom_project_request", methods=["POST"])
def custom_project_request():
    flash("Your custom project request has been submitted! We will contact you soon.", "success")
    return redirect(url_for("index"))

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms_of_service.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



# ======================================================
# APP RUN
# ======================================================

if __name__ == "__main__":
    app.run(debug=True)
