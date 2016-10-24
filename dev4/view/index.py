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
    <title>DEV4 Index</title>
    <meta charset="UTF-8">
    <script src="js/angular.min.js"></script>
    <link rel="stylesheet" href="css/style.min.css" />
    <script src="js/jquery.js"></script>
    <script src="js/jstree.min.js"></script>
<body>
</head>
<body>
    <div ng-app="myApp" ng-controller="myCtrl"></div>
    <div id="demotree"></div>
    <script src="js/index.js"></script>
</body>
</html>"""