/*
* Директива ангулар.
* Создает бутстрап верстку для простого текстового поля для формы.
* Пример использования
*   <gg-text-input-form-field model="model.field" label="Подпись к полю" size="5">
* Создат поле ввода с размером 5 (bootstrap grid size) и свяжет через ng-model с model.fiedl.
* Подпись label.
* */

var app = angular.module('myNgApp');

app.directive('ggTextInputFormField', function() {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        scope: {
            model: '=model',
            label: '@label',
            size: '@size'
        },
        template: '' +
            '<div class="form-group">' +
                '<label class="col-lg-2 control-label" style="text-align: left;">{$ label $}</label>' +
                '<div class="col-lg-{$ size $}">' +
                    '<input type="text" class="form-control" ng-model="model">' +
                '</div>' +
            '</div>' +
            ''
    };
});




