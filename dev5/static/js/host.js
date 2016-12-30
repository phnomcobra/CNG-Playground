var editHost = function() {
    document.getElementById('body').innerHTML = '';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    initAttributes();
    addAttributeText('Host UUID', 'objuuid');
    addAttributeTextBox('Name', 'name');
    addAttributeTextBox('Host', 'host');
    
    $.ajax({
        'url' : 'console/ajax_get_consoles',
        'dataType' : 'json',
        'success' : function(resp) {
            var radioButtons = [];
            for(var i = 0; i < resp.length; i++) {
                radioButtons.push({'name' : resp[i].name, 'value' : resp[i].objuuid});
            }
            addAttributeRadioGroup('Console', 'console', radioButtons)
        }
    });
}

var loadAndEditHost = function(objuuid) {
    document.getElementById('body').innerHTML = '';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    $.ajax({
        'url' : 'inventory/ajax_get_object',
        'dataType' : 'json',
        'data' : {'objuuid' : objuuid},
        'success' : function(resp) {
            inventoryObject = resp;
            editHost();
            expandToNode(inventoryObject.objuuid);
        }
    });
}
