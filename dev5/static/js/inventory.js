var contextMenu = {};
var inventoryObject = {};

 $('#inventory').jstree({
'plugins' : ['contextmenu', 'dnd'],
'contextmenu': {
    'items': 
        function (obj) {
            return contextMenu;
        }
},
'core' : {
  'check_callback' : true,
  'data' : {
    'url' : function (node) {
      return node.id === '#' ?
        'inventory/ajax_roots' :
        'ajax_children';
    },
    'data' : function (node) {
      return { 'objuuid' : node.id };
    },
    'dataType' : "json",
  },
'themes': {
        'theme': 'apple',
        'dots' : true,
        'icons': true,
        'url': "css/style.min.css"
    }
}
});

$('#inventory').on('select_node.jstree', function (evt, data) {
        contextMenu = {};
        
        $.ajax({
            'url' : 'inventory/ajax_context',
            'dataType' : 'json',
            'data' : {
                'objuuid' : data.node.id
            },
            'success' : function(resp) {
                for(var item in resp) {
                    contextMenu[item] = {
                        'label' : resp[item]['label'],
                        'route' : resp[item]['action']['route'],
                        'params' : resp[item]['action']['params'],
                        'method' : resp[item]['action']['method'],
                        'action' : function (obj) {
                            $.ajax({
                                'url' : obj.item.route,
                                'dataType' : 'json',
                                'data' : obj.item.params,
                                'success' : function(resp) {
                                    if(obj.item.method == 'ajax') {
                                        addMessage("console select success " + resp);
                                        $('#inventory').jstree('refresh'); 
                                    } else if(obj.item.method == 'edit task') {
                                        addMessage("edit task success");
                                        inventoryObject = resp;
                                        editTask();
                                    } else if(obj.item.method == 'edit container') {
                                        addMessage("edit container success");
                                        inventoryObject = resp;
                                        editContainer();
                                    } else if(obj.item.method == 'edit procedure description') {
                                        addMessage("edit procedure success");
                                        inventoryObject = resp;
                                        editProcedureDescription();
                                    } else if(obj.item.method == 'edit procedure tasks') {
                                        addMessage("edit procedure success");
                                        inventoryObject = resp;
                                        editProcedureTasks();
                                    }
                                },
                                'error' : function(resp, status, error) {
                                    addMessage("console select failure " + resp);
                                }
                            });
                        }
                    }
                }
            },
            'error' : function(resp, status, error) {
                addMessage("context failure " + resp);
            }
        });
    }
);

$('#inventory').on("move_node.jstree", function(event, data){
        $.ajax({
            'url' : 'inventory/ajax_move',
            'dataType' : 'json',
            'data' : {
                'objuuid' : data.node.id,
                'parent_objuuid' : data.node.parent
            },
            'success' : function(resp) {
                addMessage("move success " + resp);
                $('#inventory').jstree('refresh');
            },
            'error' : function(resp, status, error) {
                addMessage("move failure " + resp);
                $('#inventory').jstree('refresh');
            }
        });
});

var editTask = function() {
    document.getElementById('body').innerHTML = '<div id="aceInstance"></div>';
    
    document.getElementById('attributes').innerHTML = 'Task Name: <input type="text" id="taskName" onchange="setInventoryKey(&quot;name&quot;, &quot;taskName&quot;)"></input>';
    document.getElementById('taskName').value = inventoryObject['name'];

    var editor = new ace.edit(document.getElementById('aceInstance'));
    
    editor.setTheme("ace/theme/twilight");
    editor.session.setMode("ace/mode/python");
    editor.setValue(inventoryObject['body']);
    editor.selection.moveTo(0, 0);
    editor['inventoryObject'] = inventoryObject;
                                        
    editor.on('change', function(e, f) {
        f.inventoryObject['body'] = f.getValue();
        f.inventoryObject['changed'] = true;
    });
}

var editContainer = function() {
    document.getElementById('body').innerHTML = '';
    document.getElementById('attributes').innerHTML = 'Container Name: <input type="text" id="containerName" onchange="setInventoryKey(&quot;name&quot;, &quot;containerName&quot;)"></input>';
    document.getElementById('containerName').value = inventoryObject['name'];
}

var editProcedureDescription = function() {
    document.getElementById('body').innerHTML = '<div id="aceInstance"></div>';
    var editor = new ace.edit(document.getElementById('aceInstance'));
    
    editor.setTheme("ace/theme/twilight");
    editor.session.setMode("ace/mode/text");
    editor.setValue(inventoryObject['description']);
    editor.selection.moveTo(0, 0);
    editor['inventoryObject'] = inventoryObject;
                                        
    editor.on('change', function(e, f) {
        f.inventoryObject['description'] = f.getValue();
        f.inventoryObject['changed'] = true;
    });
    
    document.getElementById('attributes').innerHTML = '';
    $.ajax({
        'url' : 'procedure/attributes',
        'data' : {
            'name' : inventoryObject['name'],
            'title' : inventoryObject['title'],
            'objuuid' : inventoryObject['objuuid']
        },
        'success' : function(resp) {
            document.getElementById('attributes').innerHTML = resp;
        },
        'error' : function(resp, status, error) {
            document.getElementById('attributes').innerHTML = '';
        }
    });
}



var createTaskTableRow = function (rowIndex) {
    var taskTable = document.getElementById("taskTable");
    var row;
    var cell;
    
    row = taskTable.insertRow(rowIndex + 1);
    cell = row.insertCell(-1);
    cell.innerHTML = rowIndex;
    
    cell = row.insertCell(-1);
    cell.innerHTML = '<img src="images/plus_icon.png" onclick="insertProcedureTask(' + rowIndex + ')" />';
    
    cell = row.insertCell(-1);
    cell.innerHTML = '<img src="images/x_icon.png" onclick="deleteProcedureTask(' + rowIndex + ')" />';
    
    cell = row.insertCell(-1);
    cell.innerHTML = '<img src="images/up_icon.png"/>';
    
    cell = row.insertCell(-1);
    cell.innerHTML = '<img src="images/down_icon.png"/>';
    
    cell = row.insertCell(-1);
    cell.innerHTML = '<img src="images/paste_icon.png"/>';
}

var populateTaskTable = function() {
    document.getElementById('body').innerHTML = '<div id="taskTableContainer"><table id="taskTable"></table></div>';
    
    var taskTable = document.getElementById("taskTable");
    var row;
    var cell;
    
    row = taskTable.insertRow(rowIndex);
    cell = row.insertCell(-1);
    cell.innerHTML = '<b>Row</b>';
    
    cell = row.insertCell(-1);
    cell.innerHTML = '<b>Insert</b>';
    
    cell = row.insertCell(-1);
    cell.innerHTML = '<b>Delete</b>';
    
    cell = row.insertCell(-1);
    cell.innerHTML = '<b>Move Up</b>';
    
    cell = row.insertCell(-1);
    cell.innerHTML = '<b>Move Down</b>';
    
    cell = row.insertCell(-1);
    cell.innerHTML = '<b>Paste</b>';
    
    for(var rowIndex = 0; rowIndex < inventoryObject['tasks'].length; rowIndex++) {
        createTaskTableRow(rowIndex);
    }
}

var insertProcedureTask = function(rowIndex) {
    inventoryObject['tasks'].splice(rowIndex, 0, null);
    inventoryObject['changed'] = true;
    populateTaskTable();
}

var deleteProcedureTask = function(rowIndex) {
    inventoryObject['tasks'].splice(rowIndex, 1);
    inventoryObject['changed'] = true;
    populateTaskTable();
}

var editProcedureTasks = function() {
    if(inventoryObject['tasks'].length == 0) {
        inventoryObject['tasks'].push(null);
        inventoryObject['changed'] = true;
    }
    
    populateTaskTable();
    
    document.getElementById('attributes').innerHTML = '';
    $.ajax({
        'url' : 'procedure/attributes',
        'data' : {
            'name' : inventoryObject['name'],
            'title' : inventoryObject['title'],
            'objuuid' : inventoryObject['objuuid']
        },
        'success' : function(resp) {
            document.getElementById('attributes').innerHTML = resp;
        },
        'error' : function(resp, status, error) {
            document.getElementById('attributes').innerHTML = '';
        }
    });
}




var inventoryApp = angular.module('inventoryApp', []);
inventoryApp.controller('inventoryCtrl', function($scope, $interval, $http, $sce) {
    $interval(function () {
        if(inventoryObject['changed']) {
            $http.post('inventory/ajax_post_object', JSON.stringify(inventoryObject)
            ).then(function successCallback(response) {
                addMessage("saving " + inventoryObject['objuuid']);
                inventoryObject['changed'] = false;
                
                if(inventoryObject['refreshTree']) {
                    $('#inventory').jstree('refresh');
                    inventoryObject['refreshTree'] = false;
                }
            });
        }
        
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

var addMessage = function (message) {
    $.ajax({
        'url' : 'messaging/ajax_add_message',
        'dataType' : 'json',
        'data' : {
            'message' : message
        },
    });
};

var setInventoryKey = function (key, div) {
    inventoryObject[key] = document.getElementById(div).value;
    inventoryObject['changed'] = true;
    
    if(key == 'name') {
        inventoryObject['refreshTree'] = true;
    }
}