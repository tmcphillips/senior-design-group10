let collapseList = $("#collapse")
let collapseButtons = collapseList.find(".static-left");
// console.log(collapseButtons)
for(let i = 0; i < collapseButtons.length; i++)
{

    jQueryButton = $(collapseButtons[i])
    // console.log(jQueryButton)
    // console.log(collapseButtons)
    let splitDashArray = jQueryButton.attr("id").split("-")
    // console.log("splitting id array: " + splitDashArray)
    // console.log(splitDashArray)
    let idNumber = splitDashArray[splitDashArray.length-1]
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
