var contextMenu = {};

var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $interval, $http) {
    /* $interval(function () {
            $http.post("textarea", $scope.textarea);
    }, 1000); */
}); 

 $('#demotree').jstree({
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
        'ajax_roots' :
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

$('#demotree').on("select_node.jstree", function(event, data){
    var evt =  window.event || event;
    if(evt.which || evt.button == 1){
        $.ajax({
            'url' : 'ajax_select',
            'dataType' : 'json',
            'data' : {
                'id' : data.node.id
            },
            'success' : function(resp) {
                console.log("select success", resp);
                $('#demotree').jstree('refresh');
            },
            'error' : function(resp, status, error) {
                console.log("select failure", resp, status, error);
            }
        });
    }
});

$('#demotree').on('hover_node.jstree', function (evt, data) {
        $.ajax({
            'url' : 'ajax_context',
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
                                'url' : 'ajax_context_select',
                                'dataType' : 'json',
                                'data' : {
                                    'id' : data.node.id,
                                    'option' : obj.item.option
                                },
                                'success' : function(resp) {
                                    console.log("console select success", resp);
                                    $('#demotree').jstree('refresh');
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

$('#demotree').on("move_node.jstree", function(event, data){
        $.ajax({
            'url' : 'ajax_move',
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
                $('#demotree').jstree('refresh');
            }
        });
});