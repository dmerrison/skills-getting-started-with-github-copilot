"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    # Intellectual Activities
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Society": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Prepare for debate tournaments and practice public speaking",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["jack@mergington.edu", "elijah@mergington.edu"]
    },
    "Maths Society": {
        "description": "Problem solving, competitions, and maths enrichment",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["sophia.m@mergington.edu", "lucas@mergington.edu"]
    },
    "History Society": {
        "description": "Explore British and world history through talks and trips",
        "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["george@mergington.edu", "alice@mergington.edu"]
    },

    # Artistic Activities
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["mia@mergington.edu", "amelia@mergington.edu"]
    },
    "Drama Society": {
        "description": "Acting workshops, rehearsals, and stage productions",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["charlotte@mergington.edu", "harper@mergington.edu"]
    },
    "Choir": {
        "description": "Sing in a variety of styles and perform at school events",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 30,
        "participants": ["lucy@mergington.edu", "thomas@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn photography techniques and participate in exhibitions",
        "schedule": "Tuesdays, 3:45 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["ella@mergington.edu", "oscar@mergington.edu"]
    },

    # Sports Activities
    "Football Team": {
        "description": "Competitive football (soccer) team practices and matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Cricket Club": {
        "description": "Practice cricket skills and play friendly matches",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 16,
        "participants": ["harry@mergington.edu", "freddie@mergington.edu"]
    },
    "Netball Club": {
        "description": "Netball training sessions and inter-school matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["grace@mergington.edu", "ruby@mergington.edu"]
    },
    "Rugby Team": {
        "description": "Rugby training and fixtures against local schools",
        "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["archie@mergington.edu", "alfie@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")  
    
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
