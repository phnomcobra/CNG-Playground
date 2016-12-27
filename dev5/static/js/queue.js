var drawQueue = function(resp) {
    queue = document.getElementById('queue');
    queue.innerHTML = '';
    
    for(var jobuuid in resp) {
        queueItem = document.createElement('div');
        queueItem.setAttribute('id', 'jobuuid-' + jobuuid);
        queueItem.setAttribute('data-jobuuid', jobuuid);
        queueItem.setAttribute('class', 'panel panel-default');
        queueItem.setAttribute('style', 'width:100%');

        progressInnerDIV = document.createElement('div');
        progressInnerDIV.setAttribute('class', 'progress-bar');
        progressInnerDIV.setAttribute('role', 'progressbar');
        progressInnerDIV.setAttribute('style', 'width:' + Math.round(resp[jobuuid].progress * 100.0) + '%');
        progressInnerDIV.innerHTML = Math.round(resp[jobuuid].progress * 100.0) + '%';

        progressOuterDIV = document.createElement('div');
        progressOuterDIV.setAttribute('class', 'progress');
        progressOuterDIV.appendChild(progressInnerDIV);
        
        panelHeading = document.createElement('div');
        panelHeading.setAttribute('class', 'panel-heading');
        panelHeading.innerHTML = resp[jobuuid].name + '@' + resp[jobuuid].host;
        
        panelBody = document.createElement('div');
        panelBody.setAttribute('class', 'panel-body');
        
        panelTable = document.createElement('table');
        panelTable.setAttribute('class', 'table');
        
        row = panelTable.insertRow(-1);
        cell = row.insertCell(-1);
        cell.innerHTML = "Message";
        cell = row.insertCell(-1);
        cell.innerHTML = resp[jobuuid].message;
        
        row = panelTable.insertRow(-1);
        cell = row.insertCell(-1);
        cell.innerHTML = "Start Time";
        cell = row.insertCell(-1);
        cell.innerHTML = new Date(resp[jobuuid]['start time'] * 1000);
        
        queueItem.appendChild(panelHeading);
        queueItem.appendChild(panelBody);
        panelBody.appendChild(progressOuterDIV);
        panelBody.appendChild(panelTable);

        queue.appendChild(queueItem);
    }
}

var updateQueueState = function() {
    $.ajax({
        'url' : 'procedure/ajax_get_queue_grid',
        'dataType' : 'json',
        'success' : function(resp) {
            drawQueue(resp);
        }
    });
}