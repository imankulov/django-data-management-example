import pygal
from pygal.style import DefaultStyle

style = DefaultStyle(
    background='rgba(255, 255, 255, 1)',
    font_family='"Roboto","Helvetica","Arial",sans-serif')


def top_groups_barplot(df):
    """
    Return barplot with top group members, based on the report
    "top_groups"
    """
    bar = pygal.Bar(
        style=style,
        show_legend=False,
        x_label_rotation=270,
        truncate_label=30,
        margin=0,
        width=600,
        height=300,
        show_minor_y_labels=False,
        show_x_labels=False)
    bar.x_labels = df.name
    bar.add('Members', df.members)
    return bar


def meetup_groups_growth(df):
    plot = pygal.StackedLine(
        style=style,
        fill=True,
        show_dots=False,
        x_labels_major_every=4,
        show_minor_x_labels=False,
        show_minor_y_labels=False,
        x_label_rotation=270)

    plot.x_labels = [v.strftime('%b %Y') for v in df.index]
    for city, records in df.iteritems():
        plot.add(city, records)
    return plot


def meetup_groups_dynamic(df):
    plot = pygal.StackedLine(
        style=style,
        fill=True,
        show_dots=False,
        stack_from_top=True,
        x_labels_major_every=4,
        show_minor_x_labels=False,
        show_minor_y_labels=False,
        x_label_rotation=270)

    plot.x_labels = [v.strftime('%b %Y') for v in df.index]
    for city, records in df.iteritems():
        plot.add(city, records)
    return plot
