/*
* Директива ангулар.
* Рендерится в кнопки: "Добавить", "Изменить", "Удалить".
* Используется под формой редактирования / добавления модели.
* Этот же компонент посылает запрос на сервер с данными модели.
* И отображает ответ от сервера.
* Пример использования
*     <gg-model-operations mode="add" model="model" operation-url="/server/rest_api/" success-url="/list/" />
* Тогда отправляться будет model на /server/rest_api/ и в случае успеха редирект на /list/
* mode=add - добавляется только 1 кнопка CREATE
* mode=edit - добавляется 2 пноки - редактировать и удалить.
* */

var app = angular.module('myNgApp');

app.directive('ggModelOperations',function() {
    return {
        restrict: 'E',
        replace: true,
        scope: true,
        template:
            '<div><div ng-show="statusMessage != undefined" ng-cloak>' +
                '<div class="alert" ng-class="{\'alert-info\': statusMessage == true, \'alert-danger\': statusMessage.length != undefined}">' +
                    '<span ng-show="statusMessage == true">Происходит сохранение на сервер, пожалуйста, подождите...</span>' +
                    '<span ng-show="statusMessage.length != undefined" ng-bind-html="statusMessage"></span>' +
                '</div>' +
            '</div>' +
            '<div class="form-group" ng-show="mode==\'add\'">' +
                '<div class="col-lg-offset-2 col-lg-9">' +
                    '<button ng-click="sendForm(\'CREATE\')" class="btn btn-primary">Добавить</button>' +
                '</div>' +
            '</div>' +
            '<div class="form-group" ng-show="mode==\'edit\'">' +
                '<div class="col-lg-offset-2 col-lg-4">' +
                    '<button ng-click="sendForm(\'UPDATE\')" class="btn btn-primary">Изменить</button>' +
                    '<button ng-click="sendForm(\'DELETE\')" class="btn btn-danger pull-right">Удалить</button>' +
                '</div>' +
            '</div></div>',
        link: function($scope, element, attrs) {

            // mode = 'edit' - показываем 2 кнопки - изменить и удалить
            // mode = 'add' - показываем 1 кнопку - добавить
            $scope.mode=attrs['mode'];

            // Сообщение об ошибке - очищаем
            // undefined - ничего не показываем
            // true - показываем что идет сохранение на сервер...
            // текст - значит показываем красным этот текст ошибки.
            $scope.statusMessage = undefined;

            // Установка $scope.statusMessage с обновлением скоупа (вызывается не из ангулар а из внешних событий).
            $scope._asyncSetStatusMessage = function(newValue){
                $scope.$apply(function($scope){
                    $scope.statusMessage = newValue;
                });
            };


            // Отправка формы
            // type = CREATE или UPDATE или DELETE
            // вызывается по нажатию на соотв. кнопки внизу формы редактирования.
            $scope.sendForm = function(type){

                $scope.statusMessage = true;

                // Шлем данные на сервер и операция CREATE
                // Шлем именно через jQuery ajax а не angular $http
                // Так как через $http почему-то на сервере пост не содержит данные
                // и CSRF проверка не проходит. Видимо, как-то по-другому надо отсылать через $http
                // чем через jQuery. Не стал разбираться как а заюзал jQuery.
                $.ajax({
                    url: attrs['operationsUrl'],
                    method: 'POST',
                    data: {
                        operation: type,
                        data: JSON.stringify($scope.$eval(attrs['model']))
                    }

                // Сервер ответил с кодом HTTP 200 (ОК)
                }).success(function(result) {

                    // Если поле status_ok не True (полученные данные некорректны)
                    // Важно проверка именно ==, т.к. код ответа может быть 302 (требуется авторизация)
                    // и тогда поля status_ok не будет т.е. оно будет undefined и !status_ok дала бы true
                    // а !== false даст false
                    if (result.status_ok == false) {

                        var m = "";
                        for (var i=0; i<result.response.length; ++i){
                            m += result.response[i][0] + " = " + result.response[i][1] + "<br />";
                        }

                        // Показать текст ошибки
                        $scope._asyncSetStatusMessage('Ошибка при сохранении данных.<br />' + m);
                    }

                    // Иначе - данные корректны, операция выполнена
                    else if (result.status_ok == true) {

                        // Тут мы специально оставляем показываться сообщение "Загрузка с сервера"
                        // Потому что редирект может делаться несколько секунд.
                        // $scope._asyncSetStatusMessage(undefined);

                        // Делаем редирект
                        // на ту страницу с которой пришли если она на том же хосте
                        // (редирект на ту с которой пришли надо для того что при заходе в редактирование из
                        // листинга например со страницы 5 чтобы обратно мы возвращались на эту же страницу
                        // 5 листинга) а если хост другой (зашли на редактирование например с другого сайта) -
                        // то заходим на дефолтову страницу листинга.
                        defUrl = attrs['successUrl'];
                        refUrl = document.referrer;
                        window.location = (refUrl[2] == defUrl[2]) ? defUrl : refUrl;
                    }
                    else {
                        // Показать текст ошибки
                        $scope._asyncSetStatusMessage('Ошибка на сервере при сохранении данных. Обратитесь в службу поддержки.');
                    }

                // Код HTTP отличный от 200 (отпало соединнеие или Internal Server Error)
                // Показать текст ошибки
                // Когда инет отпал тупо недоступен то exc приходит пустой строкой
                // Чтобы не смущать пользователя в этом случае - пишем текст что нет соединения.
                }).error( function(obj, text, exc) {
                    $scope._asyncSetStatusMessage(exc ? exc : 'Отсутствует соединение с сервером.');
                });
            };

        }
    };
});




