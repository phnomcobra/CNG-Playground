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
    document.getElementById('body').innerHTML = '<div id="taskGrid" style="padding:10px"></div><div id="RFCGrid" style="padding:10px;float:left"></div><div id="relatedProcedureGrid" style="padding:10px;margin-left:calc(50% - 5px)"></div>';
    
    $("#taskGrid").jsGrid({
        height: "calc(50% - 5px)",
        width: "calc(100% - 10px)",
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