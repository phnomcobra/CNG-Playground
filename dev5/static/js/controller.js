var controllerStateFlag = null;
var controllerStateData;
var showControllerDetails = false;

/*
var touchController = function() {
    $.ajax({
        'url' : 'flags/ajax_touch',
        'dataType' : 'json',
        'data' : {
            'key' : 'controller-' + inventoryObject.objuuid;
        },
        'success' : function(resp) {
            controllerStateFlag = resp.value;
        },
    });
}
*/

var addControllerProcedure = function(objuuid) {
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            $("#procedureGrid").jsGrid("insertItem", {'name' : resp['name'], 'objuuid' : resp['objuuid']});
        }
    });
}

var addControllerHost = function(objuuid) {
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            $("#hostGrid").jsGrid("insertItem", {'name' : resp['name'], 'objuuid' : resp['objuuid'], 'host' : resp['host']});
        }
    });
}

var executeController = function() {
    document.getElementById('body').innerHTML = '<div id="controllerTableDiv" style="width:inherit;height:inherit"><table id="controllerTable"></table></div><div id="procedureResultAccordion" style="display:none"></div>';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    initAttributes();
    addAttributeText('Controller UUID', 'objuuid');
    addAttributeTextBox('Controller Name', 'name');
    
    $.ajax({
        'url' : 'controller/ajax_get_tiles',
        'dataType' : 'json',
        'data' : {'objuuid' : inventoryObject.objuuid},
        'success' : function(resp) {
            var table = document.getElementById('controllerTable');
            var row;
            var cell;
            
            for(var y = 0; y < resp.procedures.length; y++) {
                row = table.insertRow(-1);
                
                for(var x = 0; x < resp.hosts.length; x++) {
                    cell = row.insertCell(-1);
                    cell.setAttribute('id', 'controller-cell-' + resp.hosts[x].objuuid + '-' + resp.procedures[y].objuuid);
                    cell.setAttribute('data-host-objuuid', resp.hosts[x].objuuid);
                    cell.setAttribute('data-host-name', resp.hosts[x].name);
                    cell.setAttribute('data-host-host', resp.hosts[x].host);
                    cell.setAttribute('data-procedure-objuuid', resp.procedures[y].objuuid);
                    cell.setAttribute('data-procedure-name', resp.procedures[y].name);
                    cell.setAttribute('data-selected', 'false');
                    cell.setAttribute('onclick', 'cellClick(this)');
                    cell.setAttribute('class', 'controllerCell');
                    
                    cell.innerHTML = cell.getAttribute('data-procedure-name') + '<br>';
                    cell.innerHTML += cell.getAttribute('data-host-name') + '<br>';
                    cell.innerHTML += cell.getAttribute('data-host-host');
                    
                    cell.style.borderStyle = 'solid';
                    cell.style.borderColor = '#000';
                    cell.style.padding = '10px';
                    
                    document.getElementById('procedureResultAccordion').innerHTML += '<div id="section-header-' + resp.hosts[x].objuuid + '-' + resp.procedures[y].objuuid + '"></div>';
                    document.getElementById('procedureResultAccordion').innerHTML += '<pre><code id="section-body-' + resp.hosts[x].objuuid + '-' + resp.procedures[y].objuuid + '"></code></pre>';
                }
            }
            
            updateControllerStateData();
            updateControllerTimer();
            
            $("#procedureResultAccordion").accordion({
                collapsible: true,
                heightStyle: "content",
                active: false
            });
        }
    });
    
    link = document.createElement("a");
    link.setAttribute("href", "#");
    link.innerHTML = "Details";
    cell = document.createElement("li");
    cell.setAttribute('onclick', 'toggleControllerDetails()');
    cell.appendChild(link);
    document.getElementById('menuBarDynamic').appendChild(cell);
    
    link = document.createElement("a");
    link.setAttribute("href", "#");
    link.innerHTML = "Run All";
    cell = document.createElement("li");
    cell.setAttribute('onclick', 'executeAllProcedures()');
    cell.appendChild(link);
    document.getElementById('menuBarDynamic').appendChild(cell);
    
    link = document.createElement("a");
    link.setAttribute("href", "#");
    link.innerHTML = "Run Selected";
    cell = document.createElement("li");
    cell.setAttribute('onclick', 'executeSelectedProcedures()');
    cell.appendChild(link);
    document.getElementById('menuBarDynamic').appendChild(cell);
    
    link = document.createElement("a");
    link.setAttribute("href", "#");
    link.innerHTML = "Select All";
    cell = document.createElement("li");
    cell.setAttribute('onclick', 'selectAllProcedures()');
    cell.appendChild(link);
    document.getElementById('menuBarDynamic').appendChild(cell);
    
    link = document.createElement("a");
    link.setAttribute("href", "#");
    link.innerHTML = "Clear Selected";
    cell = document.createElement("li");
    cell.setAttribute('onclick', 'deselectAllProcedures()');
    cell.appendChild(link);
    document.getElementById('menuBarDynamic').appendChild(cell);
}

var toggleControllerDetails = function(item) {
    if(showControllerDetails) {
        document.getElementById('controllerTableDiv').style.display = 'block';
        document.getElementById('procedureResultAccordion').style.display = 'none';
        showControllerDetails = false;
    } else {
        document.getElementById('controllerTableDiv').style.display = 'none';
        document.getElementById('procedureResultAccordion').style.display = 'block';
        showControllerDetails = true;
        
        $('#controllerTable tr').each(function(){
            $(this).find('td').each(function(){
                if($(this)[0].id) {
                    if($(this)[0].attributes['data-selected'].value == 'true') {
                        document.getElementById('section-header-' + $(this)[0].attributes['data-host-objuuid'].value + '-' + $(this)[0].attributes['data-procedure-objuuid'].value).style.display = 'block';
                    } else {
                        document.getElementById('section-header-' + $(this)[0].attributes['data-host-objuuid'].value + '-' + $(this)[0].attributes['data-procedure-objuuid'].value).style.display = 'none';
                    }
                }
            });
        });
    }
}

var cellClick = function(item) {
    if(item.getAttribute('data-selected') == 'true') {
        item.setAttribute('data-selected', false);
        item.style.borderStyle = 'solid';
        item.style.borderColor = '#000';
    } else {
        item.setAttribute('data-selected', true);
        item.style.borderStyle = 'solid';
        item.style.borderColor = '#FFF';
    }
}

var executeAllProcedures = function() {
    $('#controllerTable tr').each(function(){
        $(this).find('td').each(function(){
            if($(this)[0].id) {
                addMessage("queuing " + $(this)[0].attributes['data-procedure-name'].value + " on " + $(this)[0].attributes['data-host-name'].value + "...");
            
                $.ajax({
                    'url' : 'procedure/ajax_queue_procedure',
                    'dataType' : 'json',
                    'data' : {
                        'prcuuid' : $(this)[0].attributes['data-procedure-objuuid'].value, 
                        'hstuuid' : $(this)[0].attributes['data-host-objuuid'].value
                    },
                });
            }
        });
    });
}

var executeSelectedProcedures = function() {
    $('#controllerTable tr').each(function(){
        $(this).find('td').each(function(){
            if($(this)[0].id) {
                if($(this)[0].attributes['data-selected'].value == 'true') {
                    addMessage("queuing " + $(this)[0].attributes['data-procedure-name'].value + " on " + $(this)[0].attributes['data-host-name'].value + "...");
                    
                    $.ajax({
                        'url' : 'procedure/ajax_queue_procedure',
                        'dataType' : 'json',
                        'data' : {
                            'prcuuid' : $(this)[0].attributes['data-procedure-objuuid'].value, 
                            'hstuuid' : $(this)[0].attributes['data-host-objuuid'].value
                        },
                    });
                }
            }
        });
    });
}

var selectAllProcedures = function() {
    $('#controllerTable tr').each(function(){
        $(this).find('td').each(function(){
            if($(this)[0].id) {
                document.getElementById($(this)[0].id).setAttribute('data-selected', true);
                document.getElementById($(this)[0].id).style.borderStyle = 'solid';
                document.getElementById($(this)[0].id).style.borderColor = '#FFF';
            }
        });
    });
}

var deselectAllProcedures = function() {
    $('#controllerTable tr').each(function(){
        $(this).find('td').each(function(){
            if($(this)[0].id) {
                document.getElementById($(this)[0].id).setAttribute('data-selected', false);
                document.getElementById($(this)[0].id).style.borderStyle = 'solid';
                document.getElementById($(this)[0].id).style.borderColor = '#000';
            }
        });
    });
}

var drawCells = function(resultItems) {
    var cell;
    var currentTime = (new Date).getTime() / 1000;

    for(var i = 0; i < resultItems.length; i++) {
        cell = document.getElementById('controller-cell-' + resultItems[i].host.objuuid + '-' + resultItems[i].procedure.objuuid);

        if(resultItems[i].stop) {
            if(currentTime - resultItems[i].stop > 60) {
                cell.style.color = '#' + resultItems[i].status.sfg;
                cell.style.backgroundColor = '#' + resultItems[i].status.sbg;
            } else {
                cell.style.color = '#' + resultItems[i].status.cfg;
                cell.style.backgroundColor = '#' + resultItems[i].status.cbg;
            }
            cell.innerHTML = cell.getAttribute('data-procedure-name') + '<br>';
            cell.innerHTML += cell.getAttribute('data-host-name') + '<br>';
            cell.innerHTML += cell.getAttribute('data-host-host') + '<br>';
            cell.innerHTML += resultItems[i].status.name;
        } else {
            cell.style.color = '#' + resultItems[i].status.cfg;
            cell.style.backgroundColor = '#' + resultItems[i].status.cbg;
            
            cell.innerHTML = cell.getAttribute('data-procedure-name') + '<br>';
            cell.innerHTML += cell.getAttribute('data-host-name') + '<br>';
            cell.innerHTML += cell.getAttribute('data-host-host') + '<br>';
            cell.innerHTML += resultItems[i].status.name;
        }
        
        viewProcedureResult(resultItems[i]);
    }
}

var updateControllerTimer = function() {
    if(document.getElementById('controllerTable')) {
        $.ajax({
            'url' : 'flags/ajax_get',
            'dataType' : 'json',
            'data' : {
                //'key' : 'controller-' + inventoryObject.objuuid
                'key' : 'results'
            },
            'success' : function(resp) {
                if(controllerStateFlag != resp.value) {
                    controllerStateFlag = resp.value;
                    updateControllerStateData();
                } else {
                    if(controllerStateData)
                        drawCells(controllerStateData);
                }
                setTimeout(updateControllerTimer, 2000);
            },
        });
    }
}

var updateControllerStateData = function() {
    $.ajax({
        'url' : 'results/ajax_get_controller',
        'dataType' : 'json',
        'data' : {'objuuid' : inventoryObject.objuuid},
        'success' : function(resp) {
            controllerStateData = resp;
            drawCells(controllerStateData);
        }
    });
}

var editController = function() {
    initAttributes();
    addAttributeText('Controller UUID', 'objuuid');
    addAttributeTextBox('Controller Name', 'name');
    
    document.getElementById('body').innerHTML = '<div id="procedureGrid" style="padding:10px"></div><div id="hostGrid" style="padding:10px"></div>';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    $("#procedureGrid").jsGrid({
        height: "calc(50% - 5px)",
        width: "calc(100% - 5px)",
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
                    url: "/controller/ajax_get_procedure_grid",
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
            {name : "name", type : "text", title : "Procedure Name"},
            {name : "objuuid", type : "text", visible: false},
            {type : "control" }
        ],
 
        onRefreshed: function() {
            var $gridData = $("#procedureGrid .jsgrid-grid-body tbody");
 
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
                    
                    inventoryObject['procedures'] = [];
                    for(var i in items) {
                        inventoryObject['procedures'].push(items[i].objuuid);
                    }
                    inventoryObject['changed'] = true;
                }
            });
        }
    });
    
    $("#hostGrid").jsGrid({
        height: "calc(50% - 5px)",
        width: "calc(100% - 5px)",
        autoload: true,
        
        deleteButton: true,
        confirmDeleting: false,
        
        rowClass: function(item, itemIndex) {
            return "client-" + itemIndex;
        },
        
        rowDoubleClick: function(args) {
            loadAndEditHost(args.item.objuuid);
        },
 
        controller: {
            loadData: function(filter) {
                return $.ajax({
                    type: "GET",
                    url: "/controller/ajax_get_host_grid",
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
 
        onRefreshed: function() {
            var $gridData = $("#hostGrid .jsgrid-grid-body tbody");
 
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
                    
                    inventoryObject['hosts'] = [];
                    for(var i in items) {
                        inventoryObject['hosts'].push(items[i].objuuid);
                    }
                    inventoryObject['changed'] = true;
                }
            });
        }
    });
}

var viewProcedureResult = function(result) {
    document.getElementById('section-header-' + result.host.objuuid + '-' + result.procedure.objuuid).innerHTML = result.procedure.name + '<br>' + result.host.name + '<br>' + result.host.host + '<br>' + result.status.name;
    
    document.getElementById('section-body-' + result.host.objuuid + '-' + result.procedure.objuuid).innerHTML = '<table id="section-body-procedure-header-' + result.host.objuuid + '-' + result.procedure.objuuid + '"></table>';
    
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
    row.insertCell(-1).innerHTML = result.start;
    
    row = table.insertRow(-1);
    row.insertCell(-1).innerHTML = '<b>Procedure Stop:</b>';
    row.insertCell(-1).innerHTML = result.stop;
    
    row = table.insertRow(-1);
    row.insertCell(-1).innerHTML = '<b>Procedure Status:</b>';
    row.insertCell(-1).innerHTML = result.status.name;
    
    document.getElementById('section-body-' + result.host.objuuid + '-' + result.procedure.objuuid).innerHTML += '<br><br><table id="section-body-rfcs-' + result.host.objuuid + '-' + result.procedure.objuuid + '"></table>';
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
        document.getElementById('section-body-' + result.host.objuuid + '-' + result.procedure.objuuid).innerHTML += '<br><br><table id="section-body-task-header-' + i + '-' + result.host.objuuid + '-' + result.procedure.objuuid + '"></table>';
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
        
        document.getElementById('section-body-' + result.host.objuuid + '-' + result.procedure.objuuid).innerHTML += '<br>';
    }
    
    document.getElementById('section-header-' + result.host.objuuid + '-' + result.procedure.objuuid).style.color = '#' + result.status.cfg;
    document.getElementById('section-header-' + result.host.objuuid + '-' + result.procedure.objuuid).style.backgroundColor = '#' + result.status.cbg;
}
