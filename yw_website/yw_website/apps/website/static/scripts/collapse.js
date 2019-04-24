function getLastDashItem(dashString)
{
    splitArray = dashString.split("-")
    return splitArray[splitArray.length-1]
}

function getFileTable(resIds)
{ 
    window.currentResources = resIds
    if(window.currentResources.constructor === Array)
    {
        if(resIds.length == 0)
        {   
            window.currentResources =  0
        }
        else
        {
            window.currentResources = window.currentResources.join(",")
        }
    }

    $.ajax({
        url: tableUrl + `?resources=${window.currentResources}`, 
        type: 'GET',
        contentType: false,
        success: function(html) {
            let table = $("#file-table");
            table.empty()
            table.append(html)
        },
        error: function(error) {
        }
    });
}

let collapseList = $("#collapse")
let collapseButtons = collapseList.find(".static-left");

for(let i = 0; i < collapseButtons.length; i++)
{
    jQueryButton = $(collapseButtons[i])
    let idNumber = getLastDashItem(jQueryButton.attr("id"))

    let collapseContent = collapseList.find("#collapse-content-" + idNumber)
    collapseContent.hide()

    let plus = jQueryButton.find("#expand-button-" + idNumber)
    let minus = jQueryButton.find("#collapse-button-" + idNumber)
    minus.hide()

    jQueryButton.click((event) => {
        if(!jQueryButton.children())
            return;

        collapseContent.slideToggle(150)
        plus.toggle()
        minus.toggle()
    });
}

let resources = $(".js-resource")
for(let i=0; i<resources.length; i++)
{
    let res = $(resources[i])
    let resId = getLastDashItem(res.attr("id"))
    
    res.click(function(){
        getFileTable(resId)
    });
}

let ports = $(".js-port")
for(let i=0; i< ports.length; i++)
{
    let port = $(ports[i])
    portId = getLastDashItem(port.attr("id"))

    let resources = $("#collapse-content-" + portId).find(".js-resource")
    let resIds = []
    for(let j=0; j<resources.length; j++)
    {
        let res = $(resources[j])
        resIds.push(getLastDashItem(res.attr("id")))
    }
    
    port.click(function(){
        getFileTable(resIds);
    });
}
