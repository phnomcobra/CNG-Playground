var setCredentials = function() {
    document.getElementById('modal-header').innerHTML = '<h2>Set Credentials</h2>';
    document.getElementById('modal-body').innerHTML = '<table id="modalTable"></table>';
    
    var modalTable = document.getElementById('modalTable');
    var modalRow;
    var modalCell;
    
    modalRow = modalTable.insertRow(-1);
    
    modalCell = modalRow.insertCell(-1);
    modalCell.innerHTML = 'SSH Username';
    
    modalCell = modalRow.insertCell(-1);
    modalCell.innerHTML = '<input type="text" id="SSHUsername">';
    
    modalRow = modalTable.insertRow(-1);
    
    modalCell = modalRow.insertCell(-1);
    modalCell.innerHTML = 'SSH Password';
    
    modalCell = modalRow.insertCell(-1);
    modalCell.innerHTML = '<input type="password" id="SSHPassword">';
    
    modalRow = modalTable.insertRow(-1);
    
    modalCell = modalRow.insertCell(-1);
    modalCell.innerHTML = 'MySQL Username';
    
    modalCell = modalRow.insertCell(-1);
    modalCell.innerHTML = '<input type="text" id="MySQLUsername">';
    
    modalRow = modalTable.insertRow(-1);
    
    modalCell = modalRow.insertCell(-1);
    modalCell.innerHTML = 'MySQL Password';
    
    modalCell = modalRow.insertCell(-1);
    modalCell.innerHTML = '<input type="password" id="MySQLPassword">';
    
    document.getElementById('modal-body').innerHTML += '<button onclick="submitCredentials()">Submit</button>';
    document.getElementById('modal-body').innerHTML += '<button onclick="closeModal()">Close</button>';
    
    document.getElementById('modal-content').style.display = 'block';
}

var submitCredentials = function() {
    $.ajax({
        'url' : 'credentials/set_ssh_username',
        'data' : {'username' : document.getElementById('SSHUsername').value}
    });

    $.ajax({
        'url' : 'credentials/set_mysql_username',
        'data' : {'username' : document.getElementById('MySQLUsername').value}
    });

    $.ajax({
        'url' : 'credentials/set_ssh_password',
        'data' : {'b64str' : window.btoa(document.getElementById('SSHPassword').value)}
    });

    $.ajax({
        'url' : 'credentials/set_mysql_password',
        'data' : {'b64str' : window.btoa(document.getElementById('MySQLPassword').value)}
    });

    closeModal();
}

var closeModal = function() {
    document.getElementById('modal-header').innerHTML = '';
    document.getElementById('modal-body').innerHTML = '';
    document.getElementById('modal-footer').innerHTML = '';
    document.getElementById('modal-content').style.display='none';
}