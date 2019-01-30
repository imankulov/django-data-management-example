import pandas as pd
import pygal
from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from explore.communities.models import Group
from nbconvert import HTMLExporter
from nbconvert.nbconvertapp import NbConvertApp
from nbconvert.writers import WriterBase


@staff_member_required
def hello(request):
    """
    Hello world example on how template context is passed though
    """
    return render(request, 'hello.html', {
        'user': request.GET.get('user'),
    })


@staff_member_required
def simple_dashboard(request):
    """
    Simple dashboard example, essentially displaying how Django templates
    work, as well as how you can convert the output of a Django query to a
    Pandas dataframe.
    """
    groups = Group.objects.filter(country='PT').order_by('-members')[:10]
    df = pd.DataFrame.from_records(groups.values())
    return render(request, 'simple_dashboard.html', {
        'df': df,
    })


@staff_member_required
def plot_dashboard(request):
    """
    Example on how you can create a dashboard with tables and plots, using
    Pygal (http://pygal.org)
    """
    groups = Group.objects.filter(country='PT').order_by('-members')[:10]
    df = pd.DataFrame.from_records(groups.values())
    bar = pygal.Bar(show_legend=False, x_label_rotation=270, height=400)
    bar.x_labels = df.name
    bar.add('Members', df.members)
    return render(
        request,
        'plot_dashboard.html', {
            'df': df,
            'bar': bar.render(is_unicode=True),
        })


class FilterForm(forms.Form):
    limit = forms.IntegerField(min_value=1)
    order_by = forms.ChoiceField(choices=[
        ('created', 'oldest first'),
        ('-members', 'most members first'),
    ])
    name_contains = forms.CharField(required=False)


@staff_member_required
def input_dashboard(request):
    """
    Example on how you can create a dynamic dashboard using Django templates
    and forms. The form of the example let you sort, filter and limit the
    output.
    """
    # initialize the form
    default_data = {
        'limit': 10,
        'order_by': '-members',
        'name_contains': '',
    }
    form = FilterForm(data=request.GET or None, initial=default_data)

    if form.is_valid():
        # form-based filtration
        data = form.cleaned_data
    else:
        # default values for filtration
        data = default_data

    groups = Group.objects.filter(country='PT').order_by(data['order_by'])
    if data['name_contains']:
        groups = groups.filter(name__icontains=data['name_contains'])
    groups = groups[:data['limit']]
    df = pd.DataFrame.from_records(groups.values())

    return render(request, 'input_dashboard.html', {
        'form': form,
        'df': df,
    })


class StringWriter(WriterBase):
    """
    Simple writer which just stores the content of the notebook to its
    "content" attribute
    """
    content = None

    def write(self, output, resources, **kw):
        self.content = output


@staff_member_required
def notebook(request):
    """
    Example on how Jupyter Notebook can be converted to HTML and returned
    from a Django view
    """
    exporter = HTMLExporter(exclude_input=True, exclude_output_prompt=True)
    writer = StringWriter()
    app = NbConvertApp(writer=writer, exporter=exporter)
    app.convert_single_notebook('./notebooks/sample.ipynb')
    return HttpResponse(writer.content)


@staff_member_required
def shiny_dashboard(request):
    """
    "Shiny dashboard", the one which creates a beautifully looking dashboard
    using Pygal (http://pygal.org) and Material Design Lite (https://getmdl.io/)
    """
    # import resources for the shiny dashboard here for the sake of keeping
    # the example self-sufficient.
    from explore.communities import graphs, reports

    top_groups_df = reports.top_groups()
    top_groups_plot = graphs.top_groups_barplot(top_groups_df)

    growth_df = reports.meetup_groups_growth()
    growth_plot = graphs.meetup_groups_growth(growth_df)

    dynamic_df = reports.meetup_groups_dynamic(growth_df)
    dynamic_plot = graphs.meetup_groups_dynamic(dynamic_df)
    return render(
        request,
        'shiny_dashboard.html', {
            'top_groups_df': top_groups_df,
            'top_groups_plot': top_groups_plot.render(is_unicode=True),
            'growth_plot': growth_plot.render(is_unicode=True),
            'dynamic_plot': dynamic_plot.render(is_unicode=True),
        })
