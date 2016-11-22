var contextMenu = {};
var inventoryObject = {};
var saving = false;

 $('#inventory').jstree({
'plugins' : ['contextmenu', 'dnd', 'checkbox'],
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
    if(data.event.target.offsetParent.id == 'taskGrid' ||
       data.event.target.offsetParent.className == 'js-grid-body') {
        var nodes = $('#inventory').jstree().get_selected(true);
        for(i in nodes) {
            $.ajax({
                'url' : 'inventory/ajax_get_object',
                'dataType' : 'json',
                'data' : {'objuuid' : nodes[i].id},
                'success' : function(resp) {
                    $('#inventory').jstree("deselect_all");
                    if(resp['type'] == 'task') {
                        addProcedureTask(resp['objuuid']);
                    }
                }
            });
        }
    }
});

var createNode = function(object) {
    var parentNode = $('#inventory').find("[id='" + object['parent'] + "']");
    $('#inventory').jstree('create_node', parentNode, {'id' : object['objuuid'], 'parent' : object['parent'], 'text' : object['name'], 'icon' : object['icon']}, 'last', false, false);
}

var deleteNode = function(objuuid) {
    var node = $('#inventory').find("[id='" + objuuid + "']");
    $('#inventory').jstree('delete_node', node);
    if(inventoryObject['objuuid'] == objuuid) {
        inventoryObject = {}
        document.getElementById('attributes').innerHTML = '';
        document.getElementById('body').innerHTML = '';
    }
}

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
                                    $('#inventory').jstree("deselect_all");
                                    if(obj.item.method == 'create container') {
                                        addMessage('create container success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editContainer();
                                    } else if(obj.item.method == 'create task') {
                                        addMessage('create task success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editTask();
                                    } else if(obj.item.method == 'create rfc') {
                                        addMessage('create rfc success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editRFC();
                                    } else if(obj.item.method == 'create procedure') {
                                        addMessage('create procedure success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editProcedure();
                                    } else if(obj.item.method == 'create status') {
                                        addMessage('create status success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editStatusCode();
                                    } else if(obj.item.method == 'create host') {
                                        addMessage('create host success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editHost();
                                    } else if(obj.item.method == 'create controller') {
                                        addMessage('create controller success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editController();
                                    } else if(obj.item.method == 'edit task') {
                                        addMessage("edit task success");
                                        inventoryObject = resp;
                                        editTask();
                                    } else if(obj.item.method == 'edit container') {
                                        addMessage("edit container success");
                                        inventoryObject = resp;
                                        editContainer();
                                    } else if(obj.item.method == 'edit procedure') {
                                        addMessage("edit procedure success");
                                        inventoryObject = resp;
                                        editProcedure();
                                    } else if(obj.item.method == 'edit rfc') {
                                        addMessage("edit rfc success");
                                        inventoryObject = resp;
                                        editRFC();
                                    } else if(obj.item.method == 'edit status code') {
                                        addMessage("edit status success");
                                        inventoryObject = resp;
                                        editStatusCode();
                                    } else if(obj.item.method == 'edit host') {
                                        addMessage("edit host success");
                                        inventoryObject = resp;
                                        editHost();
                                    } else if(obj.item.method == 'edit controller') {
                                        addMessage("edit controller success");
                                        inventoryObject = resp;
                                        editController();
                                    } else if(obj.item.method == 'delete node') {
                                        addMessage("delete success");
                                        deleteNode(resp['id']);
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

$('#inventory').on("move_node.jstree", function(event, data) {
        $('#inventory').jstree("deselect_all");
        $.ajax({
            'url' : 'inventory/ajax_move',
            'dataType' : 'json',
            'data' : {
                'objuuid' : data.node.id,
                'parent_objuuid' : data.node.parent
            },
            'success' : function(resp) {
                addMessage('move success');
            },
            'error' : function(resp, status, error) {
                addMessage('move failure');
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

var addAttributeTextArea = function(fieldName, inventoryKey) {
    var attributeTable = document.getElementById("attributesTable");
    var attributeRow = attributeTable.insertRow(-1);
    var attributeCell;
    
    attributeCell = attributeRow.insertCell(-1);
    attributeCell.innerHTML = fieldName;
    
    attributeCell = attributeRow.insertCell(-1);
    var id = 'inventory-obj-key-' + inventoryKey;
    attributeCell.innerHTML = '<textarea rows = "5" id="' + id + '" onchange="setInventoryKey(&quot;' + inventoryKey + '&quot;, &quot;' + id + '&quot;)" style="width:98%;"></textarea>';
    document.getElementById(id).value = inventoryObject[inventoryKey];
}

var addAttributeCheckBox = function(fieldName, inventoryKey) {
    var attributeTable = document.getElementById("attributesTable");
    var attributeRow = attributeTable.insertRow(-1);
    var attributeCell;
    
    attributeCell = attributeRow.insertCell(-1);
    attributeCell.innerHTML = fieldName;
    
    attributeCell = attributeRow.insertCell(-1);
    var id = 'inventory-obj-key-' + inventoryKey;
    attributeCell.innerHTML = '<input type="checkbox" id="' + id + '" onchange="this.value = this.checked;setInventoryKey(&quot;' + inventoryKey + '&quot;, &quot;' + id + '&quot;)"></input>';
    document.getElementById(id).checked = inventoryObject[inventoryKey];
    document.getElementById(id).value = inventoryObject[inventoryKey];
}

var addAttributeColor = function(fieldName, inventoryKey) {
    var attributeTable = document.getElementById("attributesTable");
    var attributeRow = attributeTable.insertRow(-1);
    var attributeCell;
    
    attributeCell = attributeRow.insertCell(-1);
    attributeCell.innerHTML = fieldName;
    
    attributeCell = attributeRow.insertCell(-1);
    var id = 'inventory-obj-key-' + inventoryKey;
    attributeCell.innerHTML = '<input class="jscolor" id="' + id + '" onchange="setInventoryKey(&quot;' + inventoryKey + '&quot;, &quot;' + id + '&quot;)" style="width:99%"></input>';
    jsc.tryInstallOnElements([document.getElementById(id)], "jscolor");
    jsc.register();
    document.getElementById(id).jscolor.fromString(inventoryObject[inventoryKey]);
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
        $("#inventory").jstree('rename_node', inventoryObject['objuuid'] , inventoryObject[key]);
    }
}