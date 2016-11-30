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
    <meta charset="UTF-8">
    <link rel="stylesheet" href="css/index.css" />
    <link rel="stylesheet" href="css/style.min.css" />
    <link rel="stylesheet" href="css/jquery-ui.css">
    <link rel="stylesheet" href="css/jsgrid.min.css">
    <link rel="stylesheet" href="css/jsgrid-theme.min.css">
    <script src="js/jquery.js"></script>
    <script src="js/jquery-ui.js"></script>
    <script src="js/jsgrid.js"></script>
    <script src="js/jstree.min.js"></script>
    <script src="js/angular.min.js"></script>
    <script src="js/ace/src-min-noconflict/ace.js"></script>
    <script src="js/procedure.js"></script>
    <script src="js/task.js"></script>
    <script src="js/rfc.js"></script>
    <script src="js/container.js"></script>
    <script src="js/status.js"></script>
    <script src="js/jscolor.js"></script>
    <script src="js/host.js"></script>
    <script src="js/controller.js"></script>
    <script src="js/menubar.js"></script>
    <script src="js/console.js"></script>
</head>
<body>
    <div id="jqmpage">
        <header id="opsact">
            <div id="menuBarStaticLeft">
                <div class="menuBarItem">Back</div>
                <div class="menuBarItem">Forward</div>
                <div class="menuBarItem">Export</div>
                <div class="menuBarItem">Import</div>
                <div class="menuBarItem" onclick="setCredentials()">Set Credentials</div>
            </div>
            <div id="menuBarDynamic"></div>
            <div id="menuBarStaticRight">
                <div class="menuBarItem" onclick="setCredentials()">SSH:Null SQL:Null</div>
            </div>
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
    <div id="modal-content">
        <div id="modal-header"></div>
        <div id="modal-body"></div>
        <div id="modal-footer"></div>
    </div>
    <script src="js/inventory.js"></script>    
</body>

</html>"""