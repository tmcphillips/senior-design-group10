let collapseList = document.querySelector("#collapse")
let collapseButtons = collapseList.querySelectorAll(".static-left");

for(let i = 0; i < collapseButtons.length; i++)
{
    // console.log(collapseButtons)
    let splitDashArray = collapseButtons[i].id.split("-")
    // console.log("splitting id array: " + splitDashArray)
    // console.log(splitDashArray)
    let idNumber = splitDashArray[splitDashArray.length-1]
    // console.log("getting id num: " + idNumber)
    let collapseContent = collapseList.querySelector("#collapse-content-" + idNumber)
    // console.log("getting content from id #collapse-content-" + idNumber + ": ")
    // console.log(collapseContent)
    collapseButtons[i].addEventListener("click", (event) => {
        // console.log("before " + collapseContent.style.display) 
        // console.log(event)
        if(!collapseButtons[i].childNodes)
            return;
        
        // console.log("plus minus exists")
        // console.log(collapseButtons[i].childNodes)

        let plus = collapseButtons[i].querySelector("#expand-button-" + idNumber)
        let minus = collapseButtons[i].querySelector("#collapse-button-" + idNumber)
        if(collapseContent.classList.contains("hidden")) {
            collapseContent.classList.remove("hidden")
            plus.classList.add("hidden")
            minus.classList.remove("hidden")
        } else {
            collapseContent.classList.add("hidden")
            plus.classList.remove("hidden")
            minus.classList.add("hidden")
        }
        // console.log("after " + collapseContent.style.display)
    });
}
