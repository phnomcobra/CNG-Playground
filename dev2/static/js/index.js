var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $interval, $http) {
    $interval(function () {
            $http.post("textarea", $scope.textarea);
    }, 1000);
});
