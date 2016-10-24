var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $interval, $http) {
    /* $interval(function () {
            $http.post("textarea", $scope.textarea);
    }, 1000); */
}); 

 $('#demotree').jstree({
'plugins' : [
    'contextmenu', 'checkbox'
  ],
'core' : {
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
},
'contextmenu':{         
    'items': function (node) {
        return {
            'Create': {
                'separator_before': false,
                'separator_after': false,
                'label': 'Create',
                'action': function () { 
                    $.ajax({
                        'url' : 'ajax_create',
                        'dataType' : 'json',
                        'data' : {
                            'id' : node.id
                        },
                        'success' : function(resp) {
                            console.log("create success", resp);
                        },
                        'error' : function(resp, status, error) {
                            console.log("create failure", resp, status, error);
                        }
                    });
                }
            },
            'Refresh': {
                'separator_before': false,
                'separator_after': false,
                'label': 'Refresh',
                'action': function () { 
                    $("#demotree").jstree(true).refresh();
                    console.log("refresh success");
                }
            }
        };
    }
}
}).on("select_node.jstree", function(evt, data){
        $.ajax({
            'url' : 'ajax_select',
            'dataType' : 'json',
            'data' : {
                'id' : data.node.id
            },
            'success' : function(resp) {
                console.log("select success", resp);
            },
            'error' : function(resp, status, error) {
                console.log("select failure", resp, status, error);
            }
        });
    }
);