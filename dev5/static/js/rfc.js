var editRFC = function() {
    document.getElementById('body').innerHTML = '<div id="aceInstance"></div>';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    initAttributes();
    addAttributeText('RFC UUID', 'objuuid');
    addAttributeTextBox('RFC Name', 'name');
    addAttributeTextBox('RFC Title', 'title');
    addAttributeTextBox('RFC Number', 'number');
    addAttributeTextArea('Description', 'description');
    addAttributeTextBox('POC Name', 'poc name');
    addAttributeTextBox('POC Email', 'poc email');
    addAttributeTextBox('POC Phone', 'poc phone');
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
            expandToNode(inventoryObject.objuuid);
        }
    });
}