# -*- coding: utf-8 -*-

import simplejson
import datetime
import django.db.models
import django.db.models.fields.files
import models



# Преобразует QuerySet к списку словарей для передачи на клиент
# Отличие в том что из кверисет поступают поля как они идут в БД (object_id)
# а когда мы берем через модель то ссылающиеся поля имеют другое имя (object)
# + возможность дополнительнрых свойств extraPropsList.
def modelQuerySetToListOfDictWithExtra(qs, extraPropsList):
    return [modelToDictWithExtra(o, extraPropsList) for o in qs]


# Получая на вход модель данная функция преобразует ее к словарю
# используя список полей в качестве ключей + значения свойств extraPropsList
# (именно этим и отличается от стандартной джанговской)
# используется чтобы передать на клиент не только поля базы, но и вычисляемые поля (проперти)
def modelToDictWithExtra(o, extraPropsList):
    from django.forms.models import model_to_dict
    res = model_to_dict(o, fields=[], exclude=[])
    for p in extraPropsList:
        res[p] = getattr(o, p)
    return res


# Аналог django.forms.models.model_to_dict
# За тем лишь исключением, что django model_to_dict не включает в результирующий
# словарь поле модели, объявленное так:
#     date_creation = models.DateField(auto_now_add=True)
# а наша версия функции - включает.
# в джанго почему-то стоит проверка
#        if not f.editable:
#            continue
# которая пропускает поле объявленное таким образом...
#
# fields - какие поля включить в выдачу (пустой - то все)
# exclude - какие поля исключить из выдачи (пустой - то никакие)
# rules - словарь, для каких полей какие правила (правила не заданы - тогда дефолтовое)
def gg_model_to_dict(instance, fields = [], exclude = [], extra=[], rules=[]):
    from django.db.models.fields.related import ManyToManyField
    opts = instance._meta
    data = {}

    # Проверка что использованы допустимые имена полей.
    # На случай переименования полей в модели - это нужная проверка.
    for f in fields + exclude:
        fnames = [f2.name for f2 in opts.fields] + [f3.name for f3 in opts.many_to_many]
        if f not in fnames:
            raise RuntimeError(u"Неизвестное название поля \"{0}\". Допустимые значения: \"{1}\"".format(f, '", "'.join(fnames)))

    for f in opts.fields + opts.many_to_many:
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue

        # Если задано правило - применяем его
        if f.name in rules:
            data[f.name] = rules[f.name](instance)
            continue

        # Если поле m2m
        if isinstance(f, ManyToManyField):
            # If the object doesn't have a primary key yet, just use an empty
            # list for its m2m fields. Calling f.value_from_object will raise
            # an exception.
            if instance.pk is None:
                data[f.name] = []
            else:
                # MultipleChoiceWidget needs a list of pks, not object instances.
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
            continue

        # Иначе
        data[f.name] = f.value_from_object(instance)
        continue

    # Дополнительные поля (для них обязательно должны быть правила)
    for f in extra:
        # Если тут ошибка KeyError значит забыли в rules добавить те поля что добавили в extra
        data[f] = rules[f](instance)

    return data


# В клиенте удобнее когда не тюпл а id и text поля словаря. Преобразует.
def choicesTupleToIdAndTextDict(choicesTuple):
    return [dict(id = c[0], text = c[1]) for c in choicesTuple]


# Цифровое значение преобразовывает к текстовому используя CHOICES_TUPLE
def choiceToText(id, choicesTuple):
    for c in choicesTuple:
        if c[0] == id:
            return c[1]
    raise RuntimeError(u'Некорректное значение {0}'.format(id))


# Передавая этой функции набор энкодеров можно сделать универсальный энкодер (который делает то что нам надо
# с помощью указанных энкодеров вызывая их по-очереди друг за другом).
def makeJSONEncoder(*handlers):

    class MakedJSONEncoder(simplejson.JSONEncoder):
        def default(self, o):

            for hObj in handlers:
                handler = hObj.getHandlerForValue(o)
                if handler:
                    return handler(o)

            return super(MakedJSONEncoder, self).default(o)

    return MakedJSONEncoder


# Делает дамп объекта в JSON.
# Отличие от стандартного json.dumps:
# Использует simplejson (из-за поддержки decimal)
# Форматирует indent4, использует юникод.
# Использует encoder который можно "наполнять" энкодировщиками.
# Юникодные строки дампит как строки а не как эскейп-коды.
# Поддерживает date
def ggJsonDumps(obj, cls = makeJSONEncoder()):
    return simplejson.dumps(
        obj,
        cls=cls,
        use_decimal=True,
        indent=4,
        ensure_ascii=False
    )


# Делает сначала json dump а потом json loads т.е. обратно в питон преобразует.
# Это нужно для того чтобы использовать JSON-энкодеры а на выходе иметь питон-объект
# Например для использования в джанго-шаблонах.
def ggJsonPy(obj, cls = makeJSONEncoder()):
    return simplejson.loads(ggJsonDumps(obj, cls))


# Сериализует Django QuerySet как list
class JSONEncoderDjangoQuerySetAsList(object):
    def getHandlerForValue(self, o):
        import django.db.models.query
        if isinstance(o, django.db.models.query.QuerySet):
            def handler(o):
                return list(o)
            return handler


# Сериализует Django Model как список полей
class JSONEncoderDjangoModelAsDict(object):

    def __init__(self, fields=[], exclude=[], extra=[], rules=[], type=None):
        self.fields = fields
        self.exclude = exclude
        self.extra = extra
        self.rules = rules
        self.type = type

    def getHandlerForValue(self, o):
        def handler(o):
            return gg_model_to_dict(o, fields=self.fields, exclude=self.exclude, extra=self.extra, rules=self.rules)
        if self.type:
            if isinstance(o, self.type):
                return handler
        elif isinstance(o, django.db.models.Model):
            return handler




class JSONEncoderTypeToDict(object):
    def __init__(self, fields=[], extra=[], rules=[], type=None):
        self.fields = fields
        self.extra = extra
        self.rules = rules
        self.type = type

    def getHandlerForValue(self, o):
        if isinstance(o, self.type):
            def handler(o):
                res = dict()
                for f in self.fields:
                    if f in self.rules:
                        res[f] = self.rules[f](o)
                    else:
                        res[f] = getattr(o, f)
                for f in self.extra:
                    res[f] = self.rules[f](o)
                return res
            return handler


# Сериализует Date Time как список isoformat
class JSONEncoderDateTimeToIso(object):
    def getHandlerForValue(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            def handler(o):
                return o.isoformat()
            return handler


# Получая CHOICES тюпл и значение в нем, возвращает соответствующее строковое значение из CHOICES.
def getChoicesTextByValue(choices, value):
    for c in choices:
        if c[0] == value:
            return c[1]
    raise RuntimeError('Значение {0} не найдено в списке возможных значений.'.format(value))


# QuerySet -> List
# Model -> Dict
def makeJSONDjangoEncoder():
    return makeJSONEncoder(
        JSONEncoderDjangoQuerySetAsList(),
        JSONEncoderDjangoModelAsDict()
    )


# Для листинга
def makeJSONEncoderUserListing():
    return makeJSONEncoder(
        JSONEncoderDjangoQuerySetAsList(),
        JSONEncoderDjangoModelAsDict(
            type=django.contrib.auth.models.User,
            fields=['id', 'email'],
        ),
    )

# Для карточки
def makeJSONEncoderUserCard():
    return makeJSONEncoder(
        JSONEncoderDjangoQuerySetAsList(),
        JSONEncoderDjangoModelAsDict(
            type=django.contrib.auth.models.User,
            fields=['id', 'email', 'password'],
        ),
    )

# Для листинга
def makeJSONEncoderMemberListing():
    return makeJSONEncoder(
        JSONEncoderDjangoQuerySetAsList(),
        JSONEncoderDjangoModelAsDict(
            type=models.Member,
            fields=[
                'id',
                'fio',
                'dr',
            ],
            extra=[
                'group_name',
            ],
            rules={
                'dr': lambda o: formatDate(o.dr),
                'group_name': lambda o: o.getGroupName(),
            }
        ),
        JSONEncoderDateTimeToIso()
    )

# Для карточки
def makeJSONEncoderMemberCard():
    return makeJSONEncoder(
        JSONEncoderDjangoQuerySetAsList(),
        JSONEncoderDjangoModelAsDict(
            type=models.Member,
        ),
        JSONEncoderDateTimeToIso()
    )

# Возврщает строку дат для недели года
# Пример: 14 янв
def formatDate(date):

    def monthStr(date):
        monthL = [u'янв', u'фев', u'мар', u'апр', u'май', u'июн', u'июл', u'авг', u'сен', u'окт', u'ноя', u'дек']
        return monthL[date.month-1]

    # Печатаем число
    year = divmod(date.year, 100)[1]
    str = unicode(date.day) + u" " + monthStr(date) + u" " + unicode(year)
    return str


# Для листинга
def makeJSONEncoderGroupListing():
    return makeJSONEncoder(
        JSONEncoderDjangoQuerySetAsList(),
        JSONEncoderDjangoModelAsDict(
            type=models.Group,
            fields=[
                'id',
                'req_number',
                'date_begin',
                'date_end',
            ],
            extra=[
                'place_descr'
            ],
            rules={
                'date_begin': lambda o: formatDate(o.date_begin),
                'date_end': lambda o: formatDate(o.date_end),
                'place_descr': lambda o: o.getPlaceDescr(),
            }
        ),
    )

# Для карточки
def makeJSONEncoderGroupCard():
    return makeJSONEncoder(
        JSONEncoderDjangoQuerySetAsList(),
        JSONEncoderDjangoModelAsDict(
            type=models.Group,
        ),
        JSONEncoderDateTimeToIso()
    )