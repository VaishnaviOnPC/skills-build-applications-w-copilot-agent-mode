from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data using raw SQL to avoid unhashable instance issues
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM octofit_tracker_user")
            cursor.execute("DELETE FROM octofit_tracker_team_members")
            cursor.execute("DELETE FROM octofit_tracker_team")
            cursor.execute("DELETE FROM octofit_tracker_activity")
            cursor.execute("DELETE FROM octofit_tracker_leaderboard")
            cursor.execute("DELETE FROM octofit_tracker_workout")

        # Create users
        users = [
            User(email="user1@example.com", name="User One"),
            User(email="user2@example.com", name="User Two"),
            User(email="user3@example.com", name="User Three"),
        ]
        User.objects.bulk_create(users)

        # Retrieve saved users from the database
        users = list(User.objects.all())

        # Create teams
        team = Team(name="Team A")
        team.save()
        team.members.set(users)

        # Create activities
        activities = [
            Activity(user=users[0], activity_type="Running", duration=30, date=date(2025, 4, 8)),
            Activity(user=users[1], activity_type="Cycling", duration=60, date=date(2025, 4, 8)),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(user=users[0], score=100),
            Leaderboard(user=users[1], score=90),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name="Morning Run", description="A quick morning run", duration=30),
            Workout(name="Evening Cycle", description="Cycling in the evening", duration=60),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))