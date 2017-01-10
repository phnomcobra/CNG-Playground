var contextMenu = {};
var inventoryObject = {};
var saving = false;
var inventoryStateFlag = null;
var queueStateFlag = null;

 $('#inventory').jstree({
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
        }
    },
    'search': {
        'case_insensitive': true,
        'show_only_matches' : true
    },
    'plugins' : ['contextmenu', 'dnd', 'checkbox', 'search', 'sort']
});

var to = false;
 $('#inventorySearchTextBox').keyup(function () {
            if(to) { clearTimeout(to); }
            to = setTimeout(function () {
                var v = $('#inventorySearchTextBox').val();
                $('#inventory').jstree(true).search(v);
            }, 500);
        });

var searchInventoryTree = function(item) {
    $('#inventory').jstree(true).search(item.value);
}

$(document).on('dnd_stop.vakata', function (e, data) {
    if(data.event.target.className == 'jsgrid-grid-body' ||
       data.event.target.className == 'jsgrid-cell') {
        var nodes = $('#inventory').jstree().get_selected(true);
        for(i in nodes) {
            $.ajax({
                'url' : 'inventory/ajax_get_object',
                'dataType' : 'json',
                'data' : {'objuuid' : nodes[i].id},
                'success' : function(resp) {
                    $('#inventory').jstree("deselect_all");
                    if(resp['type'] == 'task' && document.getElementById('taskGrid')) {
                        addProcedureTask(resp['objuuid']);
                    } else if(resp['type'] == 'rfc' &&
                              inventoryObject['rfcs'].indexOf(resp['objuuid']) == -1 &&
                              document.getElementById('RFCGrid')) {
                        addProcedureRFC(resp['objuuid']);
                    } else if(resp['type'] == 'host' &&
                              inventoryObject['hosts'].indexOf(resp['objuuid']) == -1 &&
                              document.getElementById('hostGrid')) {
                        addControllerHost(resp['objuuid']);
                    } else if(resp['type'] == 'procedure' &&
                              inventoryObject['procedures'].indexOf(resp['objuuid']) == -1 &&
                              document.getElementById('procedureGrid')) {
                        addControllerProcedure(resp['objuuid']);
                    }
                }
            });
        }
    }
});

var exportFromInventory = function() {
    $('.nav-tabs a[href="#console"]').tab('show');
    
    var nodes = $('#inventory').jstree().get_selected(true);
    
    var objuuids = []
    for(i in nodes)
        objuuids.push(nodes[i].id);
    
    window.location = 'inventory/export_objects?objuuids=' + objuuids.join(',');
}

var importToInventory = function(item) {
    $('.nav-tabs a[href="#console"]').tab('show');
    
    var formData = new FormData();
    formData.append("file", item.files[0], item.files[0].name);
    
    //var xhr = new XMLHttpRequest();
    //xhr.open('POST', 'inventory/import_objects', true);
    //xhr.send(formData);
    
     
    $.ajax({
        url: 'inventory/import_objects',  //Server script to process data
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(resp) {
            touchInventory();
            $('#inventory').jstree('refresh');
        }
    }); 
}

var createNode = function(object) {
    var parentNode = $('#inventory').find("[id='" + object['parent'] + "']");
    $('#inventory').jstree('create_node', parentNode, {'id' : object['objuuid'], 'parent' : object['parent'], 'text' : object['name'], 'icon' : object['icon']}, 'last', false, false);
    touchInventory();
}

var deleteNode = function(objuuid) {
    $('.nav-tabs a[href="#console"]').tab('show');
    var node = $('#inventory').find("[id='" + objuuid + "']");
    $('#inventory').jstree('delete_node', node);
    if(inventoryObject['objuuid'] == objuuid) {
        inventoryObject = {}
        document.getElementById('attributes').innerHTML = '';
        document.getElementById('body').innerHTML = '';
    }
    touchInventory();
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
                                        document.title = resp.type + ": " + resp.name;
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editContainer();
                                        touchInventory();
                                        $('.nav-tabs a[href="#attributes"]').tab('show');
                                    } else if(obj.item.method == 'create task') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage('create task success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editTask();
                                        touchInventory();
                                        $('.nav-tabs a[href="#attributes"]').tab('show');
                                    } else if(obj.item.method == 'create rfc') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage('create rfc success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editRFC();
                                        touchInventory();
                                        $('.nav-tabs a[href="#attributes"]').tab('show');
                                    } else if(obj.item.method == 'create procedure') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage('create procedure success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editProcedure();
                                        touchInventory();
                                        $('.nav-tabs a[href="#attributes"]').tab('show');
                                    } else if(obj.item.method == 'create status') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage('create status success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editStatusCode();
                                        touchInventory();
                                        $('.nav-tabs a[href="#attributes"]').tab('show');
                                    } else if(obj.item.method == 'create host') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage('create host success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editHost();
                                        touchInventory();
                                        $('.nav-tabs a[href="#attributes"]').tab('show');
                                    } else if(obj.item.method == 'create console') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage('create console success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editConsole();
                                        touchInventory();
                                        $('.nav-tabs a[href="#attributes"]').tab('show');
                                    } else if(obj.item.method == 'create controller') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage('create controller success');
                                        inventoryObject = resp;
                                        createNode(resp);
                                        editController();
                                        touchInventory();
                                        $('.nav-tabs a[href="#body"]').tab('show');
                                    } else if(obj.item.method == 'edit task') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("edit task success");
                                        inventoryObject = resp;
                                        editTask();
                                        $('.nav-tabs a[href="#body"]').tab('show');
                                    } else if(obj.item.method == 'edit task hosts') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("edit task success");
                                        inventoryObject = resp;
                                        editTaskHosts();
                                        setTimeout(refreshJSGrids, 1000);
                                        $('.nav-tabs a[href="#body"]').tab('show');
                                    } else if(obj.item.method == 'edit container') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("edit container success");
                                        inventoryObject = resp;
                                        editContainer();
                                        $('.nav-tabs a[href="#attributes"]').tab('show');
                                    } else if(obj.item.method == 'edit procedure') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("edit procedure success");
                                        inventoryObject = resp;
                                        editProcedure();
                                        setTimeout(refreshJSGrids, 1000);
                                        $('.nav-tabs a[href="#body"]').tab('show');
                                    } else if(obj.item.method == 'edit rfc') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("edit rfc success");
                                        inventoryObject = resp;
                                        editRFC();
                                        $('.nav-tabs a[href="#attributes"]').tab('show');
                                    } else if(obj.item.method == 'edit status code') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("edit status success");
                                        inventoryObject = resp;
                                        editStatusCode();
                                        $('.nav-tabs a[href="#attributes"]').tab('show');
                                    } else if(obj.item.method == 'edit host') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("edit host success");
                                        inventoryObject = resp;
                                        editHost();
                                        $('.nav-tabs a[href="#attributes"]').tab('show');
                                    } else if(obj.item.method == 'edit controller') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("edit controller success");
                                        inventoryObject = resp;
                                        editController();
                                        setTimeout(refreshJSGrids, 1000);
                                        $('.nav-tabs a[href="#body"]').tab('show');
                                    } else if(obj.item.method == 'edit console') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("edit console success");
                                        inventoryObject = resp;
                                        editConsole();
                                        $('.nav-tabs a[href="#body"]').tab('show');
                                    } else if(obj.item.method == 'run procedure') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("run procedure success");
                                        inventoryObject = resp;
                                        executeProcedure();
                                        $('.nav-tabs a[href="#body"]').tab('show');
                                    } else if(obj.item.method == 'run controller') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("run controller success");
                                        inventoryObject = resp;
                                        executeController();
                                        $('.nav-tabs a[href="#body"]').tab('show');
                                    } else if(obj.item.method == 'run task') {
                                        document.title = resp.type + ": " + resp.name;
                                        addMessage("run task success");
                                        inventoryObject = resp;
                                        executeTask();
                                        $('.nav-tabs a[href="#body"]').tab('show');
                                    } else if(obj.item.method == 'delete node') {
                                        document.title = "ValARIE WebApp";
                                        addMessage("delete success");
                                        deleteNode(resp['id']);
                                        touchInventory();
                                        $('.nav-tabs a[href="#console"]').tab('show');
                                    } else if(obj.item.method == 'copy node') {
                                        addMessage("copy success");
                                        createNode(resp);
                                        touchInventory();
                                    } else if(obj.item.method == 'create terminal') {
                                        document.title = "terminal: " + resp.name;
                                        addMessage("start terminal success");
                                        inventoryObject = resp;
                                        launchTerminal();
                                        $('.nav-tabs a[href="#body"]').tab('show');
                                    }
                                },
                                'error' : function(resp, status, error) {
                                    $('.nav-tabs a[href="#console"]').tab('show');
                                    addMessage("console select failure " + resp);
                                    console.log(resp);
                                    console.log(status);
                                    console.log(error);
                                }
                            });
                        }
                    }
                }
            },
            'error' : function(resp, status, error) {
                $('.nav-tabs a[href="#console"]').tab('show');
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
                $('.nav-tabs a[href="#console"]').tab('show');
                addMessage('move success');
                touchInventory();
            },
            'error' : function(resp, status, error) {
                addMessage('move failure');
                $('.nav-tabs a[href="#console"]').tab('show');
                $('#inventory').jstree('refresh');
            }
        });
});

var initAttributes = function() {
    document.getElementById('attributes').innerHTML = '<table id="attributesTable" class="table"></table>';
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

var addAttributeRadioGroup = function(fieldName, inventoryKey, radioButtons) {
    var attributeTable = document.getElementById("attributesTable");
    var attributeRow = attributeTable.insertRow(-1);
    var attributeCell;
    
    attributeCell = attributeRow.insertCell(-1);
    attributeCell.innerHTML = fieldName;
    
    attributeCell = attributeRow.insertCell(-1);
    attributeCell.innerHTML = '';
    for(var i = 0; i < radioButtons.length; i++) {
        if(inventoryObject[inventoryKey] == radioButtons[i].value) {
            attributeCell.innerHTML += '<input type="radio" name="radio-' + inventoryKey + 
                                       '" value="' + radioButtons[i].value + 
                                       '" checked=true onclick="inventoryObject[&quot;' + inventoryKey + '&quot;]=this.value;inventoryObject[&quot;changed&quot;]=true;">' +
                                       radioButtons[i].name + '<br>';
        } else {
            attributeCell.innerHTML += '<input type="radio" name="radio-' + inventoryKey + 
                                       '" value="' + radioButtons[i].value + 
                                       '" onclick="inventoryObject[&quot;' + inventoryKey + '&quot;]=this.value;inventoryObject[&quot;changed&quot;]=true;">' +
                                       radioButtons[i].name + '<br>';
        }
    }
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
            inventoryObject['changed'] = false;
            saving = true;
            $http.post('inventory/ajax_post_object', JSON.stringify(inventoryObject)
            ).then(function successCallback(response) {
                addMessage("saving " + inventoryObject['objuuid']);
                saving = false;
                
                if(inventoryObject['refreshTree']) {
                    $('#inventory').jstree('refresh');
                    inventoryObject['refreshTree'] = false;
                }
                
            }, function errorCallback(response) {
                $('.nav-tabs a[href="#console"]').tab('show');
                addMessage("save failure " + inventoryObject['objuuid']);
                saving = false;
            });
        }
        
        $http.get("messaging/ajax_get_messages").then(function (response) {
            var messageData = '<table>';
            var responseJSON = angular.fromJson(response)['data']['messages'];
            for(item in responseJSON) {
                messageData += '<tr><td>' + responseJSON[item]['timestamp'] + '</td><td>' + responseJSON[item]['message'] + '</td></tr>';
            }
            messageData += '</table>'
            
            $scope.messages = $sce.trustAsHtml(messageData);
        });
        
        $.ajax({
            'url' : 'flags/ajax_get',
            'dataType' : 'json',
            'data' : {
                'key' : 'inventoryState'
            },
            'success' : function(resp) {
                if(inventoryStateFlag != resp.value) {
                    inventoryStateFlag = resp.value;
                    $('#inventory').jstree('refresh');
                }
            },
        });
        
        $.ajax({
            'url' : 'flags/ajax_get',
            'dataType' : 'json',
            'data' : {
                'key' : 'queueState'
            },
            'success' : function(resp) {
                if(queueStateFlag != resp.value) {
                    queueStateFlag = resp.value;
                    updateQueueState();
                }
            },
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
        document.title = inventoryObject.type + ": " + inventoryObject.name;
        touchInventory();
    }
}

var touchInventory = function() {
    $.ajax({
        'url' : 'flags/ajax_touch',
        'dataType' : 'json',
        'data' : {
            'key' : 'inventoryState'
        },
        'success' : function(resp) {
            inventoryStateFlag = resp.value;
        },
    });
}

/* Exists to mitigate css race condition 
between BS transitions and jsgrid instantiation. */
var refreshJSGrids = function() {
    $('.jsgrid').each(function(){
        $(this).jsGrid('refresh');
    });
}

var selectDependencies = function() {
    //$('#inventory').jstree("deselect_all");
    
    var nodes = $('#inventory').jstree().get_selected(true);
    
    var objuuids = []
    for(i in nodes)
        objuuids.push(nodes[i].id);
    
    $.ajax({
        'type' : 'POST',
        'url' : 'inventory/ajax_get_dependencies',
        'dataType' : 'json',
        'contentType' : 'application/json',
        'data' : JSON.stringify(objuuids),
        'success' : function(objuuids) {
            for(var i in objuuids) {
                $('#inventory').jstree(true).select_node(objuuids[i]);
            }
        },
    });
}

var expandToNode = function(nodeID) {
    $('#inventory').jstree("deselect_all");
    $('#inventory').jstree(true).select_node(nodeID);
}