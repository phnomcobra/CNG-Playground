var controllerStateFlag = null;
var controllerStateData;

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
    document.getElementById('body').innerHTML = '<div id="controllerCommandsTable"></div><table id="controllerTable"></table>'
    document.getElementById('menuBarDynamic').innerHTML = '';
     document.getElementById('body').style.backgroundColor = '#000';
    
    initAttributes();
    addAttributeText('Controller UUID', 'objuuid');
    addAttributeTextBox('Controller Name', 'name');
    
    $.ajax({
        'url' : 'controller/ajax_get_tiles',
        'dataType' : 'json',
        'data' : {'objuuid' : inventoryObject.objuuid},
        'success' : function(resp) {
            var controllerTable = document.getElementById('controllerTable');
            var row;
            var cell;
            
            for(var y = 0; y < resp.procedures.length; y++) {
                row = controllerTable.insertRow(-1);
                
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
                    
                    $.ajax({
                        'url' : 'procedure/ajax_get_related_procedures',
                        'dataType' : 'json',
                        'hstuuid' : resp.hosts[x].objuuid,
                        'hstname' : resp.hosts[x].name,
                        'hsthost' : resp.hosts[x].host,
                        'prcuuid' : resp.procedures[y].objuuid,
                        'data' : {'objuuid' : resp.procedures[y].objuuid},
                        'success' : function(resp) {
                            for(var i = 0; i < resp.length; i++) {
                                cell = document.createElement("DIV");
                                cell.innerHTML = resp[i].name + '<br>' + this.hstname;
                                cell.setAttribute('data-host-objuuid', this.hstuuid);
                                cell.setAttribute('data-procedure-objuuid', resp[i].objuuid);
                                cell.setAttribute('class', 'controllerCommandCell');
                                cell.setAttribute('onclick', 'executeRelatedProcedure(this)');
                                cell.setAttribute('style', 'display:none');
                                cell.setAttribute('name', 'controller-command-' + this.prcuuid + '-' + this.hstuuid);
                                document.getElementById('controllerCommandsTable').appendChild(cell);
                            }
                        }
                    });
                }
            }
            
            updateControllerStateData();
            updateControllerTimer();
        }
    });
    
    cell = document.createElement("DIV");
    cell.innerHTML = "Run All";
    cell.setAttribute('class', 'menuBarItem');
    cell.setAttribute('onclick', 'executeAllProcedures()');
    document.getElementById('menuBarDynamic').appendChild(cell);
    
    cell = document.createElement("DIV");
    cell.innerHTML = "Run Selected";
    cell.setAttribute('class', 'menuBarItem');
    cell.setAttribute('onclick', 'executeSelectedProcedures()');
    document.getElementById('menuBarDynamic').appendChild(cell);
    
    cell = document.createElement("DIV");
    cell.innerHTML = "Select All";
    cell.setAttribute('class', 'menuBarItem');
    cell.setAttribute('onclick', 'selectAllProcedures()');
    document.getElementById('menuBarDynamic').appendChild(cell);
    
    cell = document.createElement("DIV");
    cell.innerHTML = "Deselect All";
    cell.setAttribute('class', 'menuBarItem');
    cell.setAttribute('onclick', 'deselectAllProcedures()');
    document.getElementById('menuBarDynamic').appendChild(cell);
}

var cellClick = function(item) {
    if(item.getAttribute('data-selected') == 'true') {
        item.setAttribute('data-selected', false);
        item.style.borderStyle = 'solid';
        item.style.borderColor = '#000';
        
        var commandCells = document.getElementsByName('controller-command-' + item.getAttribute('data-procedure-objuuid') + '-' + item.getAttribute('data-host-objuuid'));
        for(var i = 0; i < commandCells.length; i++) {
            commandCells[i].setAttribute('style', 'display:none');
        }
    } else {
        item.setAttribute('data-selected', true);
        item.style.borderStyle = 'solid';
        item.style.borderColor = '#FFF';
                  
        var commandCells = document.getElementsByName('controller-command-' + item.getAttribute('data-procedure-objuuid') + '-' + item.getAttribute('data-host-objuuid'));
        for(var i = 0; i < commandCells.length; i++) {
            commandCells[i].setAttribute('style', 'display:block');
        }
    }
}

var executeAllProcedures = function() {
    $('#controllerTable tr').each(function(){
        $(this).find('td').each(function(){
            addMessage("executing " + $(this)[0].attributes['data-procedure-name'].value + " on " + $(this)[0].attributes['data-host-name'].value + "...");
            
            $.ajax({
                'url' : 'procedure/ajax_execute_procedure',
                'dataType' : 'json',
                'data' : {
                    'prcuuid' : $(this)[0].attributes['data-procedure-objuuid'].value, 
                    'hstuuid' : $(this)[0].attributes['data-host-objuuid'].value
                }
            });
        });
    });
}

var executeSelectedProcedures = function() {
    $('#controllerTable tr').each(function(){
        $(this).find('td').each(function(){
            if($(this)[0].attributes['data-selected'].value == 'true') {
                addMessage("executing " + $(this)[0].attributes['data-procedure-name'].value + " on " + $(this)[0].attributes['data-host-name'].value + "...");
            
                $.ajax({
                    'url' : 'procedure/ajax_execute_procedure',
                    'dataType' : 'json',
                    'data' : {
                        'prcuuid' : $(this)[0].attributes['data-procedure-objuuid'].value, 
                        'hstuuid' : $(this)[0].attributes['data-host-objuuid'].value
                    }
                });
            }
        });
    });
}

var selectAllProcedures = function() {
    $('#controllerTable tr').each(function(){
        $(this).find('td').each(function(){
            document.getElementById($(this)[0].id).setAttribute('data-selected', true);
            document.getElementById($(this)[0].id).style.borderStyle = 'solid';
            document.getElementById($(this)[0].id).style.borderColor = '#FFF';
        });
    });
    
    var commandCells = document.getElementsByClassName('controllerCommandCell');
    for(var i = 0; i < commandCells.length; i++) {
        commandCells[i].setAttribute('style', 'display:block');
    }
}

var deselectAllProcedures = function() {
    $('#controllerTable tr').each(function(){
        $(this).find('td').each(function(){
            document.getElementById($(this)[0].id).setAttribute('data-selected', false);
            document.getElementById($(this)[0].id).style.borderStyle = 'solid';
            document.getElementById($(this)[0].id).style.borderColor = '#000';
        });
    });
    
    var commandCells = document.getElementsByClassName('controllerCommandCell');
    for(var i = 0; i < commandCells.length; i++) {
        commandCells[i].setAttribute('style', 'display:none');
    }
}

var executeRelatedProcedure = function(item) {
    addMessage("executing procedure...");
    $.ajax({
        'url' : 'procedure/ajax_execute_procedure',
        'dataType' : 'json',
        'data' : {'prcuuid' : item.getAttribute('data-procedure-objuuid'), 'hstuuid' : item.getAttribute('data-host-objuuid')}
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
            cell.innerHTML += resultItems[i].status.abbreviation + '<br>';
            cell.innerHTML += Math.round(currentTime - resultItems[i].stop);
        } else {
            cell.style.color = '#' + resultItems[i].status.cfg;
            cell.style.backgroundColor = '#' + resultItems[i].status.cbg;
            cell.innerHTML = cell.getAttribute('data-procedure-name') + '<br>';
            cell.innerHTML += cell.getAttribute('data-host-name') + '<br>';
            cell.innerHTML += cell.getAttribute('data-host-host') + '<br>';
            cell.innerHTML += resultItems[i].status.abbreviation;
        }
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
                setTimeout(updateControllerTimer, 1000);
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