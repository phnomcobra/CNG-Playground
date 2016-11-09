var contextMenu = {};
var tabs = {};
var saving = false;

 $('#inventory').jstree({
'plugins' : ['contextmenu', 'dnd'],
'contextmenu': {
    'items': 
        function (obj) {
            return contextMenu;
        }
},
'core' : {
  'check_callback' : true,
  'data' : {
    'url' : function (node) {
      return node.id === '#' ?
        'inventory/ajax_roots' :
        'ajax_children';
    },
    'data' : function (node) {
      return { 'id' : node.id };
    },
    'dataType' : "json",
  },
'themes': {
        'theme': 'apple',
        'dots' : true,
        'icons': true,
        'url': "css/style.min.css"
    }
}
});

$('#inventory').on('select_node.jstree', function (evt, data) {
        contextMenu = {};
        
        $.ajax({
            'url' : 'inventory/ajax_context',
            'dataType' : 'json',
            'data' : {
                'id' : data.node.id
            },
            'success' : function(resp) {
                for(var item in resp) {
                    contextMenu[item] = {
                        'label' : resp[item]['label'],
                        'route' : resp[item]['route'],
                        'params' : resp[item]['params'],
                        'action' : function (obj) {
                            $.ajax({
                                'url' : obj.item.route,
                                'dataType' : 'json',
                                'data' : obj.item.params,
                                'success' : function(resp) {
                                    addMessage("console select success " + resp);
                                    $('#inventory').jstree('refresh');
                                    tabUpdate();
                                },
                                'error' : function(resp, status, error) {
                                    addMessage("console select failure " + resp);
                                }
                            });
                        }
                    }
                }
            },
            'error' : function(resp, status, error) {
                addMessage("context failure " + resp);
            }
        });
    }
);

$('#inventory').on("move_node.jstree", function(event, data){
        $.ajax({
            'url' : 'inventory/ajax_move',
            'dataType' : 'json',
            'data' : {
                'id' : data.node.id,
                'parent' : data.node.parent
            },
            'success' : function(resp) {
                addMessage("move success " + resp);
            },
            'error' : function(resp, status, error) {
                addMessage("move failure " + resp);
                $('#inventory').jstree('refresh');
            }
        });
});

var tabUpdate = function () {
    $.ajax({
            'url' : 'tabs/ajax_get_tabs',
            'dataType' : 'json',
            'success' : function(resp) {
                addMessage("get tabs success " + resp);
                for(item in resp['tabs']){
                        if(!document.getElementById('tab-' + resp['tabs'][item])) {
                            $.ajax({
                                'url' : 'inventory/ajax_get_object',
                                'dataType' : 'json',
                                'data' : {'id' : resp['tabs'][item]},
                                'success' : function(resp) {
                                    addMessage("tab load success " + resp);
                                    
                                    document.getElementById('bodies').innerHTML += '<div class="TabBody" id="tab-' + resp['objuuid'] + '"></div>';
                                    
                                    var row = document.getElementById("handles");
                                    var cell = row.insertCell(-1);
                                    cell.innerHTML = '<input type="button" value="' + 
                                                    resp['name'] + 
                                                    '" onclick=tabSelect("' + 
                                                    resp['objuuid'] + 
                                                    '"); /><input type="button" value="x" onclick=tabClose("' 
                                                    + resp['objuuid'] + '"); />';
                                    cell.id = 'handle-' + resp['objuuid'];
                                    
                                    if(resp['type'] == 'task') {
                                        document.getElementById('tab-' + resp['objuuid']).innerHTML = '<div id="ace-' + resp['objuuid'] + '"></div>';
                                    
                                        tabs[resp['objuuid']] = {'ace' : new ace.edit('ace-' + resp['objuuid'])};
                                        tabs[resp['objuuid']]['ace'].setTheme("ace/theme/twilight");
                                        tabs[resp['objuuid']]['ace'].session.setMode("ace/mode/python");
                                        tabs[resp['objuuid']]['ace'].setValue(resp['body']);
                                        tabs[resp['objuuid']]['ace'].selection.moveTo(0, 0);
                                        tabs[resp['objuuid']]['ace']['inventoryObject'] = resp;
                                        
                                        tabs[resp['objuuid']]['ace'].on('change', function(e, f) {
                                            if(!saving) {
                                                saving = true;
                                                f.inventoryObject.body = f.getValue();
                                                addMessage("saving " + f.inventoryObject['name']);
                                                $.ajax({
                                                    type: 'POST',
                                                    url: 'inventory/ajax_post_object',
                                                    data: JSON.stringify(f.inventoryObject),
                                                    contentType: "application/json",
                                                    success: function (resp) {saving = false; addMessage("save complete");},
                                                    failure: function (resp) {saving = false; addMessage("save failed!");},
                                                    dataType: 'json'
                                                });
                                            }
                                        });
                                    }
                                    
                                    tabSelect(resp['objuuid']);
                                },
                                'error' : function(resp, status, error) {
                                    addMessage("tab load failure " + resp);
                                }
                            });
                        }
                    
                }
            },
            'error' : function(resp, status, error) {
                addMessage("get tabs failure " + resp);
                document.getElementById('handles').innerHTML = '';
            }
        });
};

var tabSelect = function (item) {
    $('.TabBody').each(function(){
        if($(this).attr('id') == 'tab-' + item) {
            $(this)[0].style.display = 'block';
            
            if(item in tabs) {
                if('ace' in tabs[item]) {
                    //tabs[item]['ace'] = new ace.edit('ace-' + item);
                }
            }
        } else {
            $(this)[0].style.display = 'none';
        }
    });
};

var tabClose = function (item) {
    var handle = document.getElementById('handle-' + item);
    handle.parentNode.removeChild(handle);
    
    var tab = document.getElementById('tab-' + item);
    tab.parentNode.removeChild(tab);
    
    delete tabs[item];
    
    $.ajax({
        'url' : 'tabs/ajax_close_tab',
        'dataType' : 'json',
        'data' : {
            'id' : item
        },
        'success' : function(resp) {
            addMessage("tab close success " + resp);
        },
        'error' : function(resp, status, error) {
            addMessage("tab close failure " + resp);
        }
    });
};