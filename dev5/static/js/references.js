var loadRequiresGrid = function(){
    $("#requiresGrid").jsGrid({
        width: "calc(100% - 5px)",
        height: "calc(50vh - 80px)",
        autoload: true,
        
        rowClick: function(args) {
            if(args.item.type == "host") {
                loadAndEditHost(args.item.objuuid);
            } else if(args.item.type == "console") {
                loadAndEditConsole(args.item.objuuid);
            } else if(args.item.type == "rfc") {
                loadAndEditRFC(args.item.objuuid);
            } else if(args.item.type == "task") {
                loadAndEditTask(args.item.objuuid);
            } else if(args.item.type == "procedure") {
                loadAndEditProcedure(args.item.objuuid);
            } else if(args.item.type == "controller") {
                loadAndEditController(args.item.objuuid);
            }
        },
        
        rowClass: function(item, itemIndex) {
            return "client-" + itemIndex;
        },
 
        controller: {
            loadData: function(filter) {
                return $.ajax({
                    type: "GET",
                    url: "/inventory/ajax_get_required_objects_grid",
                    data: {'objuuid' : inventoryObject.objuuid},
                    dataType: "JSON"
                });
            }
        },
       
        fields: [
            {name : "name", type : "text", title : "Requires"},
            {name : "type", type : "text", title : "Type"},
            {name : "objuuid", type : "text", visible: false}
        ],
    });
}

var loadProvidesGrid = function(){
    $("#providesGrid").jsGrid({
        width: "calc(100% - 5px)",
        height: "calc(50vh - 80px)",
        autoload: true,
        
        rowClick: function(args) {
            if(args.item.type == "host") {
                loadAndEditHost(args.item.objuuid);
            } else if(args.item.type == "console") {
                loadAndEditConsole(args.item.objuuid);
            } else if(args.item.type == "rfc") {
                loadAndEditRFC(args.item.objuuid);
            } else if(args.item.type == "task") {
                loadAndEditTask(args.item.objuuid);
            } else if(args.item.type == "procedure") {
                loadAndEditProcedure(args.item.objuuid);
            } else if(args.item.type == "controller") {
                loadAndEditController(args.item.objuuid);
            }
        },
        
        rowClass: function(item, itemIndex) {
            return "client-" + itemIndex;
        },
 
        controller: {
            loadData: function(filter) {
                return $.ajax({
                    type: "GET",
                    url: "/inventory/ajax_get_provided_objects_grid",
                    data: {'objuuid' : inventoryObject.objuuid},
                    dataType: "JSON"
                });
            }
        },
        
        fields: [
            {name : "name", type : "text", title : "Provides"},
            {name : "type", type : "text", title : "Type"},
            {name : "objuuid", type : "text", visible: false}
        ],
    });
}
