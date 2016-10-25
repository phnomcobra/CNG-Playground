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
        'tree/ajax_roots' :
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

$('#inventory').on("select_node.jstree", function(event, data){
    var evt =  window.event || event;
    if(evt.which || evt.button == 1){
        $.ajax({
            'url' : 'tree/ajax_select',
            'dataType' : 'json',
            'data' : {
                'id' : data.node.id
            },
            'success' : function(resp) {
                console.log("select success", resp);
                $('#inventory').jstree('refresh');
                tabUpdate();
            },
            'error' : function(resp, status, error) {
                console.log("select failure", resp, status, error);
            }
        });
    }
});

$('#inventory').on('hover_node.jstree', function (evt, data) {
        $.ajax({
            'url' : 'tree/ajax_context',
            'dataType' : 'json',
            'data' : {
                'id' : data.node.id
            },
            'success' : function(resp) {
                contextMenu = {};
                for(var item in resp) {
                    contextMenu[item] = {
                        'label' : resp[item]['label'],
                        'option' : resp[item]['option'],
                        'action' : function (obj) {
                            $.ajax({
                                'url' : 'tree/ajax_context_select',
                                'dataType' : 'json',
                                'data' : {
                                    'id' : data.node.id,
                                    'option' : obj.item.option
                                },
                                'success' : function(resp) {
                                    console.log("console select success", resp);
                                    $('#inventory').jstree('refresh');
                                    tabUpdate();
                                },
                                'error' : function(resp, status, error) {
                                    console.log("context select failure", resp, status, error);
                                }
                            });
                        }
                    }
                }
            },
            'error' : function(resp, status, error) {
                console.log("context failure", resp, status, error);
            }
        });
    }
);

$('#inventory').on("move_node.jstree", function(event, data){
        $.ajax({
            'url' : 'tree/ajax_move',
            'dataType' : 'json',
            'data' : {
                'id' : data.node.id,
                'parent' : data.node.parent
            },
            'success' : function(resp) {
                console.log("move success", resp);
            },
            'error' : function(resp, status, error) {
                console.log("move failure", resp, status, error);
                $('#inventory').jstree('refresh');
            }
        });
});

var tabUpdate = function () {
    $.ajax({
            'url' : 'tree/ajax_get_tabs',
            'dataType' : 'json',
            'success' : function(resp) {
                console.log("get tabs success", resp);
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
                                console.log("tab load success", resp);
                                document.getElementById(resp['item']).innerHTML = resp['resp'];
                            },
                            'error' : function(resp, status, error) {
                                console.log("tab load failure", resp, status, error);
                            }
                        });
                    
                }
                tabHTML += '</tr></table>';
                document.getElementById('handles').innerHTML = tabHTML;
            },
            'error' : function(resp, status, error) {
                console.log("get tabs failure", resp, status, error);
                document.getElementById('handles').innerHTML = '';
            }
        });
};

var tabSelect = function (item) {
    console.log(item);
    $('#bodies').find('div').each(function(){
        console.log($(this));
        if($(this).attr('id') == item) {
            $(this)[0].style.display = 'block';
        } else {
            $(this)[0].style.display = 'none';
        }
    });
};

var tabClose = function (item) {
    $.ajax({
            'url' : 'tree/ajax_close_tab',
            'dataType' : 'json',
            'data' : {
                'item' : item
            },
            'success' : function(resp) {
                console.log("tab close success", resp);
                tabUpdate();
            },
            'error' : function(resp, status, error) {
                console.log("tab close failure", resp, status, error);
            }
        });
    
};
