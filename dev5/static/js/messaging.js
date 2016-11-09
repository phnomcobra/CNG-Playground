var addMessage = function (message) {
    $.ajax({
            'url' : 'messaging/ajax_add_message',
            'dataType' : 'json',
            'data' : {
                'message' : message
            },
        });
};

var messageingApp = angular.module('messagingApp', []);
messageingApp.controller('messagingCtrl', function($scope, $interval, $http, $sce) {
    $interval(function () {
            $http.get("messaging/ajax_get_messages").then(function (response) {
            
            var messageData = '<code><table>';
            var responseJSON = angular.fromJson(response)['data']['messages'];
            for(item in responseJSON) {
                messageData += '<tr><td>' + responseJSON[item]['timestamp'] + '</td><td>' + responseJSON[item]['message'] + '</td></tr>';
            }
            messageData += '</table></code>'
            
            $scope.messages = $sce.trustAsHtml(messageData);
        });
    }, 1000);
});