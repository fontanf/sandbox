import pulp
import argparse
import plotly.graph_objects as go
import plotly.express as px

parser = argparse.ArgumentParser(description='')
parser.add_argument(
        "-m", "--month",
        type=str,
        help='JAN FEB MAR APR MAY JUN...')
parser.add_argument(
        "-d", "--day",
        type=int,
        help="1 2 3 4...")
args = parser.parse_args()

month2cell = {
        "JAN": (0, 6),
        "FEB": (1, 6),
        "MAR": (2, 6),
        "APR": (3, 6),
        "MAY": (4, 6),
        "JUN": (5, 6),
        "JUL": (0, 5),
        "AUG": (1, 5),
        "SEP": (2, 5),
        "OCT": (3, 5),
        "NOV": (4, 5),
        "DEC": (5, 5),
}
day2cell = {
        1: (0, 4),
        2: (1, 4),
        3: (2, 4),
        4: (3, 4),
        5: (4, 4),
        6: (5, 4),
        7: (6, 4),
        8: (0, 3),
        9: (1, 3),
        10: (2, 3),
        11: (3, 3),
        12: (4, 3),
        13: (5, 3),
        14: (6, 3),
        15: (0, 2),
        16: (1, 2),
        17: (2, 2),
        18: (3, 2),
        19: (4, 2),
        20: (5, 2),
        21: (6, 2),
        22: (0, 1),
        23: (1, 1),
        24: (2, 1),
        25: (3, 1),
        26: (4, 1),
        27: (5, 1),
        28: (6, 1),
        29: (0, 0),
        30: (1, 0),
        31: (2, 0),
}
items = [
        [  # 0
            # OOO
            # OOO
            [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
            # OO
            # OO
            # OO
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
        ], [  # 1
            # O
            # O
            # OOO
            [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
            # OOO
            # O
            # O
            [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
            # OOO
            #   O
            #   O
            [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)],
            #   O
            #   O
            # OOO
            [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        ], [  # 2
            # O
            # OO
            # OO
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)],
            # OO
            # OO
            # O
            [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)],
            # OO
            # OO
            #  O
            [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
            #  O
            # OO
            # OO
            [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)],
            # OO
            # OOO
            [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
            # OOO
            # OO
            [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)],
            # OOO
            #  OO
            [(0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
            #  OO
            # OOO
            [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1)],
        ], [  # 3
            # O
            # O
            # O
            # OO
            [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0)],
            # OO
            # O
            # O
            # O
            [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)],
            #  O
            #  O
            #  O
            # OO
            [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)],
            # OO
            #  O
            #  O
            #  O
            [(0, 3), (1, 0), (1, 1), (1, 2), (1, 3)],
            # O
            # OOOO
            [(0, 0), (0, 1), (1, 0), (2, 0), (3, 0)],
            #    O
            # OOOO
            [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
            # OOOO
            # O
            [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1)],
            # OOOO
            #    O
            [(0, 1), (1, 1), (2, 1), (3, 0), (3, 1)],
        ], [  # 4
            # OO
            # O
            # OO
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)],
            # OO
            #  O
            # OO
            [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],
            # O O
            # OOO
            [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
            # OOO
            # O O
            [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)],
        ], [  # 5
            #  O
            # OO
            # O
            # O
            [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)],
            # O
            # OO
            #  O
            #  O
            [(0, 2), (0, 3), (1, 0), (1, 1), (1, 2)],
            #  O
            #  O
            # OO
            # O
            [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)],
            # O
            # O
            # OO
            #  O
            [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1)],
            #   OO
            # OOO
            [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)],
            # OOO
            #   OO
            [(0, 1), (1, 1), (2, 0), (2, 1), (3, 0)],
            # OO
            #  OOO
            [(0, 1), (1, 0), (1, 1), (2, 0), (3, 0)],
            #  OOO
            # OO
            [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1)],
        ], [  # 6
            # O
            # OO
            # O
            # O
            [(0, 0), (0, 1), (0, 2), (0, 3), (1, 2)],
            # O
            # O
            # OO
            # O
            [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1)],
            #  O
            #  O
            # OO
            #  O
            [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3)],
            #  O
            # OO
            #  O
            #  O
            [(0, 2), (1, 0), (1, 1), (1, 2), (1, 3)],
            #  O
            # OOOO
            [(0, 0), (1, 0), (1, 1), (2, 0), (3, 0)],
            # OOOO
            #  O
            [(0, 1), (1, 0), (1, 1), (2, 1), (3, 1)],
            #   O
            # OOOO
            [(0, 0), (1, 0), (2, 0), (2, 1), (3, 0)],
            # OOOO
            #   O
            [(0, 1), (1, 1), (2, 0), (2, 1), (3, 1)],
        ], [  # 7
            # O
            # OOO
            # O
            [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
            #   O
            # OOO
            #   O
            [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
            # OOO
            #  O
            #  O
            [(0, 2), (1, 0), (1, 1), (1, 2), (2, 2)],
            #  O
            #  O
            # OOO
            [(0, 0), (1, 0), (1, 1), (1, 2), (2, 0)],
        ]
]
valid_cells = set([
        (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
        (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
        (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
        (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
        (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
        (0, 0), (1, 0), (2, 0)])
valid_cells.remove(month2cell[args.month])
valid_cells.remove(day2cell[args.day])
print("valid_cells", valid_cells)
w = max(x for x, y in valid_cells)
h = max(y for x, y in valid_cells)
print("w", w)
print("h", h)
# Compute all valid item positions.
# List of tuples (item, rotation, x, y).
valid_item_positions = [[] for item in items]
# covering[(x, y)] = list of valid item positions covering (x, y)
covering = {(x, y): [] for (x, y) in valid_cells}
for j, item in enumerate(items):
    for r, cells in enumerate(item):
        for x in range(w):
            for y in range(h):
                ok = True
                for (xj, yj) in cells:
                    if (x + xj, y + yj) not in valid_cells:
                        ok = False
                        break
                if ok:
                    valid_item_positions[j].append((r, x, y))
                    for (xj, yj) in cells:
                        covering[(x + xj, y + yj)].append((j, r, x, y))
    print("valid_item_positions j", j, valid_item_positions[j])
# Build model.
model = pulp.LpProblem()
# Variables.
variables = {}
for j, item in enumerate(items):
    for r, x, y in valid_item_positions[j]:
        variables[(j, r, x, y)] = pulp.LpVariable(
                "v_j" + str(j) + "_r" + str(r) + "_x" + str(x) + "_y" + str(y),
                0,  # Lower bound
                1,  # Upper bound
                pulp.LpBinary)
# Demand constraints.
for j, item in enumerate(items):
    model += (pulp.lpSum(variables[(j, r, x, y)]
                         for (r, x, y) in valid_item_positions[j]) == 1)
# Cover constraints: one constraint for each available cell.
for (x, y) in valid_cells:
    model += (pulp.lpSum(variables[(j, r, xj, yj)]
                         for (j, r, xj, yj) in covering[(x, y)]) == 1)
# Solve.
model.solve()

# Retrieve solution.
fig = go.Figure()
# Same scale for both axis.
fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1)
# Draw solution.
colors = px.colors.qualitative.Plotly
print("Solution")
for j, item in enumerate(items):
    for r, x, y in valid_item_positions[j]:
        if variables[(j, r, x, y)].varValue < 0.5:
            continue
        print([(x + xj, y + yj) for xj, yj in items[j][r]])
        plotly_x = []
        plotly_y = []
        for xj, yj in items[j][r]:
            plotly_x += [x + xj, x + xj + 1, x + xj + 1, x + xj, x + xj, None]
            plotly_y += [y + yj, y + yj, y + yj + 1, y + yj + 1, y + yj, None]
        fig.add_trace(go.Scatter(
            x=plotly_x,
            y=plotly_y,
            marker=None,
            fillcolor=colors[j],
            fill="toself"))
# Draw grid.
plotly_x = []
plotly_y = []
for y in range(6, -1, -1):
    for x in range(0, 7):
        if y >= 5 and x == 6:
            continue
        if y == 0 and x >= 3:
            continue
        plotly_x += [x, x + 1, x + 1, x, x, None]
        plotly_y += [y, y, y + 1, y + 1, y, None]
fig.add_trace(go.Scatter(
    x=plotly_x,
    y=plotly_y,
    marker=dict(
        color='black',
        size=20)))
# Draw months and days.
plotly_x = []
plotly_y = []
for y in range(6, -1, -1):
    for x in range(0, 7):
        if y >= 5 and x == 6:
            continue
        if y == 0 and x >= 3:
            continue
        plotly_x.append(x + 0.5)
        plotly_y.append(y + 0.5)
fig.add_trace(go.Scatter(
    x=plotly_x,
    y=plotly_y,
    mode="text",
    text=[k for k in month2cell.keys()] + [k for k in day2cell.keys()],
    textfont=dict(size=32),
    textposition="middle center"))
# Plot.
fig.show()
