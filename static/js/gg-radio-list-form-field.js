/*
* Директива ангулар.
* */

var app = angular.module('myNgApp');

app.directive('ggRadioListFormField', function() {
    return {
        restrict: 'E',
        replace: true,
        scope: {
            model: '=',
            label: '@',
            items: '='
        },
        template: '' +
            '<div class="form-group">' +
                '<label class="col-lg-2 control-label" style="text-align: left;">{$ label $}</label>' +
                '<div class="col-lg-8">' +
                    '<div ng-repeat="i in items" class="radio">' +
                        '<label>' +
                            '<input type="radio" value="{$i.id$}" ng-model="$parent.model" selected="$parent.model == $i.id">{$i.text$}' +
                        '</label>' +
                    '</div>' +
                '</div>' +
            '</div>' +
            ''
    };
});




