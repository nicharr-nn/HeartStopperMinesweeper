import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Graph:
    def __init__(self, title=None):
        self.df = pd.read_csv("game_results.csv")
        self.title = title

    def histogram_moves(self):
        plt.figure(figsize=(6, 4))
        sns.histplot(self.df["Total moves taken"], kde=True, bins=10, color="skyblue")
        plt.title("Total Moves Taken per Game")
        plt.xlabel("Moves")
        plt.ylabel("Frequency")
        plt.tight_layout()

        plt.savefig("image/graphs/histogram_moves.png")


    def bar_hearts_lost(self):
        plt.figure()
        sns.countplot(x=self.df["Hearts lost"], palette="Reds")
        plt.title("Feature 2: Hearts Lost per Game")
        plt.xlabel("Hearts Lost")
        plt.ylabel("Count")
        plt.tight_layout()

        plt.savefig("image/graphs/bar_hearts_lost.png")

    def box_time_taken(self):
        plt.figure()
        sns.boxplot(x=self.df["Time"], color="lightgreen")
        plt.title("Feature 3: Time Taken per Game")
        plt.xlabel("Seconds")
        plt.tight_layout()

        plt.savefig("image/graphs/box_time_taken.png")

    def pie_countdown_fail(self):
        fail = self.df["Fail reason"].fillna("None")
        labels = ["CountdownBomb" if f == "CountdownBomb" else "Other" for f in fail]
        counts = pd.Series(labels).value_counts()
        plt.figure()
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
        plt.title("Feature 4: Countdown Bomb Failures")
        plt.tight_layout()

        plt.savefig("image/graphs/pie_countdown_fail.png")

    def pie_win_loss(self):
        counts = self.df["Result"].value_counts()
        plt.figure()
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
        plt.title("Feature 5: Win/Loss Ratio")
        plt.tight_layout()

        plt.savefig("image/graphs/pie_win_loss.png")
