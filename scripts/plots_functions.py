from matplotlib import pyplot as plt
import os
import json

DATA_DIR = os.path.abspath(r"../data")

with open(os.path.join(DATA_DIR, 'clubs_info.json')) as file:
    data = json.load(file)


def get_all_clubs_participations(data):
    clubs = [club['NAME'] for club in data]
    participations = [club['PARTICIPATIONS'] for club in data]

    # sort data by participations in descending order
    sorted_clubs, sorted_participations = zip(*[(club['NAME'], club['PARTICIPATIONS']) for club in sorted(data, key=lambda x: x['PARTICIPATIONS'], reverse=True)])

    fig = plt.figure(figsize=(12, 24))
    ax = fig.add_subplot(111)

    ys = [i for i in range(len(clubs))]
    ax.barh(ys, sorted_participations, height=0.8)  # increase height to increase spacing

    plt.title('PARTICIPAÇÕES DOS CLUBES EM SÉRIE A (2003 - 2022)', fontsize=20)
    plt.xlabel('nº de participações', fontsize=14)

    fmt = lambda x, pos: '{:.0f}'.format(x)
    ax.xaxis.set_major_formatter(fmt)

    ax.set_yticks(ys)
    ax.set_yticklabels(sorted_clubs, fontsize=14)

    # modify x-axis tick positions and labels
    xtick_positions = range(0, max(participations) + 1)
    xtick_labels = [str(x) for x in xtick_positions]
    ax.set_xticks(xtick_positions)
    ax.set_xticklabels(xtick_labels)

    plt.subplots_adjust(left=0.25)

    # Add dashed grid lines to y-axis labels
    ax.xaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    plt.show()




get_all_clubs_participations(data)
