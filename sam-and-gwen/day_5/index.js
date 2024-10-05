// THANK YOU MOZILLA:
// https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop


let file = null;


function readerOnLoad(e) {
    console.log(e.target.result);
}

function dropHandler(ev) {
    console.log("File dropped");
    ev.preventDefault();

    if (ev.dataTransfer.items) {
        // Use DataTransferItemList interface to access the file(s)
        let item = ev.dataTransfer.items[0];
        if (item.kind === "file") {
            file = item.getAsFile();
            // Output the file contents (text) to the console:
            let reader = new FileReader();
            let text = null
            reader.onload = readerOnLoad;
            // reader.readAsText(file); // Read file as text
        } else {
            alert("File error: no file dropped");
        }
    }
}


function dragOverHandler(ev) {
    console.log("File in drop zone");

    ev.preventDefault();
}