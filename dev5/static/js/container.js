var editContainer = function() {
    document.getElementById('body').innerHTML = '';
    document.getElementById('menuBarDynamic').innerHTML = '';
    
    initAttributes();
    addAttributeText('Container UUID', 'objuuid');
    addAttributeTextBox('Container Name', 'name');
}