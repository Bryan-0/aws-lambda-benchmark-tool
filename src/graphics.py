import matplotlib.pyplot as plt


class Graphics:

    @staticmethod
    def draw_line_graph(title, x_axis, y_axis, x_label, y_label, filename):
        plt.clf()

        plt.title(title)
        plt.plot(x_axis, y_axis)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.xticks(ticks=plt.xticks()[0], labels=plt.xticks()[0].astype(int))
        plt.savefig(filename)
