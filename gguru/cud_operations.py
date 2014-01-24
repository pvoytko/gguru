# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json



# Класс инкапсулирует в себе знание о том какой
# формат взаимодействия между сервером и клиентом (JS).
# А именно пока он такой:
# ответ содержит 2 поля - status_ok (булевый, True если операция выполнена и False если что-то случилось)
# и response который содержит доп. данные в обоих случаях или может быть пустой.
class JsonResponseBuilder():

    def __init__(self):
        self._responseObject = {
            'status_ok': True
        }

    def setError(self, errorResponseObject):
        self._responseObject['status_ok'] = False
        self._responseObject['response'] = errorResponseObject

    def setSuccess(self, successResponseObject):
        self._responseObject['status_ok'] = True
        self._responseObject['response'] = successResponseObject

    def buildHttpJsonResponse(self):
        return HttpResponse(json.dumps(self._responseObject), content_type="application/json")


class SuccessResponseMaker:
    def makeCreateResponse(self, model):
        return None
    def makeUpdateResponse(self, model):
        return None
    def makeDeleteResponse(self, model):
        return None


class SuccessResponseMakerModelId(SuccessResponseMaker):
    def makeCreateResponse(self, model):
        return dict(id = model.id)
    def makeUpdateResponse(self, model):
        return {}


# Реализует обработку запросов CREATE UPDATE DELETE полученых через AJAX делегируая вызовы к Django-модели.
# Решает 2 задачи:
# * получение данных о запрошенной операции из запросва
# * выполенение запрошенной операций на сервере для выполнени
# Параметризуя класс с помощью класса модели можно реализовать аля RESTful интерфейс для этой модели
# и валидировать его с помощью класса формы.
def executeCUDOperationOnModel(modelClassName, formClassName, request):
    return executeCUDOperationOnModel2(modelClassName, formClassName, SuccessResponseMakerModelId(), request)


# Вторая версия функции. Коммент см. к первой.
# Вторая версия отличается тем что позволяет параметризовать еще класс мейкера который используется
# для того чтобы имея сохраненную на сервере модель на ее основе сформировать ответ обратно на клиент от сервера.
# В первой версии функции всегда возвращался ОК и id, а при добавлении связанных моделей
# может быть необходимо возвращать еще и поля сохранной модели. Для реализации этого и нужен мейкер.
def executeCUDOperationOnModel2(modelClassName, formClassName, successResponseMakerObject, request):
    executer = CUDOperationsModelExecuter(modelClassName, formClassName, successResponseMakerObject)
    return executer.executeOperation(request)


class CUDOperationsModelExecuter:

    def __init__(self, modelClassName, formClassName, successResponseMakerObject):
        self._modelClassName = modelClassName
        self._formClassName = formClassName
        self._respBuilder = JsonResponseBuilder()
        self._successResponseMakerObject = successResponseMakerObject

    # Выполняет операцию по имени
    def executeOperation(self, request):

        # Тут используется всегда метод POST а не типы запросов PUT, DELETE так как для типов запросов PUT и DELETE
        # почему-то не проходит django-csrf проверка (возникает ошибка на сервере при отправке ajax-запроса)
        # для экономии времени разбираться не стал а просто использовал POST метод для всех операций.
        operation = request.POST['operation']
        userData = json.loads(request.POST['data'])

        # Выполняем операцию
        if operation == "CREATE":
            return self.executeCreate(userData)
        elif operation == "DELETE":
            return self.executeDelete(userData)
        elif operation == "UPDATE":
            return self.executeUpdate(userData)
        else:
            raise RuntimeError(u"Неподдерживаемая операция '{0}'".format(operation))


    def executeCreate(self, userData):

        # Делаем модэл-форму с полями на основе полученных данных
        fm = self._formClassName(data=userData)

        # Валидируем данные с помощью формы и модели
        # ОК = сохраняем в БД и готовим ответ
        if fm.is_valid():
            m = fm.save()
            respObj = self._successResponseMakerObject.makeCreateResponse(m)
            if respObj:
                self._respBuilder.setSuccess(respObj)

        # Ошбка - готовим ответ
        else:
            self._respBuilder.setError([i for i in fm.errors.items()])

        return self._respBuilder.buildHttpJsonResponse()


    def executeUpdate(self, userData):

        # Делаем модэл-форму с полями на основе полученных данных
        u = self._modelClassName.objects.get(id=userData['id'])
        fm = self._formClassName(instance=u, data=userData)

        # Валидируем данные с помощью формы и модели
        # ОК = сохраняем в БД и готовим ответ
        if fm.is_valid():
            m = fm.save()
            respObj = self._successResponseMakerObject.makeUpdateResponse(m)
            if respObj:
                self._respBuilder.setSuccess(respObj)

        # Ошбка - готовим ответ
        else:
            self._respBuilder.setError([i for i in fm.errors.items()])

        return self._respBuilder.buildHttpJsonResponse()


    def executeDelete(self, userData):
        delObj = self._modelClassName.objects.get(id=userData['id'])
        delObj.delete()
        respObj = self._successResponseMakerObject.makeDeleteResponse(delObj)
        if respObj:
            self._respBuilder.setSuccess(respObj)
        return self._respBuilder.buildHttpJsonResponse()

