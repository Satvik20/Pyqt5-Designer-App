class CricketTeam:

    def __init__(self, team, nationality, is_full_member, points=0, matches_played=0, wins=0, runs=0, wickets=0):
        self.__team = team
        self.__nationality = nationality
        self.__is_full_member = is_full_member
        self.__points = points
        self.__matches_played = matches_played
        self.__wins = wins
        self.__runs = runs
        self.__wickets = wickets

    def reset_all(self):
        self.__points = 0
        self.__matches_played = 0
        self.__wins = 0
        self.__runs = 0
        self.__wickets = 0

    def add_runs(self, runs):
        self.__runs += runs

    def add_wickets(self, wickets):
        self.__wickets += wickets

    def get_runs(self):
        return self.__runs

    def get_wickets(self):
        return self.__wickets

    def get_name(self):
        return self.__team

    def get_nationality(self):
        return self.__nationality

    def is_full_member(self):
        return self.__is_full_member

    def get_points(self):
        return self.__points

    def get_matches_played(self):
        return self.__matches_played

    def get_wins(self):
        return self.__wins

    def get_win_percentage(self):
        if self.__matches_played == 0:
            return 0
        return round(100 * (self.__wins / self.__matches_played), 1)

    def mark_win(self):
        self.__points += 2
        self.__matches_played += 1
        self.__wins += 1

    def mark_draw(self):
        self.__points += 1
        self.__matches_played += 1

    def mark_loss(self):
        self.__matches_played += 1

    def __str__(self):
        return (f"{self.__team} ({self.__nationality}): "
                f"Pts: {self.__points}, Played: {self.__matches_played}, "
                f"Wins: {self.__wins}, Runs: {self.__runs}, Wkts: {self.__wickets}")