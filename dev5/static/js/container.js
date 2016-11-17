var editContainer = function() {
    document.getElementById('body').innerHTML = '';
    
    initAttributes();
    addAttributeText('Container UUID', 'objuuid');
    addAttributeTextBox('Container Name', 'name');
}