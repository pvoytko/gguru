# -*- coding: utf-8 -*-




# Этот декортатор проверяет 2 вещи
# 1. Юзер залогинне
# Только в этом случае целевой вью отрабатывает. Иначе - перекидываем его на страницу логина.
def login_required(f):
    from django.contrib.auth.decorators import login_required
    return login_required(f, login_url = '/login/')

# Делает рендер в HTML того контекст который получает от Вью из return
def render_html(templateName):
    def render_html_decor(f):
        def render_html_wrapper(request, *args, **kwargs):
            from   django.shortcuts import render
            return render(
                request,
                templateName,
                f(request, *args, **kwargs)
            )
        return render_html_wrapper
    return render_html_decor