var term;
var outputBuffer = '';
var sending = false;
var receiving = false;

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

var launchTerminal = function() {
    document.getElementById('body').innerHTML = '<div id="terminal"></div>';
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
    
    term = new Terminal({
        cols: 80,
        rows: 24,
        useStyle: true,
        screenKeys: true,
        cursorBlink: true
    });

    term.on('data', function(data) {
        outputBuffer += data;
    });

    term.on('title', function(title) {
        document.title = title;
    });

    term.open(document.getElementById('terminal'));
    
    $.ajax({
        'url' : 'terminal/ajax_create_session',
        'dataType' : 'json',
        'data' : {
            'hstuuid' : inventoryObject.objuuid
        }
    });
    
    setTimeout(terminalTimer, 1000);
}

var recvTerminalData = function() {
    if(!(receiving)) {
        receiving = true;
        $.ajax({
            'url' : 'terminal/ajax_recv',
            'data' : {
                'hstuuid' : inventoryObject.objuuid
            },
            'success' : function(resp) {
                receiving = false;
                if(resp != '') term.write(resp);
            },
            'error' : function() {
                receiving = false;
            }
        });
    }
}

var sendTerminalData = function() {
    if(outputBuffer != '' && !(sending)) {
        sending = true;
        var buffer = outputBuffer;
        outputBuffer = '';
        
        $.ajax({
            'url' : 'terminal/ajax_send',
            'dataType' : 'json',
            'data' : {
                'hstuuid' : inventoryObject.objuuid,
                'buffer' : buffer
            },
            'success' : function() {
                sending = false;
            },
            'error' : function() {
                sending = false;
            }
        });
    }
}

var terminalTimer = function() {
    if(document.getElementById('terminal')) {
        recvTerminalData();
        sendTerminalData();
        setTimeout(terminalTimer, 1000);
    } else {
        $.ajax({
            'url' : 'terminal/ajax_destroy_session',
            'dataType' : 'json',
            'data' : {
                'hstuuid' : inventoryObject.objuuid
            }
        });
    }
}