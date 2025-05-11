import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Visualizer:
    def __init__(self):
        self.df = pd.read_csv("game_results.csv")

    def get_statistics(self):
        features = {
            'Total Moves': 'Total moves taken',
            'Hearts Lost': 'Hearts lost',
            'Time Taken(s)': 'Time'
        }

        stat_types = ['Min', 'Max', 'Average', 'Median', 'Std Dev']
        stats_data = {'Feature': list(features.keys())}

        for stat in stat_types:
            if stat == 'Min':
                values = [self.df[col].min() for col in features.values()]
            elif stat == 'Max':
                values = [self.df[col].max() for col in features.values()]
            elif stat == 'Average':
                values = [self.df[col].mean() for col in features.values()]
            elif stat == 'Median':
                values = [self.df[col].median() for col in features.values()]
            elif stat == 'Std Dev':
                values = [self.df[col].std() for col in features.values()]
            stats_data[stat] = [round(v, 2) for v in values]

        countdown_pct = round((self.df["Fail reason"].fillna("None") == "CountdownBomb").mean() * 100, 2)
        result_counts = self.df["Result"].value_counts(normalize=True) * 100
        win_pct = round(result_counts.get("win", 0), 2)
        loss_pct = round(result_counts.get("lose", 0), 2)

        col_labels = list(stats_data.keys())
        cell_text = [
            [stats_data[col][i] for col in col_labels]
            for i in range(len(stats_data['Feature']))
        ]

        plt.figure(figsize=(6, 4))
        plt.title('Statistics Summary', fontsize=24, fontweight='bold')
        plt.axis('off')
        table = plt.table(
            cellText=cell_text,
            colLabels=col_labels,
            loc='center',
            cellLoc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.0, 1.2)

        plt.figtext(
            0.5, 0.05,
            f"Countdown Bomb Failures: {countdown_pct}%\n"
            f"Win/Loss Ratio: {win_pct}% / {loss_pct}%",
            ha='center', fontsize=10, bbox=None
        )

        plt.tight_layout()
        plt.savefig("image/graphs/summary_table.png", dpi=120, bbox_inches='tight')
        plt.close()

    def histogram_moves(self):
        plt.figure(figsize=(6, 4))
        sns.histplot(self.df["Total moves taken"], kde=True, bins=10, color="skyblue")
        plt.title("Total Moves Taken per Game")
        plt.xlabel("Moves")
        plt.ylabel("Frequency")
        plt.tight_layout()

        plt.savefig("image/graphs/histogram_moves.png")

    def bar_hearts_lost(self):
        plt.figure(figsize=(6, 4))
        sns.countplot(x="Hearts lost", data=self.df, palette="Reds", legend=False)
        plt.title("Hearts Lost per Game")
        plt.xlabel("Hearts Lost")
        plt.ylabel("Count")
        plt.tight_layout()

        plt.savefig("image/graphs/bar_hearts_lost.png")
        plt.close()

    def box_time_taken(self):
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=self.df["Time"], color="lightgreen")
        plt.title("Time Taken per Game")
        plt.xlabel("Seconds")
        plt.tight_layout()

        plt.savefig("image/graphs/box_time_taken.png")

    def pie_countdown_fail(self):
        fail = self.df["Fail reason"].fillna("None")
        labels = ["CountdownBomb" if f == "CountdownBomb" else "Other" for f in fail]
        counts = pd.Series(labels).value_counts()
        plt.figure(figsize=(6, 4))
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
        plt.title("Countdown Bomb Failures")
        plt.tight_layout()

        plt.savefig("image/graphs/pie_countdown_fail.png")

    def pie_win_loss(self):
        counts = self.df["Result"].value_counts()
        plt.figure(figsize=(6, 4))
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
        plt.title("Win/Loss Ratio")
        plt.tight_layout()

        plt.savefig("image/graphs/pie_win_loss.png")
