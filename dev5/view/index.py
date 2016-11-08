#!/usr/bin/python
################################################################################
# VIEW
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 10/25/2016 Original construction
################################################################################

import cherrypy

def index_view():
    return """<!doctype html>
<html>
<head>
    <title>DEV5 Index</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="css/index.css" />
    <link rel="stylesheet" href="css/style.min.css" />
    <script src="js/jquery.js"></script>
    <script src="js/jquery-ui.js"></script>
    <script src="js/jstree.min.js"></script>
    <script src="js/angular.min.js"></script>
    <script src="js/messaging.js"></script>
    <script src="js/ace/src-min-noconflict/ace.js" type="text/javascript" charset="utf-8"></script>
</head>
<body>
    <div id="ops">
        <div id="opsact">
            <p>Operations Action Ribbon</p>
        </div>
        <div id="container">
            <div id="inventory">
                <p>Inventory</p>
            </div>
            <div id="tabs">
                <div id="handles">
                    <p>Handles</p>
                </div>
                <div id="bodies">
                    <p>Bodies</p>
                </div>
            </div>
        </div>
        <div id="messages">
            <div ng-app="messagingApp" ng-controller="messagingCtrl">
                <div ng-bind-html="messages"></div>
            </div>
        </div>
    </div>
    <script src="js/inventory.js"></script>
</body>

</html>"""