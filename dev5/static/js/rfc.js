var editRFC = function() {
    document.getElementById('body').innerHTML = '';
    
    initAttributes();
    addAttributeText('RFC UUID', 'objuuid');
    addAttributeTextBox('RFC Name', 'name');
    addAttributeTextBox('RFC Title', 'title');
    addAttributeTextBox('RFC Number', 'number');
    addAttributeTextBox('POC Name', 'poc name');
    addAttributeTextBox('POC Email', 'poc email');
    addAttributeTextBox('POC Phone', 'poc phone');
    addAttributeTextArea('Description', 'description');
}

var loadAndEditRFC = function(objuuid) {
    document.getElementById('body').innerHTML = '';
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