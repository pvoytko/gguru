// Настройки ангулар
var app = angular.module('myNgApp', []);

// Для Angular меняем две фигурные скобки на скобку и бакс (чтоб с шаблонами джанги различаться)
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

// Отключаем SCE (иначе ответ от сервера в виде HTLM при сохранении диалогов - не работает)
app.config(['$sceProvider', function($sceProvider) {
    $sceProvider.enabled(false);
}]);