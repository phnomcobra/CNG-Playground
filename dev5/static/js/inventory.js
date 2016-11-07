var contextMenu = {};

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
        $.ajax({
            'url' : 'inventory/ajax_context',
            'dataType' : 'json',
            'data' : {
                'id' : data.node.id
            },
            'success' : function(resp) {
                contextMenu = {};
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
            'url' : 'inventory/ajax_get_tabs',
            'dataType' : 'json',
            'success' : function(resp) {
                addMessage("get tabs success " + resp);
                document.getElementById('bodies').innerHTML = '';
                var tabHTML = '<table><tr>';
                for(item in resp){
                        tabHTML += '<td>';
                        tabHTML += '<input type="button" value="' + resp[item]['label'] + '" onclick=tabSelect("' + item + '"); />';
                        tabHTML += '<input type="button" value="x" onclick=tabClose("' + item + '"); />';
                        tabHTML +='</td>';
                    
                        document.getElementById('bodies').innerHTML += '<div id="' + item + '"></div>';
                        tabSelect(item);
                        
                        $.ajax({
                            'url' : resp[item]['route'],
                            'dataType' : 'json',
                            'data' : {
                                'item' : item
                            },
                            'success' : function(resp) {
                                addMessage("tab load success " + resp);
                                document.getElementById(resp['item']).innerHTML = resp['resp'];
                            },
                            'error' : function(resp, status, error) {
                                addMessage("tab load failure " + resp);
                            }
                        });
                    
                }
                tabHTML += '</tr></table>';
                document.getElementById('handles').innerHTML = tabHTML;
            },
            'error' : function(resp, status, error) {
                addMessage("get tabs failure " + resp);
                document.getElementById('handles').innerHTML = '';
            }
        });
};

var tabSelect = function (item) {
    $('#bodies').find('div').each(function(){
        if($(this).attr('id') == item) {
            $(this)[0].style.display = 'block';
        } else {
            $(this)[0].style.display = 'none';
        }
    });
};

var tabClose = function (item) {
    $.ajax({
            'url' : 'inventory/ajax_close_tab',
            'dataType' : 'json',
            'data' : {
                'item' : item
            },
            'success' : function(resp) {
                addMessage("tab close success " + resp);
                tabUpdate();
            },
            'error' : function(resp, status, error) {
                addMessage("tab close failure " + resp);
            }
        });
    
};
