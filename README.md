# sbyc_course_app

This app provides a simple interface for courses and flags of South Beach Yacht Club's Friday Night Series.

Quick start
-----------

1. Add "sbyc_course_app" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'sbyc_course_app',
    ]

2. Include the sbyc_course_app URLconf in your project urls.py like this:
    path('sbyc_course_app/', include('sbyc_course_app.urls')),

3. Start the development server with `python manage.py runserver` and visit http://127.0.0.1:8000/admin/.

No need to run migrations, there is no database for this app.
