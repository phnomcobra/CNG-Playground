#!/usr/bin/python
################################################################################
# VIEW
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# (614) 692 2050
#
# 11/14/2016 Original construction
################################################################################

def edit_view(description):
    return """<div id="procedureEditTabs">
    <ul>
        <li><a href="#tabs-tasks">Tasks</a></li>
        <li><a href="#tabs-procedures">Procedures</a></li>
        <li><a href="#tabs-rfcs">RFC</a></li>
        <li><a href="#tabs-description">Description</a></li>
    </ul>
    <div id="tabs-tasks">
        <table id="tasksTable"></table>
    </div>
    <div id="tabs-procedures">
        <table id="proceduresTable"></table>
    </div>
    <div id="tabs-RFCs">
        <table id="RFCsTable"></table>
    </div>
    <div id="tabs-description">
        <textarea id="procedureDescription" onchange="setInventoryKey('description', 'procedureDescription')" style="width:100%;height:100%;">{0}</textarea>
    </div>
</div>""".format(description)

def attribute_view(name, title, objuuid):
    return """<table>
    <tr>
        <td>Name</td>
        <td><input type="text" id="procedureName" onchange="setInventoryKey('name', 'procedureName')" placeholder="{0}"></input></td>
    </tr>
    <tr>
        <td>Title</td>
        <td><input type="text" id="procedureTitle" onchange="setInventoryKey('title', 'procedureTitle')" placeholder="{1}"></input></td>
    </tr>
    <tr>
        <td>UUID</td>
        <td>{2}</td>
    </tr>
</table>""".format(name, title, objuuid)