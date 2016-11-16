var contextMenu = {};
var inventoryObject = {};
var saving = false;

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

$(document).on('dnd_stop.vakata', function (e, data) {
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : data.data.nodes[0]},
        'success' : function(resp) {
            if(resp['type'] == 'task' && 
               document.getElementById("taskTable") &&
               inventoryObject['type'] == 'procedure') {
                inventoryObject['tasks'].push(resp['objuuid']);
                inventoryObject['changed'] = true;
                populateTaskTable();
            }
        },
        'error' : function(resp, status, error) {
        }
    });
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

var createTaskTableRow = function (rowIndex, objuuid) {
    var taskTable = document.getElementById("taskTable");
    var taskRow;
    var taskCell;
    
    taskRow = taskTable.insertRow(rowIndex);
    
    taskCell = taskRow.insertCell(-1);
    taskCell.innerHTML = rowIndex;
    
    taskCell = taskRow.insertCell(-1);
    taskCell.innerHTML = '<table></table>';
    
    var tileRow;
    var tileCell;
    var tileTable = taskCell.childNodes[0];
    
    tileRow = tileTable.insertRow(-1);
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<img src="images/up_icon.png" onclick="moveUpProcedureTask(' + rowIndex + ')" />';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<img src="images/edit_icon.png" onclick="loadAndEditTask(&quot;' + objuuid + '&quot;)" />';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<div name="name-' + objuuid + '"><img src="images/throbber.gif"/></div>';
    
    tileRow = tileTable.insertRow(-1);
    
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<img src="images/down_icon.png" onclick="moveDownProcedureTask(' + rowIndex + ')" />';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<img src="images/x_icon.png" onclick="deleteProcedureTask(' + rowIndex + ')" />';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = objuuid;
    
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            var elements = document.getElementsByName('name-' + objuuid);
            for(var element in elements) {elements[element].innerHTML = resp['name'];}
        }
    });
}

var loadAndEditTask = function(objuuid) {
    document.getElementById('body').innerHTML = '';
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            inventoryObject = resp;
            editTask();
        }
    });
}

var populateTaskTable = function() {
    document.getElementById('body').innerHTML = '<table id="taskTable"></table>';
    
    for(var rowIndex = 0; rowIndex < inventoryObject['tasks'].length; rowIndex++) {
        createTaskTableRow(rowIndex, inventoryObject['tasks'][rowIndex]);
    }
}

var deleteProcedureTask = function(rowIndex) {
    inventoryObject['tasks'].splice(rowIndex, 1);
    inventoryObject['changed'] = true;
    populateTaskTable();
}

var moveUpProcedureTask = function(rowIndex) {
    if(rowIndex > 0) {
        inventoryObject['tasks'][rowIndex] = inventoryObject['tasks'].splice(rowIndex - 1, 1, inventoryObject['tasks'][rowIndex])[0];
        inventoryObject['changed'] = true;
        populateTaskTable();
    }
}

var moveDownProcedureTask = function(rowIndex) {
    if(rowIndex < inventoryObject['tasks'].length - 1) {
        inventoryObject['tasks'][rowIndex] = inventoryObject['tasks'].splice(rowIndex + 1, 1, inventoryObject['tasks'][rowIndex])[0];
        inventoryObject['changed'] = true;
        populateTaskTable();
    }
}

var editProcedureTasks = function() {
    
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
        if(inventoryObject['changed'] && !saving) {
            saving = true;
            $http.post('inventory/ajax_post_object', JSON.stringify(inventoryObject)
            ).then(function successCallback(response) {
                addMessage("saving " + inventoryObject['objuuid']);
                saving = false;
                inventoryObject['changed'] = false;
                
                if(inventoryObject['refreshTree']) {
                    $('#inventory').jstree('refresh');
                    inventoryObject['refreshTree'] = false;
                }
            }, function errorCallback(response) {
                addMessage("save failure " + inventoryObject['objuuid']);
                saving = false;
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