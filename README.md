Django as your data management framework
========================================

Code samples with comments from the presentation. 
Sides can be found at https://speakerdeck.com/pyporto/django-as-your-data-management-framework

If you come to Python to work with data, most likely you are intimately 
familiar with its data science ecosystem, which includes Anaconda, Jupyter and 
Pandas, among others. Probably though you are less familiar with the other side
of Python, including frameworks, ORMs and template engines, traditionally used 
to create web applications.

The talk aimed at blurring the border between data science and web development
ecosystems and tried to show how Django, extremely popular framework for
creating web applications, could be successfully applied to some common tasks
of data processing and data analysis and how it can be used seamlessly with
your tools of choice.

As an example, we created a Django application to explore tech communities
in Portugal. We tried try different approaches to see what we can get with
them, and how Django specifically can help us. 

Application structure
---------------------

If nothing else, consider Django at least for its ability to organize your work.
The problem of way too many even high profile data science projects is lack of
the common structure. It makes them more difficult to start, to maintain over
time and eventually to pass the knowledge to your colleagues. Sometimes it’s
just a pile of scripts and notebooks, loosely organizer, with probably a README
inside.

Django is quite opinionated on the way you organize your project. On one hand 
it means that you’re not completely free to choose the structure of your 
project. On the other hand though, it means that you feel more at home with 
every new Django project. You open it, and you know where’s what. 

The application itself in Django is quite lightweight, by the way. Two main 
files there are manage.py (which is an executable file you run to perform almost 
all tasks around django) and settings.py, the file which contains global 
configuration of your project. There, inside the project you start creating
apps, which contains the actual code. There’s no projects without at least one
app.

Data to explore
---------------

There is a database db.sqlite3.sample which before initializing the app has
to be renamed to db.sqlite3. The database consists of one table `groups`, which
structure can be explored with

```python
./manage.py inspectdb groups
```

The command looks into your tables and writes models for you. In the context of
web development it has limited functionality, usually to migrate your legacy
system to Django, but in the context of data analysis, it can save quite a lot
of your time if you want to use Django to get access to your external system.

Converting query sets to Pandas dataframes
------------------------------------------

As soon as you get the subset of your data from the database, you may want to
convert it to a more convenient format of pandas data frame for further
processing or simply to print it out. Although there’s no “official way” to 
convert, fortunately, it’s a trivial operation even without it.
 
```python
queryset = Group.objects.filter(…)
df = pd.DataFrame.from_records(queryset.values())
```
  
Speaking of dataframes and how they can be helpful in our environment. Every
dataframe has a method “to_html()” which converts it to a basic HTML table,
good enough to simply show it in the response somewhere in our Django template.


Admin console
-------------

Django admin panel lets you explore your datasets and to modify its elements.
The best thing about it is that you need to write close to zero code to have it.
It’s actually more configuring than coding. 


[admin.py](./explore/communities/admin.py)

The example shows what do you need to define to display the list of community
groups in the admin interface — you create a class definition, define a number 
of properties to tell admin which fields to show, which fields to use for 
filtering and which ones for full-text search.

Even if you don’t have any models in your application yet, Django allows you to
manage users of Django itself with the same interface.


Hints for data people
---------------------

*Can I use Django from Jupyter Notebook?*

You can, but you need to initialize your environment properly to make it 
explicit which project we are working with right now, and also probably
optionally set the PYTHONPATH properly.

Your first cell could look like this

```python
import os
import sys
import django

# Optional, if it's not in PYTHONPATH
sys.path.insert(1, 'path/to/your/django/app')

# Name of your settings module. Name of the file "explore/settings.py" 
# converted to module name "explore.settings". 
# You can also avoid this if you set this as an environment variable before
# starting your notebook server.
os.environ['DJANGO_SETTINGS_MODULE'] = 'explore.settings'

# Initialize Django environment
django.setup()
```

*What is the easiest way to display a plot in my Django view?*

Use [Pygal](https://pygal.org) which draws plots to SVG and put them right in 
your templates. There is an example in views.py.

*Can I serve my Jupyter Notebooks with Django*

It’s not straightforward, but you can convert them to HTML with nbconvert and
serve this way. There is another example in views.py

*How can I initiate long-running tasks from Django views?*

Offload these tasks to workers. For example, use [Celery](http://celeryproject.org/)


MVC (or rather MTV) framework
-----------------------------

Surprisingly enough, Django can provide you a framework to create, well, a
website. From a data person perspective it’s crucial to be able to present your 
data to more general audience, and a customized dynamic dashboard is a better 
option for this purpose a jupyter notebook.

[views.py](./explore/communities/views.py)

It's also important to register all views in the urls.py file to make them
available for the client.

[urls.py](./explore/communities/urls.py)

Each view calls "render" with a template name. Links to templates are also
provided.


List of examples
----------------

- [hello()](./explore/communities/views.py#L13-20). Basic example of a
  Django view, processing request and returing a response from a template.
  Notice a "@staff_member_required" decorator, the way to hide the view
  from unauthorized users. 
  
  Template [hello.html](explore/communities/templates/hello.html)

- [simple_dashboard()](./explore/communities/views.py#L23-34). A very simple
  example showing how you can display your dataset, also protected with
  a "@staff_member_required".
   
  Template [simple_dashboard.html](explore/communities/templates/simple_dashboard.html)

- [plot_dashboard()](./explore/communities/views.py#L37-53). An example of 
  use of [pygal](http://pygal.org) to show inline plots.
   
  Template [plot_dashboard.html](explore/communities/templates/plot_dashboard.html)

- [input_dashboard()](./explore/communities/views.py#L65-96). A more complex
  example of a dashboard with a form. The view uses Django forms to sort and 
  filter data (see FilterForm).
   
  Template [input_dashboard.html](explore/communities/templates/input_dashboard.html)
 
- [notebook()](./explore/communities/views.py#L110-120). An example on how you
  can convert a Jupyter Notebook to HTML and return it from the view. The
  approach employs a nbconvert API. For this to work we had to write a
  custom writer "StringWriter". Also notice how hid all the code and output
  prompts with `exclude_input=True` and `exclude_output_prompt=True`, which
  makes the output less cluttered and more suitable for people who care less
  about *what* you do, and more *what are the results*.
  
- [shiny_dashboard()](./explore/communities/views.py#L123-148). A dashboard
  which simply "looks cool". Uses [Material Design Lite](https://getmdl.io/)
  to format and stylize the dashboard and has two separate files, [reports.py](./explore/communities/reports.py)
  and [graphs.py](./explore/communities/graphs.py) to collect needed information.
   
  Template [shiny_dashboard.html](explore/communities/templates/shiny_dashboard.html)
