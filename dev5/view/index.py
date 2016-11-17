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

def index_view():
    return """<!doctype html>
<html>
<head>
    <title>DEV5 Index</title>
    <meta charset="UTF-8" name="viewport" content="width=device-width, height=device-height, initial-scale=1">
    <link rel="stylesheet" href="css/index.css" />
    <link rel="stylesheet" href="css/style.min.css" />
    <link rel="stylesheet" href="css/jquery-ui.css">
    <script src="js/jquery.js"></script>
    <script src="js/jquery-ui.js"></script>
    <script src="js/jstree.min.js"></script>
    <script src="js/angular.min.js"></script>
    <script src="js/ace/src-min-noconflict/ace.js" type="text/javascript" charset="utf-8"></script>
    <script src="js/procedure.js"></script>
    <script src="js/task.js"></script>
    <script src="js/rfc.js"></script>
    <script src="js/container.js"></script>
</head>
<body>
    <div id="jqmpage">
        <header id="opsact">
            <p>Operations Action Ribbon</p>
        </header>
        <nav>
            <div id="inventory"></div>
            <div id="attributes"></div>
        </nav>
        <article id="body"></article>
        <footer>
            <div ng-app="inventoryApp" ng-controller="inventoryCtrl">
                <div ng-bind-html="messages"></div>
            </div>
        </footer>
    </div>
    <script src="js/inventory.js"></script>    
</body>

</html>"""