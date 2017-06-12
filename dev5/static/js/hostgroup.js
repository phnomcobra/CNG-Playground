var loadAndEditHostGroup = function(objuuid) {
    document.getElementById('body').innerHTML = '';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'method': 'POST',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            inventoryObject = resp;
            editHostGroup();
            expandToNode(inventoryObject.objuuid);
        }
    });
}

var editHostGroup = function() {
    initAttributes();
    addAttributeText('Group UUID', 'objuuid');
    addAttributeTextBox('Group Name', 'name');
    
    document.title = inventoryObject.name;
    document.getElementById('bodyTitle').innerHTML = inventoryObject.type.toUpperCase() + ': ' + inventoryObject.name;
    $('.nav-tabs a[href="#body"]').tab('show');
    
    document.getElementById('body').innerHTML = '<div id="hostGrid" style="padding:10px"></div>';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    $("#hostGrid").jsGrid({
        width: "calc(100% - 5px)",
        height: "calc(100% - 5px)",
        autoload: true,
        
        deleteButton: true,
        confirmDeleting: false,
        sorting: false,
        
        editing: true,
        onItemEditing: function(args) {
            if(args.item.type == 'host') {
                loadAndEditHost(args.item.objuuid);
            } else if (args.item.type == 'host group') {
                loadAndEditHostGroup(args.item.objuuid);
            }
        },
        
        rowClass: function(item, itemIndex) {
            return "client-" + itemIndex;
        },
 
        controller: {
            loadData: function(filter) {
                return $.ajax({
                    type: "POST",
                    url: "/hostgroup/ajax_get_host_grid",
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
            {name : "type", type : "text", visible: false},
            {type : "control" }
        ],
    });
    
    loadRequiresGrid();
    loadProvidesGrid();
    
    setTimeout(refreshJSGrids, 1000);
}