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
</head>
<body>
    <div id="jqmpage" data-role="page">
        <div id="opsact" data-role="header" data-position="fixed">
            <p>Operations Action Ribbon</p>
        </div>
        <div id="ops" data-role="main" class="ui-content">
            <div class="tblrow">
                <div class="tblcell">
                    <div class="tbl">
                        <div class="tblrow">
                            <div id="inventory" class="tblcell"></div>
                        </div>
                        <div class="tblrow">
                            <div id="attributes" class="tblcell"></div>
                        </div>
                    </div>
                </div>
                <div class="tblcell" id="body"></div>
            </div>
        </div>
        <div id="messages" data-role="footer" data-position="fixed">
            <div ng-app="inventoryApp" ng-controller="inventoryCtrl">
            <div ng-bind-html="messages"></div>
        </div>
    </div>
    <script src="js/inventory.js"></script>    
</body>

</html>"""