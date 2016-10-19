#!/usr/bin/python
################################################################################
# VIEW
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/16/2016 Original construction
################################################################################

import cherrypy

def index_view():
    return """<!doctype html>
<html>
<head>
    <title>DEV2 Index</title>
    <meta charset="UTF-8">
    <script src="js/angular.min.js"></script>
    <script src="js/index.js"></script>
<body>
</head>
<body>
    <div ng-app="myApp" ng-controller="myCtrl">
        <textarea rows="25" cols="80" ng-model="textarea"></textarea>
    </div>
</body>
</html>"""