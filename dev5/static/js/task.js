var editTask = function() {
    document.getElementById('body').innerHTML = '<div id="aceInstance"></div>';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    initAttributes();
    addAttributeText('Task UUID', 'objuuid');
    addAttributeTextBox('Task Name', 'name');

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

var addRunTaskHost = function(objuuid) {
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            $("#runTaskHostGrid").jsGrid("insertItem", {'name' : resp['name'], 'objuuid' : resp['objuuid'], 'host' : resp['host']});
        }
    });
}

var executeTask = function() {
    for(var i = 0; i < inventoryObject.hosts.length; i++) {
        $.ajax({
            'url' : 'task/ajax_execute_task',
            'dataType' : 'json',
            'data' : {'tskuuid' : inventoryObject.objuuid, 'hstuuid' : inventoryObject.hosts[i]},
            'success' : function(resp) {
                console.log(resp);
            }
        });
    }
}

var runTask = function() {
    initAttributes();
    addAttributeText('Task UUID', 'objuuid');
    
    document.getElementById('menuBarDynamic').innerHTML = '<div class="menuBarItem" onclick="executeTask()">Run Task</div>';
    document.getElementById('body').innerHTML = '<div id="hostGrid" style="padding:10px"></div>';
    
    $("#hostGrid").jsGrid({
        height: "calc(50% - 5px)",
        width: "calc(100% - 5px)",
        autoload: true,
        
        deleteButton: true,
        confirmDeleting: false,
        
        rowDoubleClick: function(args) {
            loadAndEditHost(args.item.objuuid);
        },
        
        rowClass: function(item, itemIndex) {
            return "client-" + itemIndex;
        },
 
        controller: {
            loadData: function(filter) {
                return $.ajax({
                    type: "GET",
                    url: "/task/ajax_get_host_grid",
                    data: {'objuuid' : inventoryObject['objuuid']},
                    dataType: "JSON"
                });
            },
            insertItem: function(item) {
                inventoryObject['hosts'].push(item.objuuid);
                inventoryObject['changed'] = true;
            },
            deleteItem: function(item) {
                inventoryObject['hosts'].splice(inventoryObject['hosts'].indexOf(item.objuuid), 1);
                inventoryObject['changed'] = true;
            }
        },
        
        fields: [
            {name : "name", type : "text", title : "Host Name"},
            {name : "host", type : "text", title : "Host"},
            {name : "objuuid", type : "text", visible: false},
            {type : "control" }
        ],
    });
}