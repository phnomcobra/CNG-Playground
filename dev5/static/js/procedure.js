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

var addProcedureRelated = function(objuuid) {
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            $("#relatedProcedureGrid").jsGrid("insertItem", {'name' : resp['name'], 'objuuid' : resp['objuuid']});
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
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            inventoryObject = resp;
            editProcedure();
        }
    });
}

var editProcedure = function() {
    populateProcedureAttributes();
    document.getElementById('body').innerHTML = '<div id="taskGrid" style="padding:10px;float:left"></div><div id="hostGrid" style="padding:10px;margin-left:calc(50% - 5px)"></div><div id="RFCGrid" style="padding:10px;float:left"></div><div id="relatedProcedureGrid" style="padding:10px;margin-left:calc(50% - 5px)"></div>';
    
    $("#taskGrid").jsGrid({
        height: "calc(50% - 5px)",
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
    
    $("#relatedProcedureGrid").jsGrid({
        height: "calc(50% - 5px)",
        width: "calc(50% - 5px)",
        autoload: true,
        
        deleteButton: true,
        confirmDeleting: false,
        
        rowClass: function(item, itemIndex) {
            return "client-" + itemIndex;
        },
        
        rowDoubleClick: function(args) {
            loadAndEditProcedure(args.item.objuuid);
        },
 
        controller: {
            loadData: function(filter) {
                return $.ajax({
                    type: "GET",
                    url: "/procedure/ajax_get_related_procedure_grid",
                    data: {'objuuid' : inventoryObject['objuuid']},
                    dataType: "JSON"
                });
            },
            insertItem: function(item) {
                inventoryObject['procedures'].push(item.objuuid);
                inventoryObject['changed'] = true;
            },
            deleteItem: function(item) {
                inventoryObject['procedures'].splice(inventoryObject['procedures'].indexOf(item.objuuid), 1);
                inventoryObject['changed'] = true;
            }
        },
        
        fields: [
            {name : "name", type : "text", title : "Related Procedure Name"},
            {name : "objuuid", type : "text", visible: false},
            {type : "control" }
        ],
    });
}

var viewProcedureResult = function(result) {
    document.getElementById('section-header-' + result.host.objuuid).innerHTML = result.host.name + '<br>' + result.host.host + '<br>' + result.status.name;
    
    document.getElementById('section-body-' + result.host.objuuid).innerHTML = '<table id="section-body-procedure-header-' + result.host.objuuid + '"></table>';
    
    var table = document.getElementById('section-body-procedure-header-' + result.host.objuuid);
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
    row.insertCell(-1).innerHTML = result.start;
    
    row = table.insertRow(-1);
    row.insertCell(-1).innerHTML = '<b>Procedure Stop:</b>';
    row.insertCell(-1).innerHTML = result.stop;
    
    row = table.insertRow(-1);
    row.insertCell(-1).innerHTML = '<b>Procedure Status:</b>';
    row.insertCell(-1).innerHTML = result.status.name;
    
    document.getElementById('section-body-' + result.host.objuuid).innerHTML += '<br><br><table id="section-body-rfcs-' + result.host.objuuid + '"></table>';
    table = document.getElementById('section-body-rfcs-' + result.host.objuuid);
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
        document.getElementById('section-body-' + result.host.objuuid).innerHTML += '<br><br><table id="section-body-task-header-' + i + '-' + result.host.objuuid + '"></table>';
        table = document.getElementById('section-body-task-header-' + i + '-' + result.host.objuuid);
    
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
        row.insertCell(-1).innerHTML = result.tasks[i].start;
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>Task Stop:</b>';
        row.insertCell(-1).innerHTML = result.tasks[i].stop;
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>Task Status:</b>';
        row.insertCell(-1).innerHTML = result.tasks[i].status.name;
        
        row = table.insertRow(-1);
        row.insertCell(-1).innerHTML = '<b>Task Output:</b>';
        cell = row.insertCell(-1);
        for(var j = 0; j < result.tasks[i].output.length; j++)
            cell.innerHTML += result.tasks[i].output[j];
        
        document.getElementById('section-body-' + result.host.objuuid).innerHTML += '<br>';
    }
    
    document.getElementById('section-header-' + result.host.objuuid).style.color = '#' + result.status.cfg;
    document.getElementById('section-header-' + result.host.objuuid).style.backgroundColor = '#' + result.status.cbg;
}

var executeProcedure = function() {
    populateProcedureAttributes();
    
    document.getElementById('body').innerHTML = '<div id="procedureResultAccordion"></div>';
    
    for(var i = 0; i < inventoryObject.hosts.length; i++) {
        addMessage('executing ' + inventoryObject.name + ' hstuuid: ' + inventoryObject.hosts[i]);
        
        document.getElementById('procedureResultAccordion').innerHTML += '<div id="section-header-' + inventoryObject.hosts[i] + '"></div>';
        document.getElementById('procedureResultAccordion').innerHTML += '<pre><code id="section-body-' + inventoryObject.hosts[i] + '"></code></pre>';
        
        $.ajax({
            'url' : 'procedure/ajax_execute_procedure',
            'dataType' : 'json',
            'data' : {'prcuuid' : inventoryObject.objuuid, 'hstuuid' : inventoryObject.hosts[i]},
            'success' : function(resp) {
                //console.log(resp);
                viewProcedureResult(resp);
            }
        });
    }
    
    $("#procedureResultAccordion").accordion({
        collapsible: true,
        heightStyle: "content",
        active: false
    });
}