function getLastDashItem(dashString)
{
    splitArray = dashString.split("-")
    return splitArray[splitArray.length-1]
}

function getFileTable(resIds)
{
    console.log(resIds)
 
    if(resIds.constructor === Array)
    {
        if(resIds.length == 0)
        {   
            resIds = 0
        }
        else
        {
            resIds = resIds.join(",")
        }
    }
    console.log(resIds)
    // console.log(tableUrl + "?resources=" + resIdsString)
    // console.log("{% url 'populate_file_table' %}")
    $.ajax({
        url: tableUrl + "?resources=" + resIds,
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
// console.log(collapseButtons)
for(let i = 0; i < collapseButtons.length; i++)
{
    jQueryButton = $(collapseButtons[i])
    // console.log(jQueryButton)
    // console.log(collapseButtons)
    // console.log("splitting id array: " + splitDashArray)
    // console.log(splitDashArray)
    let idNumber = getLastDashItem(jQueryButton.attr("id"))
    // console.log("getting id num: " + idNumber)
    let collapseContent = collapseList.find("#collapse-content-" + idNumber)
    collapseContent.hide()
    // console.log("getting content from id #collapse-content-" + idNumber + ": ")
    // console.log(collapseContent)

    let plus = jQueryButton.find("#expand-button-" + idNumber)
    let minus = jQueryButton.find("#collapse-button-" + idNumber)
    // console.log(plus)
    // console.log(minus)
    minus.hide()

    jQueryButton.click((event) => {
        // console.log("before " + idNumber) 
        // console.log(event)
        if(!jQueryButton.children())
            return;

        collapseContent.slideToggle(150)
        plus.toggle()
        minus.toggle()
        // console.log("after " + idNumber)
    });
    // console.log(jQueryButton)
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
    console.log(port)
    portId = getLastDashItem(port.attr("id"))

    let resources = $("#collapse-content-" + portId).find(".js-resource")
    console.log(resources)
    let resIds = []
    for(let j=0; j<resources.length; j++)
    {
        let res = $(resources[j])
        resIds.push(getLastDashItem(res.attr("id")))
    }
    console.log(resIds)
    
    port.click(function(){
        getFileTable(resIds);
    });
}
