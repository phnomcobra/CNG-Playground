var editStatusCode = function() {
    document.getElementById('body').innerHTML = '';
    
    initAttributes();
    addAttributeText('Status UUID', 'objuuid');
    addAttributeTextBox('Status Name', 'name');
    addAttributeTextBox('Status Alias', 'alias');
    addAttributeTextBox('Status Abbreviation', 'abbreviation');
    addAttributeTextBox('Status Code', 'code');
    addAttributeColor('Current Foreground Color', 'cfg');
    addAttributeColor('Current Background Color', 'cbg');
    addAttributeColor('Stale Foreground Color', 'sfg');
    addAttributeColor('Stale Background Color', 'sbg');
}