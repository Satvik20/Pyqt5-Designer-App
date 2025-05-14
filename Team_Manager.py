import re
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QComboBox, QMessageBox,
    QInputDialog, QFormLayout, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Cricket_Team import CricketTeam

class TeamManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cricket Team Management")
        self.setGeometry(100, 100, 800, 800)

        self.base_font = QFont()
        self.base_font.setPointSize(12)

        self.input_font = QFont()
        self.input_font.setPointSize(18)

        self.team_list = []
        self.current_index = 0
        self.load_teams_from_file()

        self.init_ui()
        self.display_team(0)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Cricket Team Management System")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; padding: 10px;")
        main_layout.addWidget(title)

        details_group = QGroupBox("Team Details")
        details_group.setFont(self.base_font)
        details_layout = QFormLayout()
        details_layout.setVerticalSpacing(10)
        details_layout.setHorizontalSpacing(15)

        self.name_input = self.create_styled_input()
        details_layout.addRow(self.create_label("Team Name:"), self.name_input)

        self.nationality_input = self.create_styled_input()
        details_layout.addRow(self.create_label("Nationality:"), self.nationality_input)

        self.full_member_cb = QCheckBox()
        self.full_member_cb.setFont(self.base_font)
        details_layout.addRow(self.create_label("Full ICC Member:"), self.full_member_cb)

        details_group.setLayout(details_layout)
        main_layout.addWidget(details_group)

        stats_group = QGroupBox("Statistics")
        stats_group.setFont(self.base_font)
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(30)

        left_stats = QFormLayout()
        left_stats.setVerticalSpacing(10)
        left_stats.setHorizontalSpacing(15)

        self.points_input = self.create_styled_input(True)
        left_stats.addRow(self.create_label("Points:"), self.points_input)

        self.matches_input = self.create_styled_input(True)
        left_stats.addRow(self.create_label("Matches Played:"), self.matches_input)

        self.wins_input = self.create_styled_input(True)
        left_stats.addRow(self.create_label("Wins:"), self.wins_input)

        right_stats = QFormLayout()
        right_stats.setVerticalSpacing(10)
        right_stats.setHorizontalSpacing(15)

        self.runs_input = self.create_styled_input(True)
        right_stats.addRow(self.create_label("Runs:"), self.runs_input)

        self.wickets_input = self.create_styled_input(True)
        right_stats.addRow(self.create_label("Wickets:"), self.wickets_input)

        self.win_percentage_input = self.create_styled_input(True)
        right_stats.addRow(self.create_label("Win Percentage:"), self.win_percentage_input)

        stats_layout.addLayout(left_stats)
        stats_layout.addLayout(right_stats)
        stats_group.setLayout(stats_layout)
        main_layout.addWidget(stats_group)

        actions_group = QGroupBox("Match Actions")
        actions_group.setFont(self.base_font)
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        self.win_btn = self.create_action_button("Record Win", "#27ae60")
        self.win_btn.clicked.connect(self.record_win)
        actions_layout.addWidget(self.win_btn)

        self.draw_btn = self.create_action_button("Record Draw", "#f39c12")
        self.draw_btn.clicked.connect(self.record_draw)
        actions_layout.addWidget(self.draw_btn)

        self.loss_btn = self.create_action_button("Record Loss", "#e74c3c")
        self.loss_btn.clicked.connect(self.record_loss)
        actions_layout.addWidget(self.loss_btn)

        actions_group.setLayout(actions_layout)
        main_layout.addWidget(actions_group)

        modifiers_group = QGroupBox("Update Statistics")
        modifiers_group.setFont(self.base_font)
        modifiers_layout = QHBoxLayout()
        modifiers_layout.setSpacing(20)

        runs_layout = QVBoxLayout()
        runs_layout.setSpacing(5)

        self.add_runs_btn = self.create_secondary_button("Add Runs", "#3498db")
        self.add_runs_btn.clicked.connect(self.add_runs)
        runs_layout.addWidget(self.add_runs_btn)

        self.runs_combo = self.create_combo_box()
        runs_layout.addWidget(self.runs_combo)

        wickets_layout = QVBoxLayout()
        wickets_layout.setSpacing(5)

        self.add_wickets_btn = self.create_secondary_button("Add Wickets", "#3498db")
        self.add_wickets_btn.clicked.connect(self.add_wickets)
        wickets_layout.addWidget(self.add_wickets_btn)

        self.wickets_combo = self.create_combo_box()
        wickets_layout.addWidget(self.wickets_combo)

        modifiers_layout.addLayout(runs_layout)
        modifiers_layout.addLayout(wickets_layout)
        modifiers_group.setLayout(modifiers_layout)
        main_layout.addWidget(modifiers_group)

        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)

        self.first_btn = self.create_nav_button("First")
        self.first_btn.clicked.connect(self.first_team)
        nav_layout.addWidget(self.first_btn)

        self.prev_btn = self.create_nav_button("Previous")
        self.prev_btn.clicked.connect(self.prev_team)
        nav_layout.addWidget(self.prev_btn)

        self.next_btn = self.create_nav_button("Next")
        self.next_btn.clicked.connect(self.next_team)
        nav_layout.addWidget(self.next_btn)

        self.last_btn = self.create_nav_button("Last")
        self.last_btn.clicked.connect(self.last_team)
        nav_layout.addWidget(self.last_btn)

        main_layout.addLayout(nav_layout)

        manage_layout = QHBoxLayout()
        manage_layout.setSpacing(10)

        self.reset_btn = self.create_management_button("Reset Team", "#3498db")
        self.reset_btn.clicked.connect(self.reset_team)
        manage_layout.addWidget(self.reset_btn)

        self.new_btn = self.create_management_button("New Team", "#2ecc71")
        self.new_btn.clicked.connect(self.new_team)
        manage_layout.addWidget(self.new_btn)

        self.save_btn = self.create_management_button("Save All", "#9b59b6")
        self.save_btn.clicked.connect(self.save_teams)
        manage_layout.addWidget(self.save_btn)

        self.quit_btn = self.create_management_button("Quit", "#e74c3c")
        self.quit_btn.clicked.connect(self.close)
        manage_layout.addWidget(self.quit_btn)

        main_layout.addLayout(manage_layout)

    def create_label(self, text):
        label = QLabel(text)
        label.setFont(self.base_font)
        return label

    def create_styled_input(self, read_only=False):
        input_field = QLineEdit()
        input_field.setFont(self.input_font)
        input_field.setMinimumHeight(35)

        if read_only:
            input_field.setReadOnly(True)
            input_field.setStyleSheet("""
                QLineEdit {
                    background-color: #f8f9fa;
                    border: 1px solid #ddd;
                    padding: 8px;
                    font-size: 14px;
                }
            """)
        else:
            input_field.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border: 1px solid #ddd;
                    padding: 8px;
                    font-size: 14px;
                }
            """)
        return input_field

    def create_combo_box(self):
        combo = QComboBox()
        combo.setFont(self.input_font)
        combo.addItems([str(i) for i in range(1, 11)])
        combo.setMinimumHeight(35)
        combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                font-size: 12px;
            }
        """)
        return combo

    def create_action_button(self, text, color):
        btn = QPushButton(text)
        btn.setFont(self.base_font)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                min-width: 120px;
                min-height: 40px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
        return btn

    def create_secondary_button(self, text, color):
        btn = QPushButton(text)
        btn.setFont(self.base_font)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
                min-width: 100px;
                min-height: 35px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
        return btn

    def create_nav_button(self, text):
        btn = QPushButton(text)
        btn.setFont(self.base_font)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
                min-width: 100px;
                min-height: 35px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        return btn

    def create_management_button(self, text, color):
        btn = QPushButton(text)
        btn.setFont(self.base_font)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
                min-width: 100px;
                min-height: 35px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
        return btn

    def darken_color(self, hex_color, factor=0.85):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * factor) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

    def has_numbers(self, input_str):
        return bool(re.search(r'\d', input_str))

    def load_teams_from_file(self):
        try:
            with open('cricket_teams.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(':')
                    if len(data) == 8:
                        team = CricketTeam(
                            data[0], data[1], data[2] == 'True',
                            int(data[3]), int(data[4]), int(data[5]),
                            int(data[6]), int(data[7]))
                        self.team_list.append(team)
        except FileNotFoundError:
            self.team_list = [
                CricketTeam("India", "Indian", True, 32, 15, 10, 2500, 120),
                CricketTeam("Australia", "Australian", True, 25, 12, 8, 2400, 110),
                CricketTeam("New Zealand", "New Zealander", True, 22, 12, 7, 2300, 100),
                CricketTeam("England", "English", True, 28, 14, 9, 2450, 115),
                CricketTeam("Pakistan", "Pakistani", True, 26, 13, 8, 2350, 108),
                CricketTeam("South Africa", "South African", True, 24, 13, 7, 2200, 105),
                CricketTeam("Sri Lanka", "Sri Lankan", True, 20, 12, 6, 2150, 102),
                CricketTeam("Bangladesh", "Bangladeshi", True, 18, 11, 5, 2000, 95),
                CricketTeam("West Indies", "West Indian", True, 21, 13, 6, 2100, 97),
                CricketTeam("Afghanistan", "Afghan", True, 19, 12, 5, 1980, 93),
                CricketTeam("Zimbabwe", "Zimbabwean", True, 15, 11, 4, 1850, 89),
                CricketTeam("Ireland", "Irish", True, 16, 11, 4, 1800, 85),
                CricketTeam("Netherlands", "Dutch", False, 12, 10, 3, 1700, 82),
                CricketTeam("Scotland", "Scottish", False, 14, 10, 4, 1750, 84),
                CricketTeam("UAE", "Emirati", False, 11, 9, 3, 1650, 80),
                CricketTeam("Nepal", "Nepali", False, 10, 9, 2, 1600, 78),
                CricketTeam("Oman", "Omani", False, 9, 8, 2, 1550, 76),
                CricketTeam("Namibia", "Namibian", False, 13, 9, 3, 1680, 79),
                CricketTeam("USA", "American", False, 8, 7, 2, 1500, 74),
                CricketTeam("Canada", "Canadian", False, 7, 7, 1, 1480, 73),
                CricketTeam("Kenya", "Kenyan", False, 6, 6, 1, 1400, 70),
                CricketTeam("Bermuda", "Bermudian", False, 5, 6, 1, 1350, 68),
                CricketTeam("Hong Kong", "Hong Konger", False, 4, 5, 1, 1300, 66),
                CricketTeam("PNG", "Papua New Guinean", False, 3, 5, 0, 1250, 64),
                CricketTeam("Germany", "German", False, 2, 4, 0, 1200, 60)
            ]
            self.save_teams()

    def save_teams(self):
        with open('cricket_teams.txt', 'w') as f:
            for team in self.team_list:
                f.write(f"{team.get_name()}:{team.get_nationality()}:{team.is_full_member()}:"
                        f"{team.get_points()}:{team.get_matches_played()}:{team.get_wins()}:"
                        f"{team.get_runs()}:{team.get_wickets()}\n")
        QMessageBox.information(self, "Success", "All teams saved successfully!")

    def display_team(self, index):
        if 0 <= index < len(self.team_list):
            self.current_index = index
            team = self.team_list[index]
            self.name_input.setText(team.get_name())
            self.nationality_input.setText(team.get_nationality())
            self.full_member_cb.setChecked(team.is_full_member())
            self.points_input.setText(str(team.get_points()))
            self.matches_input.setText(str(team.get_matches_played()))
            self.wins_input.setText(str(team.get_wins()))
            self.runs_input.setText(str(team.get_runs()))
            self.wickets_input.setText(str(team.get_wickets()))
            self.win_percentage_input.setText(f"{team.get_win_percentage()}%")

    def validate_inputs(self, team_name, nationality):
        team_name = team_name.strip()
        nationality = nationality.strip()

        if not team_name:
            QMessageBox.warning(self, "Invalid Input", "Team name cannot be empty.")
            return False
        if not nationality:
            QMessageBox.warning(self, "Invalid Input", "Nationality cannot be empty.")
            return False
        if self.has_numbers(team_name):
            QMessageBox.warning(self, "Invalid Input", "Team name cannot contain numbers.")
            return False
        if self.has_numbers(nationality):
            QMessageBox.warning(self, "Invalid Input", "Nationality cannot contain numbers.")
            return False
        return True

    def update_current_team(self):
        if 0 <= self.current_index < len(self.team_list):
            team = self.team_list[self.current_index]
            team_name = self.name_input.text()
            nationality = self.nationality_input.text()

            if not self.validate_inputs(team_name, nationality):
                return

            team._CricketTeam__team = team_name.strip()
            team._CricketTeam__nationality = nationality.strip()
            team._CricketTeam__is_full_member = self.full_member_cb.isChecked()

    def record_win(self):
        self.update_current_team()
        self.team_list[self.current_index].mark_win()
        self.display_team(self.current_index)

    def record_draw(self):
        self.update_current_team()
        self.team_list[self.current_index].mark_draw()
        self.display_team(self.current_index)

    def record_loss(self):
        self.update_current_team()
        self.team_list[self.current_index].mark_loss()
        self.display_team(self.current_index)

    def add_runs(self):
        runs = int(self.runs_combo.currentText())
        self.team_list[self.current_index].add_runs(runs)
        self.display_team(self.current_index)

    def add_wickets(self):
        wickets = int(self.wickets_combo.currentText())
        self.team_list[self.current_index].add_wickets(wickets)
        self.display_team(self.current_index)

    def reset_team(self):
        reply = QMessageBox.question(
            self, 'Confirm Reset',
            "Are you sure you want to reset all statistics for this team?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.team_list[self.current_index].reset_all()
            self.display_team(self.current_index)

    def new_team(self):
        team_name, ok = QInputDialog.getText(
            self, "New Team", "Enter team name:",
            QLineEdit.Normal, "")

        if ok and team_name:
            nationality, ok = QInputDialog.getText(
                self, "New Team", "Enter nationality:",
                QLineEdit.Normal, "")

            if ok and nationality:
                if not self.validate_inputs(team_name, nationality):
                    return

                is_full_member = QMessageBox.question(
                    self, "ICC Status", "Is this team a full ICC member?",
                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes

                new_team = CricketTeam(
                    team_name.strip(),
                    nationality.strip(),
                    is_full_member,
                    0, 0, 0, 0, 0
                )
                self.team_list.append(new_team)
                self.display_team(len(self.team_list) - 1)

    def first_team(self):
        self.display_team(0)

    def prev_team(self):
        if self.current_index > 0:
            self.display_team(self.current_index - 1)

    def next_team(self):
        if self.current_index < len(self.team_list) - 1:
            self.display_team(self.current_index + 1)

    def last_team(self):
        self.display_team(len(self.team_list) - 1)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Confirm Exit',
            "Do you want to save changes before quitting?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )

        if reply == QMessageBox.Save:
            self.save_teams()
            event.accept()
        elif reply == QMessageBox.Discard:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = TeamManager()
    window.show()
    sys.exit(app.exec_())