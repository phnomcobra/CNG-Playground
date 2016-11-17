var deleteProcedureTask = function(rowIndex) {
    inventoryObject['tasks'].splice(rowIndex, 1);
    inventoryObject['changed'] = true;
    populateTaskTable();
}

var deleteProcedureRFC = function(rowIndex) {
    inventoryObject['rfcs'].splice(rowIndex, 1);
    inventoryObject['changed'] = true;
    populateRFCTable();
}

var moveUpProcedureTask = function(rowIndex) {
    if(rowIndex > 0) {
        inventoryObject['tasks'][rowIndex] = inventoryObject['tasks'].splice(rowIndex - 1, 1, inventoryObject['tasks'][rowIndex])[0];
        inventoryObject['changed'] = true;
        populateTaskTable();
    }
}

var moveDownProcedureTask = function(rowIndex) {
    if(rowIndex < inventoryObject['tasks'].length - 1) {
        inventoryObject['tasks'][rowIndex] = inventoryObject['tasks'].splice(rowIndex + 1, 1, inventoryObject['tasks'][rowIndex])[0];
        inventoryObject['changed'] = true;
        populateTaskTable();
    }
}

var editProcedureRFCs = function() {
    initAttributes();
    addAttributeText('Procedure UUID', 'objuuid');
    addAttributeTextBox('Procedure Name', 'name');
    addAttributeTextBox('Procedure Title', 'title');
    
    populateRFCTable();
}

var populateRFCTable = function() {
    document.getElementById('body').innerHTML = '<table id="rfcTable"></table>';
    
    for(var rowIndex = 0; rowIndex < inventoryObject['rfcs'].length; rowIndex++) {
        createRFCTableRow(rowIndex, inventoryObject['rfcs'][rowIndex]);
    }
}

var createRFCTableRow = function (rowIndex, objuuid) {
    var rfcTable = document.getElementById("rfcTable");
    var rfcRow;
    var rfcCell;
    
    rfcRow = rfcTable.insertRow(rowIndex);
    
    rfcCell = rfcRow.insertCell(-1);
    rfcCell.innerHTML = '<div name="number-' + objuuid + '"><img src="images/throbber.gif"/></div>';
    
    rfcCell = rfcRow.insertCell(-1);
    rfcCell.innerHTML = '<table></table>';
    
    var tileRow;
    var tileCell;
    var tileTable = rfcCell.childNodes[0];
    
    tileRow = tileTable.insertRow(-1);
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<img src="images/edit_icon.png" onclick="loadAndEditRFC(&quot;' + objuuid + '&quot;)" />';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<b>Name</b>';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<div name="name-' + objuuid + '"><img src="images/throbber.gif"/></div>';
    
    
    tileRow = tileTable.insertRow(-1);
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<img src="images/x_icon.png" onclick="deleteProcedureRFC(' + rowIndex + ')" />';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<b>Title</b>';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<div name="title-' + objuuid + '"><img src="images/throbber.gif"/></div>';
    
    tileRow = tileTable.insertRow(-1);
    tileCell = tileRow.insertCell(-1);
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<b>POC Name</b>';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<div name="poc-name-' + objuuid + '"><img src="images/throbber.gif"/></div>';
    
    
    
    tileRow = tileTable.insertRow(-1);
    tileCell = tileRow.insertCell(-1);
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<b>POC Email</b>';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<div name="poc-email-' + objuuid + '"><img src="images/throbber.gif"/></div>';
    
    
    
    tileRow = tileTable.insertRow(-1);
    tileCell = tileRow.insertCell(-1);
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<b>POC Phone</b>';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<div name="poc-phone-' + objuuid + '"><img src="images/throbber.gif"/></div>';
    
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            var elements;
            
            elements = document.getElementsByName('name-' + objuuid);
            for(var element in elements) {elements[element].innerHTML = resp['name'];}
            
            elements = document.getElementsByName('number-' + objuuid);
            for(var element in elements) {elements[element].innerHTML = 'RFC ' + resp['number'];}
            
            elements = document.getElementsByName('title-' + objuuid);
            for(var element in elements) {elements[element].innerHTML = resp['title'];}
            
            elements = document.getElementsByName('poc-name-' + objuuid);
            for(var element in elements) {elements[element].innerHTML = resp['poc name'];}
            
            elements = document.getElementsByName('poc-email-' + objuuid);
            for(var element in elements) {elements[element].innerHTML = resp['poc email'];}
            
            elements = document.getElementsByName('poc-phone-' + objuuid);
            for(var element in elements) {elements[element].innerHTML = resp['poc phone'];}
        }
    });
}

var editProcedureTasks = function() {
    initAttributes();
    addAttributeText('Procedure UUID', 'objuuid');
    addAttributeTextBox('Procedure Name', 'name');
    addAttributeTextBox('Procedure Title', 'title');
    
    populateTaskTable();
}

var populateTaskTable = function() {
    document.getElementById('body').innerHTML = '<table id="taskTable"></table>';
    
    for(var rowIndex = 0; rowIndex < inventoryObject['tasks'].length; rowIndex++) {
        createTaskTableRow(rowIndex, inventoryObject['tasks'][rowIndex]);
    }
}

var editProcedureDescription = function() {
    initAttributes();
    addAttributeText('Procedure UUID', 'objuuid');
    addAttributeTextBox('Procedure Name', 'name');
    addAttributeTextBox('Procedure Title', 'title');
    
    document.getElementById('body').innerHTML = '<div id="aceInstance"></div>';
    var editor = new ace.edit(document.getElementById('aceInstance'));
    
    editor.setTheme("ace/theme/twilight");
    editor.session.setMode("ace/mode/text");
    editor.setValue(inventoryObject['description']);
    editor.selection.moveTo(0, 0);
    editor['inventoryObject'] = inventoryObject;
                                        
    editor.on('change', function(e, f) {
        f.inventoryObject['description'] = f.getValue();
        f.inventoryObject['changed'] = true;
    });
}

var createTaskTableRow = function (rowIndex, objuuid) {
    var taskTable = document.getElementById("taskTable");
    var taskRow;
    var taskCell;
    
    taskRow = taskTable.insertRow(rowIndex);
    
    taskCell = taskRow.insertCell(-1);
    taskCell.innerHTML = rowIndex;
    
    taskCell = taskRow.insertCell(-1);
    taskCell.innerHTML = '<table></table>';
    
    var tileRow;
    var tileCell;
    var tileTable = taskCell.childNodes[0];
    
    tileRow = tileTable.insertRow(-1);
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<img src="images/up_icon.png" onclick="moveUpProcedureTask(' + rowIndex + ')" />';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<img src="images/edit_icon.png" onclick="loadAndEditTask(&quot;' + objuuid + '&quot;)" />';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<div name="name-' + objuuid + '"><img src="images/throbber.gif"/></div>';
    
    tileRow = tileTable.insertRow(-1);
    
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<img src="images/down_icon.png" onclick="moveDownProcedureTask(' + rowIndex + ')" />';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = '<img src="images/x_icon.png" onclick="deleteProcedureTask(' + rowIndex + ')" />';
    
    tileCell = tileRow.insertCell(-1);
    tileCell.innerHTML = objuuid;
    
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            var elements = document.getElementsByName('name-' + objuuid);
            for(var element in elements) {elements[element].innerHTML = resp['name'];}
        }
    });
}