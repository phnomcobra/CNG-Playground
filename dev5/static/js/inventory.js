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
    if(data.event.toElement.id == 'body') {
        $.ajax({
            'url' : 'inventory/ajax_get_object',
            'dataType' : 'json',
            'data' : {'objuuid' : data.data.nodes[0]},
            'success' : function(resp) {
                if(resp['type'] == 'task' && 
                   document.getElementById('taskTable') &&
                   inventoryObject['type'] == 'procedure') {
                    inventoryObject['tasks'].push(resp['objuuid']);
                    inventoryObject['changed'] = true;
                    populateTaskTable();
                } else if(resp['type'] == 'rfc' && 
                          document.getElementById('rfcTable') &&
                          inventoryObject['type'] == 'procedure' &&
                          inventoryObject['rfcs'].indexOf(resp['objuuid']) == -1) {
                    inventoryObject['rfcs'].push(resp['objuuid']);
                    inventoryObject['changed'] = true;
                    populateRFCTable();
                }
            }
        });
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
                                    } else if(obj.item.method == 'edit procedure rfcs') {
                                        addMessage("edit procedure success");
                                        inventoryObject = resp;
                                        editProcedureRFCs();
                                    } else if(obj.item.method == 'edit rfc') {
                                        addMessage("edit rfc success");
                                        inventoryObject = resp;
                                        editRFC();
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

var initAttributes = function() {
    document.getElementById('attributes').innerHTML = '<table id="attributesTable"></table>';
}

var addAttributeTextBox = function(fieldName, inventoryKey) {
    var attributeTable = document.getElementById("attributesTable");
    var attributeRow = attributeTable.insertRow(-1);
    var attributeCell;
    
    attributeCell = attributeRow.insertCell(-1);
    attributeCell.innerHTML = fieldName;
    
    attributeCell = attributeRow.insertCell(-1);
    var id = 'inventory-obj-key-' + inventoryKey;
    attributeCell.innerHTML = '<input type="text" id="' + id + '" onchange="setInventoryKey(&quot;' + inventoryKey + '&quot;, &quot;' + id + '&quot;)" style="width:99%"></input>';
    document.getElementById(id).value = inventoryObject[inventoryKey];
}

var addAttributeText = function(fieldName, inventoryKey) {
    var attributeTable = document.getElementById("attributesTable");
    var attributeRow = attributeTable.insertRow(-1);
    var attributeCell;
    
    attributeCell = attributeRow.insertCell(-1);
    attributeCell.innerHTML = fieldName;
    
    attributeCell = attributeRow.insertCell(-1);
    var id = 'inventory-obj-key-' + inventoryKey;
    attributeCell.innerHTML = '<div id="' + id + '"></div>';
    document.getElementById(id).innerHTML = inventoryObject[inventoryKey];
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