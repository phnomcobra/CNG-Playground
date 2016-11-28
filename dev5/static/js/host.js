var editHost = function() {
    document.getElementById('body').innerHTML = '';
    
    initAttributes();
    addAttributeText('Host UUID', 'objuuid');
    addAttributeTextBox('Name', 'name');
    addAttributeTextBox('Host', 'host');
}

var loadAndEditHost = function(objuuid) {
    document.getElementById('body').innerHTML = '';
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            inventoryObject = resp;
            editHost();
        }
    });
}
