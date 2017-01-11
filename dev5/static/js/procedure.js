var procedureStateFlag = null;

var populateProcedureAttributes = function() {
    initAttributes();
    
    addAttributeText('Procedure UUID', 'objuuid');
    addAttributeTextBox('Procedure Name', 'name');
    addAttributeTextBox('Procedure Title', 'title');
    addAttributeTextArea('Description', 'description');
    
    $.ajax({
        'url' : 'inventory/ajax_get_status_objects',
        'dataType' : 'json',
        'success' : function(resp) {
            for(var i = 0; i < resp.length; i++) {
                resp[i];
                
                var continueKey = 'continue ' + resp[i].code;
                
                if(!(inventoryObject.hasOwnProperty(continueKey))) {
                    inventoryObject[continueKey] = false;
                }
                
                addAttributeCheckBox('Continue on ' + resp[i].name, continueKey);
            }
        }
    });
}

var addProcedureTask = function(objuuid) {
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            $("#taskGrid").jsGrid("insertItem", {'name' : resp['name'], 'objuuid' : resp['objuuid']});
        }
    });
}

var addProcedureRFC = function(objuuid) {
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            $("#RFCGrid").jsGrid("insertItem", {'name' : resp['name'], 'objuuid' : resp['objuuid'], 'title' : resp['title'], 'number' : resp['number']});
        }
    });
}

var loadAndEditProcedure = function(objuuid) {
    document.getElementById('body').innerHTML = '';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            inventoryObject = resp;
            editProcedure();
            expandToNode(inventoryObject.objuuid);
        }
    });
}

var editProcedure = function() {
    populateProcedureAttributes();
    document.getElementById('body').innerHTML = '<div id="taskGrid" style="padding:10px;float:left"></div><div id="hostGrid" style="padding:10px; margin-left:50%"></div><div id="RFCGrid" style="padding:10px;margin-left:50%"></div>';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    link = document.createElement("a");
    link.setAttribute("href", "#");
    link.innerHTML = "Run";
    cell = document.createElement("li");
    cell.setAttribute('onclick', 'executeProcedure(); runProcedure();');
    cell.appendChild(link);
    document.getElementById('menuBarDynamic').appendChild(cell);
    
    link = document.createElement("a");
    link.setAttribute("href", "#");
    link.innerHTML = "Details";
    cell = document.createElement("li");
    cell.setAttribute('onclick', 'executeProcedure();');
    cell.appendChild(link);
    document.getElementById('menuBarDynamic').appendChild(cell);
    
    $("#taskGrid").jsGrid({
        height: "calc(100% - 5px)",
        width: "calc(50% - 5px)",
        autoload: true,
        
        deleteButton: true,
        confirmDeleting: false,
        
        rowClass: function(item, itemIndex) {
            return "client-" + itemIndex;
        },
        
        rowDoubleClick: function(args) {
            loadAndEditTask(args.item.objuuid);
        },
        
        controller: {
            loadData: function(filter) {
                return $.ajax({
                    type: "GET",
                    url: "/procedure/ajax_get_task_grid",
                    data: {'objuuid' : inventoryObject['objuuid']},
                    dataType: "JSON"
                });
            },
            insertItem: function(item) {
                inventoryObject['tasks'].push(item.objuuid);
                inventoryObject['changed'] = true;
            },
            deleteItem: function(item) {
                inventoryObject['tasks'].splice(inventoryObject['tasks'].indexOf(item.objuuid), 1);
                inventoryObject['changed'] = true;
            }
        },
        
        fields: [
            {name : "name", type : "text", title : "Task Name"},
            {name : "objuuid", type : "text", visible: false},
            {type : "control" }
        ],
 
        onRefreshed: function() {
            var $gridData = $("#taskGrid .jsgrid-grid-body tbody");
 
            $gridData.sortable({
                update: function(e, ui) {
                    // array of indexes
                    var clientIndexRegExp = /\s*client-(\d+)\s*/;
                    var indexes = $.map($gridData.sortable("toArray", { attribute: "class" }), function(classes) {
                        return clientIndexRegExp.exec(classes)[1];
                    });
 
                    // arrays of items
                    var items = $.map($gridData.find("tr"), function(row) {
                        return $(row).data("JSGridItem");
                    });
                    
                    inventoryObject['tasks'] = [];
                    for(var i in items) {
                        inventoryObject['tasks'].push(items[i].objuuid);
                    }
                    inventoryObject['changed'] = true;
                }
            });
        }
    });
    
    $("#hostGrid").jsGrid({
        height: "calc(50% - 5px)",
        width: "calc(50% - 5px)",
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
                    url: "/procedure/ajax_get_host_grid",
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
    
    $("#RFCGrid").jsGrid({
        height: "calc(50% - 5px)",
        width: "calc(50% - 5px)",
        autoload: true,
        
        deleteButton: true,
        confirmDeleting: false,
        
        rowClass: function(item, itemIndex) {
            return "client-" + itemIndex;
        },
        
        rowDoubleClick: function(args) {
            loadAndEditRFC(args.item.objuuid);
        },
 
        controller: {
            loadData: function(filter) {
                return $.ajax({
                    type: "GET",
                    url: "/rfc/ajax_get_rfc_grid",
                    data: {'objuuid' : inventoryObject['objuuid']},
                    dataType: "JSON"
                });
            },
            insertItem: function(item) {
                inventoryObject['rfcs'].push(item.objuuid);
                inventoryObject['changed'] = true;
            },
            deleteItem: function(item) {
                inventoryObject['rfcs'].splice(inventoryObject['rfcs'].indexOf(item.objuuid), 1);
                inventoryObject['changed'] = true;
            }
        },
        
        fields: [
            {name : "number", type : "text", width : 50, title : "RFC Number"},
            {name : "name", type : "text", title : "Name"},
            {name : "title", type : "text", title : "Title"},
            {name : "objuuid", type : "text", visible: false},
            {type : "control" }
        ]
    });
    
    setTimeout(refreshJSGrids, 1000);
}

var viewProcedureResult = function(result) {
    document.getElementById('section-header-' + result.host.objuuid + '-' + result.procedure.objuuid).innerHTML = result.procedure.name + '<br>' + result.host.name + ' ' + result.host.host + ' <br>' + new Date(result.stop * 1000) + ' [' + result.status.name + ']';
    
    document.getElementById('section-body-' + result.host.objuuid + '-' + result.procedure.objuuid).innerHTML = '<table class="table" id="section-body-procedure-header-' + result.host.objuuid + '-' + result.procedure.objuuid + '"></table>';
    
    var table = document.getElementById('section-body-procedure-header-' + result.host.objuuid + '-' + result.procedure.objuuid);
    var row;
    var cell;
    
    row = table.insertRow(-1);
    row.insertCell(-1).innerHTML = '<b>Procedure Name:</b>';
    row.insertCell(-1).innerHTML = result.procedure.name;
    
    row = table.insertRow(-1);
    row.insertCell(-1).innerHTML = '<b>Procedure Title:</b>';
    row.insertCell(-1).innerHTML = result.procedure.title;
    
    row = table.insertRow(-1);
    row.insertCell(-1).innerHTML = '<b>Procedure Description:</b>';
    row.insertCell(-1).innerHTML = result.procedure.description;
    
    row = table.insertRow(-1);
    row.insertCell(-1).innerHTML = '<b>Procedure Start:</b>';
    row.insertCell(-1).innerHTML = new Date(result.start * 1000);
    
    row = table.insertRow(-1);
    row.insertCell(-1).innerHTML = '<b>Procedure Stop:</b>';
    row.insertCell(-1).innerHTML = new Date(result.stop * 1000);
    
    row = table.insertRow(-1);
    row.insertCell(-1).innerHTML = '<b>Procedure Status:</b>';
    row.insertCell(-1).innerHTML = result.status.name;
    
    row = table.insertRow(-1);
    row.insertCell(-1).innerHTML = '<b>Procedure Output:</b>';
    cell = row.insertCell(-1);
    for(var j = 0; j < result.output.length; j++)
        cell.innerHTML += result.output[j] + '<br>';
    
    document.getElementById('section-body-' + result.host.objuuid + '-' + result.procedure.objuuid).innerHTML += '<br><br><table class="table" id="section-body-rfcs-' + result.host.objuuid + '-' + result.procedure.objuuid + '"></table>';
    table = document.getElementById('section-body-rfcs-' + result.host.objuuid + '-' + result.procedure.objuuid);
    for(var i = 0; i < result.rfcs.length; i++) {
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>RFC Name:</b>';
        row.insertCell(-1).innerHTML = result.rfcs[i].name;
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>RFC Number:</b>';
        row.insertCell(-1).innerHTML = result.rfcs[i].number;
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>RFC Description:</b>';
        row.insertCell(-1).innerHTML = result.rfcs[i].description;
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>POC Name:</b>';
        row.insertCell(-1).innerHTML = result.rfcs[i]['poc name'];
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>POC Email:</b>';
        row.insertCell(-1).innerHTML = result.rfcs[i]['poc email'];
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>POC Phone:</b>';
        row.insertCell(-1).innerHTML = result.rfcs[i]['poc phone'];
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = ' ';
    }
    
    for(var i = 0; i < result.tasks.length; i++) {
        document.getElementById('section-body-' + result.host.objuuid + '-' + result.procedure.objuuid).innerHTML += '<br><br><table class="table" id="section-body-task-header-' + i + '-' + result.host.objuuid + '-' + result.procedure.objuuid + '"></table>';
        table = document.getElementById('section-body-task-header-' + i + '-' + result.host.objuuid + '-' + result.procedure.objuuid);
    
        row = table.insertRow(-1);
        cell = row.insertCell(-1);
        cell.innerHTML = '<b>' + result.tasks[i].status.abbreviation + '</b>';
        cell.style.color = '#' + result.tasks[i].status.cfg;
        cell.style.backgroundColor = '#' + result.tasks[i].status.cbg;
        
        cell = row.insertCell(-1);
        cell.style.color = '#' + result.tasks[i].status.cfg;
        cell.style.backgroundColor = '#' + result.tasks[i].status.cbg;
    
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>Task Name:</b>';
        row.insertCell(-1).innerHTML = result.tasks[i].name;
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>Task Start:</b>';
        row.insertCell(-1).innerHTML = new Date(result.tasks[i].start * 1000);
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>Task Stop:</b>';
        row.insertCell(-1).innerHTML = new Date(result.tasks[i].stop * 1000);
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>Task Status:</b>';
        row.insertCell(-1).innerHTML = result.tasks[i].status.name;
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>Task Output:</b>';
        cell = row.insertCell(-1);
        for(var j = 0; j < result.tasks[i].output.length; j++)
            cell.innerHTML += result.tasks[i].output[j] + '<br>';
        
        document.getElementById('section-body-' + result.host.objuuid + '-' + result.procedure.objuuid).innerHTML += '<br>';
    }
    
    document.getElementById('section-header-' + result.host.objuuid + '-' + result.procedure.objuuid).style.color = '#' + result.status.cfg;
    document.getElementById('section-header-' + result.host.objuuid + '-' + result.procedure.objuuid).style.backgroundColor = '#' + result.status.cbg;
}

var executeProcedure = function() {
    populateProcedureAttributes();
    
    document.getElementById('body').innerHTML = '<div id="procedureResultAccordion"></div>';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    for(var i = 0; i < inventoryObject.hosts.length; i++) {
        document.getElementById('procedureResultAccordion').innerHTML += '<div id="section-header-' + inventoryObject.hosts[i] + '-' + inventoryObject.objuuid + '"></div>';
        document.getElementById('procedureResultAccordion').innerHTML += '<pre><code id="section-body-' + inventoryObject.hosts[i] + '-' + inventoryObject.objuuid + '"></code></pre>';
    }
    
    $("#procedureResultAccordion").accordion({
        collapsible: true,
        heightStyle: "content",
        active: false
    });
    
    link = document.createElement("a");
    link.setAttribute("href", "#");
    link.innerHTML = "Run";
    cell = document.createElement("li");
    cell.setAttribute('onclick', 'runProcedure()');
    cell.appendChild(link);
    document.getElementById('menuBarDynamic').appendChild(cell);
    
    link = document.createElement("a");
    link.setAttribute("href", "#");
    link.innerHTML = "Edit";
    cell = document.createElement("li");
    cell.setAttribute('onclick', 'editProcedure()');
    cell.appendChild(link);
    document.getElementById('menuBarDynamic').appendChild(cell);
    
    updateProcedureTimer();
    updateProcedureStateData();
}

var runProcedure = function () {
    for(var i = 0; i < inventoryObject.hosts.length; i++) {
        $.ajax({
            'url' : 'procedure/ajax_queue_procedure',
            'dataType' : 'json',
            'data' : {
                'prcuuid' : inventoryObject.objuuid, 
                'hstuuid' : inventoryObject.hosts[i]
            },
            'success' : function(resp){
                $('.nav-tabs a[href="#queue"]').tab('show');
            },
            'failure' : function(resp){
                $('.nav-tabs a[href="#console"]').tab('show');
            }
        });
    }
}

var updateProcedureTimer = function() {
    if(document.getElementById('procedureResultAccordion')) {
        $.ajax({
            'url' : 'flags/ajax_get',
            'dataType' : 'json',
            'data' : {
                //'key' : 'controller-' + inventoryObject.objuuid
                'key' : 'results'
            },
            'success' : function(resp) {
                if(procedureStateFlag != resp.value) {
                    procedureStateFlag = resp.value;
                    updateProcedureStateData();
                }
                setTimeout(updateProcedureTimer, 1000);
            },
        });
    }
}

var updateProcedureStateData = function() {
    for(var i = 0; i < inventoryObject.hosts.length; i++) {
        $.ajax({
            'url' : 'results/ajax_get_procedure',
            'dataType' : 'json',
            'data' : {
                'prcuuid' : inventoryObject.objuuid,
                'hstuuid' : inventoryObject.hosts[i]
            },
            'success' : function(resp) {
                viewProcedureResult(resp);
            }
        });
    }
}
