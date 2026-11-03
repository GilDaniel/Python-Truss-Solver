import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FormatStrFormatter


class TrussPlot:
    def __init__(self, nodes, elements):
        self.nodes = nodes
        self.elements = elements

    def plot(self, show=True):
        fig, ax = plt.subplots()
        force_colors = {
            "Tension": "tab:blue",
            "Compression": "tab:red",
        }

        for element in self.elements:
            x_values = [element.node1.x, element.node2.x]
            y_values = [element.node1.y, element.node2.y]
            color = force_colors.get(getattr(element, "force_type", None), "tab:gray")
            ax.plot(x_values, y_values, color=color, linewidth=2)
            if hasattr(element, "tension"):
                stress_label = f"{element.tension / 1e6:.2f} MPa"
                if element.force_type == "Compression":
                    stress_label += (
                        f"\ncr: {element.critical_buckling_tension / 1e6:.2f} MPa"
                    )
                ax.annotate(
                    stress_label,
                    (sum(x_values) / 2, sum(y_values) / 2),
                    xytext=(0, 2),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=6,
                )

        x_values = [node.x for node in self.nodes]
        y_values = [node.y for node in self.nodes]
        ax.scatter(x_values, y_values, color="black", zorder=3)
        span = max(
            max(x_values) - min(x_values),
            max(y_values) - min(y_values),
            1,
        )
        arrow_length = 0.12 * span
        support_legend = {}

        for node in self.nodes:
            ax.annotate(
                node.name,
                (node.x, node.y),
                xytext=(5, 5),
                textcoords="offset points",
            )

            restrained_x = bool(node.restX)
            restrained_y = bool(node.restY)
            if restrained_x and restrained_y:
                marker = "^"
                support_type = "Fixed support (X and Y)"
            elif restrained_x or restrained_y:
                marker = "o"
                support_type = "Roller support (one direction)"
            else:
                marker = None

            if marker:
                ax.scatter(
                    [node.x],
                    [node.y],
                    marker=marker,
                    s=100,
                    facecolors="white",
                    edgecolors="black",
                    linewidths=1.5,
                    zorder=4,
                )
                support_legend[support_type] = marker

            force_x = node.extForceX
            force_y = node.extForceY
            if force_x:
                dx = arrow_length if force_x > 0 else -arrow_length
                ax.annotate(
                    "",
                    xy=(node.x + dx, node.y),
                    xytext=(node.x, node.y),
                    arrowprops={"arrowstyle": "->", "color": "tab:green", "lw": 1.5},
                )

            if force_y:
                dy = arrow_length if force_y > 0 else -arrow_length
                ax.annotate(
                    "",
                    xy=(node.x, node.y + dy),
                    xytext=(node.x, node.y),
                    arrowprops={"arrowstyle": "->", "color": "tab:orange", "lw": 1.5},
                )

        x_span = max(x_values) - min(x_values)
        y_span = max(y_values) - min(y_values)
        padding = 0.25 * span
        ax.set_xlim(min(x_values) - padding, max(x_values) + padding)
        ax.set_ylim(min(y_values) - padding, max(y_values) + padding)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Truss structure")
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.3f"))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.3f"))
        ax.grid(True, linestyle="--", alpha=0.4)
        if support_legend:
            ax.legend(
                handles=[
                    Line2D(
                        [],
                        [],
                        color="black",
                        marker=marker,
                        linestyle="None",
                        markerfacecolor="white",
                        markersize=8,
                        label=support_type,
                    )
                    for support_type, marker in support_legend.items()
                ]
            )

        if show:
            plt.show()

        return fig, ax
