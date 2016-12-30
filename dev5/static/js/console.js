var editConsole = function() {
    document.getElementById('body').innerHTML = '<div id="aceInstance"></div>';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    initAttributes();
    addAttributeText('Console UUID', 'objuuid');
    addAttributeTextBox('Console Name', 'name');

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
}

var loadAndEditConsole = function(objuuid) {
    document.getElementById('body').innerHTML = '';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            inventoryObject = resp;
            editConsole();
            expandToNode(inventoryObject.objuuid);
        }
    });
}
