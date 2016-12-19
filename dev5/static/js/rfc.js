var editRFC = function() {
    document.getElementById('body').innerHTML = '<div id="aceInstance"></div>';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    initAttributes();
    addAttributeText('RFC UUID', 'objuuid');
    addAttributeTextBox('RFC Name', 'name');
    addAttributeTextBox('RFC Title', 'title');
    addAttributeTextBox('RFC Number', 'number');
    addAttributeTextBox('POC Name', 'poc name');
    addAttributeTextBox('POC Email', 'poc email');
    addAttributeTextBox('POC Phone', 'poc phone');
    
    var editor = new ace.edit(document.getElementById('aceInstance'));
    
    editor.setTheme("ace/theme/twilight");
    editor.setValue(inventoryObject['description']);
    editor.selection.moveTo(0, 0);
    editor['inventoryObject'] = inventoryObject;
                                        
    editor.on('change', function(e, f) {
        f.inventoryObject['description'] = f.getValue();
        f.inventoryObject['changed'] = true;
    });
}

var loadAndEditRFC = function(objuuid) {
    document.getElementById('body').innerHTML = '<div id="aceInstance"></div>';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            inventoryObject = resp;
            editRFC();
        }
    });
}