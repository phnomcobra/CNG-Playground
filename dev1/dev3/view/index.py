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
    <title>DEV3 Index</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="css/index.css">
    <script src="js/angular.min.js"></script>
    <script src="js/ace/src-min-noconflict/ace.js" type="text/javascript" charset="utf-8"></script>
<body>
</head>
<body>
    <div id="editor">
        <div id="panelin"></div>
        <div id="panelout"></div>
    </div>
    <div ng-app="myApp" ng-controller="myCtrl"></div>
    <script src="js/index.js"></script>
</body>
</html>"""