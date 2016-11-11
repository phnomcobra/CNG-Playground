var contextMenu = {};
var inventoryObjects = {};
var tabs = {};

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
                    if(resp[item]['action']['method'] == 'ajax') {
                        contextMenu[item] = {
                            'label' : resp[item]['label'],
                            'route' : resp[item]['action']['route'],
                            'params' : resp[item]['action']['params'],
                            'action' : function (obj) {
                                $.ajax({
                                    'url' : obj.item.route,
                                    'dataType' : 'json',
                                    'data' : obj.item.params,
                                    'success' : function(resp) {
                                        addMessage("console select success " + resp);
                                        $('#inventory').jstree('refresh');
                                    },
                                    'error' : function(resp, status, error) {
                                        addMessage("console select failure " + resp);
                                    }
                                });
                            }
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
            },
            'error' : function(resp, status, error) {
                addMessage("move failure " + resp);
                $('#inventory').jstree('refresh');
            }
        });
});

var tabUpdate = function () {
    $.ajax({
        'url' : 'tabs/ajax_get_tabs',
        'dataType' : 'json',
        'success' : function(resp) {
            document.getElementById('handles').innerHTML = '';
            
            tabs = resp['tabs'];
            
            for(item in resp['tabs']) {
                if(!inventoryObjects[resp['tabs'][item]['id']]) {
                    $.ajax({
                        'url' : 'inventory/ajax_get_object',
                        'dataType' : 'json',
                        'data' : {'id' : resp['tabs'][item]['id']},
                        'success' : function(resp) {
                            addMessage("object load success " + resp['objuuid']);
                            resp['changed'] = false;
                            inventoryObjects[resp['objuuid']] = resp;
                        },
                        'error' : function(resp, status, error) {
                            addMessage("object load failure!");
                        }
                    });
                }

                var row = document.getElementById("handles");
                var cell = row.insertCell(-1);
                cell.innerHTML = '<input type="button" value="' + resp['tabs'][item]['name'] + '" onclick="tabSelect(&quot;' + resp['tabs'][item]['id'] + '&quot;, &quot;' + resp['tabs'][item]['action'] + '&quot;);" />';
            }
        },   
        'error' : function(resp, status, error) {
            addMessage("get tabs failure " + resp);
            document.getElementById('handles').innerHTML = '';
        }
    });
};

var editTask = function(resp) {
    document.getElementById('body').innerHTML = '<div id="aceInstance"></div>' + 
                                                'Task Name: <input type="text" id="taskName" onchange="setInventoryKey(' + 
                                                '&quot;' + resp['objuuid'] + '&quot;, &quot;name&quot;, &quot;taskName&quot;)"></input>';
                                                
    document.getElementById('taskName').value = resp['name'];
    var tabBody = new ace.edit(document.getElementById('aceInstance'));
    
    tabBody.setTheme("ace/theme/twilight");
    tabBody.session.setMode("ace/mode/python");
    tabBody.setValue(resp['body']);
    tabBody.selection.moveTo(0, 0);
    tabBody['inventoryObject'] = resp;
                                        
    tabBody.on('change', function(e, f) {
        f.inventoryObject['body'] = f.getValue();
        f.inventoryObject['changed'] = true;
    });
}

var tabSelect = function (objuuid, action) {
    if(action == 'edit') {
        editTask(inventoryObjects[objuuid]);
    }
};

/*var tabClose = function (item) {
    var handle = document.getElementById('handle-' + item);
    handle.parentNode.removeChild(handle);
    
    document.getElementById('body').innerHTML = '';
    
    delete inventoryObjects[item];
    
    $.ajax({
        'url' : 'tabs/ajax_close_tab',
        'dataType' : 'json',
        'data' : {
            'id' : item
        },
        'success' : function(resp) {
            addMessage("tab close success " + resp);
        },
        'error' : function(resp, status, error) {
            addMessage("tab close failure " + resp);
        }
    });
};*/

var inventoryApp = angular.module('inventoryApp', []);
inventoryApp.controller('inventoryCtrl', function($scope, $interval, $http, $sce) {
    $interval(function () {
        for(objuuid in inventoryObjects) {
            if(inventoryObjects[objuuid]['changed']) {
                $http.post('inventory/ajax_post_object', JSON.stringify(inventoryObjects[objuuid])
                ).then(function successCallback(response) {
                    addMessage("saving " + objuuid);
                    inventoryObjects[objuuid]['changed'] = false;
                });
            }
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

var setInventoryKey = function (objuuid, key, div) {
    inventoryObjects[objuuid][key] = document.getElementById(div).value;
    inventoryObjects[objuuid]['changed'] = true;
}