var editorin = ace.edit("panelin");
editorin.setTheme("ace/theme/twilight");
editorin.session.setMode("ace/mode/python");

var editorout = ace.edit("panelout");
editorout.setTheme("ace/theme/twilight");
editorout.session.setMode("ace/mode/python");

var app = angular.module('myApp', []);
app.controller('myCtrl', function($interval, $http) {
    $interval(function () {
            $http.post("textarea", editorin.getValue());
            $http.get("gettextarea").then(function (response) {
                editorout.setValue(response.data);
                editorout.selection.moveTo(0, 0);
            });
    }, 1000);
});
