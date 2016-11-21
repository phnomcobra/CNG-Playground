var populateControllerTable = function() {
    document.getElementById('body').innerHTML = '<table id="controllerTable"></table>';
    
    var controllerTable = document.getElementById("controllerTable");
    
    for(var rowIndex = 0; rowIndex < inventoryObject['procedures'].length + 4; rowIndex++) {
        var row = controllerTable.insertRow(rowIndex);
        
        for(var cellIndex = 0; cellIndex < inventoryObject['procedures'].length + 4; cellIndex++) {
            var cell = row.insertCell(cellIndex);
            
            cell.innerHTML = '<div id="controller-table-cell-' + cellIndex + '-' + rowIndex + '"></div>';
        }
    }
    
    for(var i = 0; i < inventoryObject['procedures'].length; i++) {
        document.getElementById('controller-table-cell-1-' + (i + 3)).innerHTML = '<div id="procedure-name-' + inventoryObject['procedures'][i] + '">Procedure UUID: ' + inventoryObject['procedures'][i] + '</div>';
        
        document.getElementById('controller-table-cell-0-' + (i + 3)).innerHTML = '<img src="images/x_icon.png" onclick="deleteControllerProcedure(' + i + ')" />';
        
        $.ajax({
            'url' : 'inventory/ajax_get_object',
            'dataType' : 'json',
            'data' : {'objuuid' : inventoryObject['procedures'][i]},
            'success' : function(resp) {
                document.getElementById('procedure-name-' + resp['objuuid']).innerHTML = resp['name'];
            }
        });
    }
    
    for(var i = 0; i < inventoryObject['hosts'].length; i++) {
        document.getElementById('controller-table-cell-' + (i + 2) + '-1').innerHTML = '<div id="host-name-' + inventoryObject['hosts'][i] + '">Host UUID: ' + inventoryObject['hosts'][i] + '</div>';
        
        document.getElementById('controller-table-cell-' + (i + 2) + '-0').innerHTML = '<img src="images/x_icon.png" onclick="deleteControllerHost(' + i + ')" />';
        
        $.ajax({
            'url' : 'inventory/ajax_get_object',
            'dataType' : 'json',
            'data' : {'objuuid' : inventoryObject['hosts'][i]},
            'success' : function(resp) {
                document.getElementById('host-name-' + resp['objuuid']).innerHTML = '<div>' + resp['name'] + '</div><div>' + resp['host'] + '</div>';
            }
        });
    }
}

var editController = function() {
    populateControllerTable();
    
    initAttributes();
    addAttributeText('Controller UUID', 'objuuid');
    addAttributeTextBox('Controller Name', 'name');
}

var deleteControllerProcedure = function(index) {
    inventoryObject['procedures'].splice(index, 1);
    inventoryObject['changed'] = true;
}

var deleteControllerHost = function(index) {
    inventoryObject['hosts'].splice(index, 1);
    inventoryObject['changed'] = true;
}

