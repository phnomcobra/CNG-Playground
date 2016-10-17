var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $interval, $http) {
    $interval(function () {
            $http.get("getrandom").then(function (response) {
            $scope.theRandomNumber = response.data;
        });
    }, 1000);
});