# -*- coding: utf-8 -*-

import fw
from   django.views.decorators.csrf import csrf_exempt
import django.contrib.auth.models
import gg_json
import django.contrib.auth.forms
from   django import forms
import cud_operations
import models

# Редактирование и создание юзеров
class GgUserForm(forms.ModelForm):
    class Meta:
        model = django.contrib.auth.models.User
        fields = ['email', 'password']

    # Эл. почту делем обязательным полем, иначе она не обязательна у Джанги.
    def __init__(self, *args, **kwargs):
        super(GgUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password'].required = True

    # Добавляем проверку на уникальность емейла
    def clean_email(self):

        # Получаем какой емейл хотим установить юзеру
        email = self.cleaned_data.get('email')

        # Получаем запрос на всех пользователей
        users = django.contrib.auth.models.User.objects

        # Исключаем из рассмотрения редактируемого пользователя если форма редактирования
        if self.instance:
            users = users.exclude(id=self.instance.id)

        # Если находим юзера с таким емейлом в БД - это ошибка
        if users.filter(email=email).count():
            raise forms.ValidationError(u'Адрес эл. почты должен быть уникальным, пользователь с таким адресом уже есть.')

        # Результат если ОК
        return email

    # Логин делаем равный емейлу (у юзера джанги логин обязателен иначе бы
    # пришлось писать свою модельку).
    def save(self, commit = True):

        m = super(GgUserForm, self).save(False)

        # Логин = email'у
        m.username = self.cleaned_data['email']

        # Сохраняем
        if commit:
            m.save()

        return m


# Редактирование и создание Участников
class GgMemberForm(forms.ModelForm):
    class Meta:
        model = models.Member


# Редактирование и создание Группы
class GgGroupForm(forms.ModelForm):
    class Meta:
        model = models.Group


    def __init__(self, *args, **kwargs):
        super(GgGroupForm, self).__init__(*args, **kwargs)

        if 'data' in kwargs:
            data = kwargs['data']

            # Если вид местра встречи задан
            if 'place_type' in data:
                if data['place_type'] == models.Group.PLACE_TYPE_SHIP:
                    self.fields['ship'].required = True
                if data['place_type'] == models.Group.PLACE_TYPE_HOTEL:
                    self.fields['hotel'].required = True
                if data['place_type'] == models.Group.PLACE_TYPE_OTHER:
                    self.fields['other_place'].required = True



# Отличие от стандартной django authenticate в том что
# 1. использует плейн-пассворд.
class GGuruAuthenticationForm(django.contrib.auth.forms.AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                user = django.contrib.auth.models.User.objects.get(username = username, password = password)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                self.user_cache = user
            except django.contrib.auth.models.User.DoesNotExist:
                raise forms.ValidationError( self.error_messages['invalid_login'] % { 'username': 'username' })
        return self.cleaned_data


# Вызывается чтобы залогинить юзера
# Задает HTML для страницы и форму для авторизации через plain-пассворд
@csrf_exempt
def login(request):
    import django.contrib.auth.views
    return django.contrib.auth.views.login(
        request,
        template_name = 'login.html',
        authentication_form = GGuruAuthenticationForm
    )


# Выход юзера
def logout(request):
    from django.core.urlresolvers import reverse
    import django.contrib.auth.views
    return django.contrib.auth.views.logout(request, next_page = reverse('gguru.views.main'))


@fw.login_required
@fw.render_html('main.html')
def main(request):
    return {}


# В клиенте удобнее когда не тюпл а id и text поля словаря. Преобразует.
def choicesTupleToIdAndTextDict(choicesTuple):
    return [dict(id = c[0], text = c[1]) for c in choicesTuple]

def _groups_item_common():
    return {
        'placeTypeChoices': choicesTupleToIdAndTextDict(models.Group.PLACE_TYPE_CHOICES),
        'shipChoices': choicesTupleToIdAndTextDict(models.Group.SHIP_CHOICES),
    }

@fw.login_required
@fw.render_html('groups.html')
def groups(request):
    return {
        'groups': gg_json.ggJsonPy(models.Group.objects.all(), gg_json.makeJSONEncoderGroupListing())
    }

@fw.login_required
@fw.render_html('groups_item.html')
def groups_add(request):
    res = {
        'pageType': 'add',
        'modelName': u'группу',
    }
    res.update(_groups_item_common())
    return res

@fw.login_required
@fw.render_html('groups_item.html')
def groups_edit(request, id):
    res = {
        'pageType': 'edit',
        'modelName': u'группу',
        'model': gg_json.ggJsonPy(models.Group.objects.get(id = id), gg_json.makeJSONEncoderGroupCard()),
    }
    res.update(_groups_item_common())
    return res

@csrf_exempt
@fw.login_required
def groups_cud_ajax(request):
    return cud_operations.executeCUDOperationOnModel(GgGroupForm.Meta.model, GgGroupForm, request)



@fw.login_required
@fw.render_html('members.html')
def members(request):
    return {
        'members': gg_json.ggJsonPy(models.Member.objects.all(), gg_json.makeJSONEncoderMemberListing())
    }

def _members_item_common():
    return {
        'groups': gg_json.ggJsonPy(models.Group.objects.all(), gg_json.makeJSONEncoderGroupListing())
    }

@fw.login_required
@fw.render_html('members_item.html')
def members_add(request):
    res = {
        'pageType': 'add',
        'modelName': u'участника',
    }
    res.update(_members_item_common())
    return res

@fw.login_required
@fw.render_html('members_item.html')
def members_edit(request, id):
    res = {
        'pageType': 'edit',
        'modelName': u'участника',
        'model': gg_json.ggJsonPy(models.Member.objects.get(id = id), gg_json.makeJSONEncoderMemberCard()),
    }
    res.update(_members_item_common())
    return res

@csrf_exempt
@fw.login_required
def members_cud_ajax(request):
    return cud_operations.executeCUDOperationOnModel(GgMemberForm.Meta.model, GgMemberForm, request)

@fw.login_required
@fw.render_html('users.html')
def users(request):
    return {
        'users': gg_json.ggJsonPy(django.contrib.auth.models.User.objects.all(), gg_json.makeJSONEncoderUserListing())
    }

@fw.login_required
@fw.render_html('users_item.html')
def users_add(request):
    return {
        'pageType': 'add',
        'modelName': u'пользователя',
    }

@fw.login_required
@fw.render_html('users_item.html')
def users_edit(request, id):
    return {
        'model': gg_json.ggJsonPy(django.contrib.auth.models.User.objects.get(id = id), gg_json.makeJSONEncoderUserCard()),
        'pageType': 'edit',
        'modelName': u'пользователя',
    }

@csrf_exempt
@fw.login_required
def users_cud_ajax(request):
    return cud_operations.executeCUDOperationOnModel(GgUserForm.Meta.model, GgUserForm, request)
