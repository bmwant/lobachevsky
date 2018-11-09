# -*- coding: utf-8 -*-

"""Top-level package for lobachevsky."""

__author__ = 'Misha Behersky'
__email__ = 'bmwant@gmail.com'
__version__ = '0.1.0'


import settings
from . import views


def setup_routes(app):
    router = app.router
    router.add_get('/', views.index)
    router.add_get('/check_handle', views.check_handle_is_valid)
    router.add_get('/check_repository', views.check_repository_is_valid)
    router.add_get('/check_contributor', views.check_is_a_contributor)


def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=settings.PROJECT_ROOT / 'static',
                          name='static')
    app.router.add_static('/node_modules/',
                          path=settings.PROJECT_ROOT / 'node_modules',
                          name='node_modules')
