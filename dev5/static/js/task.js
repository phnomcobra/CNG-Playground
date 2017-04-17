var editTask = function() {
    document.getElementById('body').innerHTML = '<div id="aceInstance"></div>';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    document.title = inventoryObject.name;
    document.getElementById('bodyTitle').innerHTML = inventoryObject.type.toUpperCase() + ': ' + inventoryObject.name;
    $('.nav-tabs a[href="#body"]').tab('show');
    
    initAttributes();
    addAttributeText('Task UUID', 'objuuid');
    addAttributeTextBox('Task Name', 'name');

    var editor = new ace.edit(document.getElementById('aceInstance'));
    
    //editor.setTheme("ace/theme/twilight");
    editor.session.setMode("ace/mode/python");
    editor.setValue(inventoryObject['body']);
    editor.selection.moveTo(0, 0);
    editor['inventoryObject'] = inventoryObject;
                                        
    editor.on('change', function(e, f) {
        f.inventoryObject['body'] = f.getValue();
        f.inventoryObject['changed'] = true;
    });
    
    loadRequiresGrid();
    loadProvidesGrid();
}

var loadAndEditTask = function(objuuid) {
    document.getElementById('body').innerHTML = '';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'method': 'POST',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            inventoryObject = resp;
            editTask();
            expandToNode(inventoryObject.objuuid);
        }
    });
}

var addRunTaskHost = function(objuuid) {
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'method': 'POST',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            $("#runTaskHostGrid").jsGrid("insertItem", {'name' : resp['name'], 'objuuid' : resp['objuuid'], 'host' : resp['host']});
        }
    });
}

var viewTaskResult = function(result) {
    document.getElementById('section-header-' + result.host.objuuid).innerHTML = result.host.name + ' - ' + result.host.host + ' - ' + result.status.name;
    
    for(var i = 0; i < result.output.length; i++)
        document.getElementById('section-body-' + result.host.objuuid).innerHTML += result.output[i] + '<br>';
        
    document.getElementById('section-header-' + result.host.objuuid).style.color = '#' + result.status.cfg;
    document.getElementById('section-header-' + result.host.objuuid).style.backgroundColor = '#' + result.status.cbg;
}

var executeTask = function() {
    initAttributes();
    addAttributeText('Task UUID', 'objuuid');
    addAttributeTextBox('Task Name', 'name');
    
    document.title = inventoryObject.name;
    document.getElementById('bodyTitle').innerHTML = inventoryObject.type.toUpperCase() + ': ' + inventoryObject.name;
    $('.nav-tabs a[href="#body"]').tab('show');
    
    document.getElementById('body').innerHTML = '<div id="taskResultAccordion"></div>';
    
    for(var i = 0; i < inventoryObject.hosts.length; i++) {
        addMessage('executing ' + inventoryObject.name + ' hstuuid: ' + inventoryObject.hosts[i]);
        
        document.getElementById('taskResultAccordion').innerHTML += '<div id="section-header-' + inventoryObject.hosts[i] + '"></div>';
        document.getElementById('taskResultAccordion').innerHTML += '<pre><code id="section-body-' + inventoryObject.hosts[i] + '"></code></pre>';
        
        $.ajax({
            'url' : 'task/ajax_execute_task',
            'dataType' : 'json',
            'method': 'POST',
            'data' : {'tskuuid' : inventoryObject.objuuid, 'hstuuid' : inventoryObject.hosts[i]},
            'success' : function(resp) {
                //console.log(resp);
                viewTaskResult(resp);
            }
        });
    }
    
    $("#taskResultAccordion").accordion({
        collapsible: true,
        heightStyle: "content"
    });
    
    loadRequiresGrid();
    loadProvidesGrid();
}

var editTaskHosts = function() {
    initAttributes();
    addAttributeText('Task UUID', 'objuuid');
    addAttributeTextBox('Task Name', 'name');
    
    document.title = inventoryObject.name;
    document.getElementById('bodyTitle').innerHTML = inventoryObject.type.toUpperCase() + ': ' + inventoryObject.name;
    $('.nav-tabs a[href="#body"]').tab('show');
    
    document.getElementById('body').innerHTML = '<div id="hostGrid" style="padding:10px"></div>';
    
    $("#hostGrid").jsGrid({
        width: "calc(100% - 5px)",
        height: "calc(100% - 5px)",
        autoload: true,
        
        deleteButton: true,
        confirmDeleting: false,
        sorting: false,
        
        editing: true,
        onItemEditing: function(args) {
            loadAndEditHost(args.item.objuuid);
        },
        
        rowClass: function(item, itemIndex) {
            return "client-" + itemIndex;
        },
 
        controller: {
            loadData: function(filter) {
                return $.ajax({
                    type: "POST",
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
    
    loadRequiresGrid();
    loadProvidesGrid();
    
    setTimeout(refreshJSGrids, 1000);
}