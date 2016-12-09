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
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <!-- <link rel="stylesheet" href="css/bootstrap-theme.min.css"> -->
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
    <script src="js/bootstrap.min.js"></script>
    
</head>
<body>
    <div id="jqmpage">
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" 
            data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">valarie</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li><a href="#back">Back</a></li>
            <li><a href="#forward">Forward</a></li>
            <li><a href="#import">Import</a></li>
            <li><a href="#export">Export</a></li>
            <li><a href="#" data-toggle="modal" data-target="#credModal">
              Set Credentials</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right" id="menuBarDynamic">
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>
        <div id="left-nav">
            <div id="inventory"></div>
            <div id="attributes"></div>
        </div>
        <article id="body"></article>
        <footer>
            <div ng-app="inventoryApp" ng-controller="inventoryCtrl">
                <div ng-bind-html="messages"></div>
            </div>
        </footer>
    </div>
 
      <!-- modal -->
      <div class="modal fade" id="credModal" tabindex="-1" role="dialog" 
        aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
              <h4 class="modal-title" id="myModalLabel">Set Credentials</h4>
            </div>
            <div class="modal-body">
              <form class="form-horizontal">
                <div class="form-group">
                  <label class="control-label col-sm-3" for="ssh_id">SSH User:</label>
                  <div class="col-sm-9">
                    <input type="text" class="form-control" id="ssh_id"
                      placeholder="Enter ssh username">
                  </div>
                </div>
                <div class="form-group">
                  <label class="control-label col-sm-3" for="ssh_pwd">Password:</label>
                  <div class="col-sm-9"> 
                    <input type="password" class="form-control" id="ssh_pwd" 
                      placeholder="Enter ssh password">
                  </div>
                </div>
                <div class="form-group">
                  <label class="control-label col-sm-3" for="sql_id">MySQL User:</label>
                  <div class="col-sm-9">
                    <input type="text" class="form-control" id="sql_id" 
                      placeholder="Enter SQL username">
                  </div>
                </div>
                <div class="form-group">
                  <label class="control-label col-sm-3" for="pwd">Password:</label>
                  <div class="col-sm-9"> 
                    <input type="password" class="form-control" id="ssh_pwd" 
                      placeholder="Enter SQL password">
                  </div>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
              <button type="button" class="btn btn-primary" onclick="submitCredentials()" 
                data-dismiss="modal">Submit</button>
            </div>
          </div>
        </div>
      </div> <!-- End modal --> 

    <script src="js/inventory.js"></script>    
</body>

</html>"""