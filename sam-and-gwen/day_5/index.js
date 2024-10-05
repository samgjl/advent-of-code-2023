// THANK YOU MOZILLA:
// https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop

class RangeMap {
    src; dest; range;
    constructor(dest, src, range) {
        this.src = src;
        this.dest = dest;
        this.range = range
    }

    contains(input) {
        return (input >= this.src && input < this.src + this.range);
    }
    place(input) {
        return this.dest + (input - this.src);
    }
}


function readText(item) {
    return new Promise((resolve, reject) => {
        let file = item.getAsFile();
        let reader = new FileReader();
        let text = null
        reader.onload = function (e) {
            text = e.target.result;
            resolve(text);
        };
        reader.readAsText(file); // Read file as text    });
    });
}

async function dropHandler(ev) {
    console.log("File dropped");
    ev.preventDefault();
    if (ev.dataTransfer.items) {
        let item = ev.dataTransfer.items[0];
        if (item.kind != "file") {
            alert("File error: no file dropped");
            return null;
        }
        // Read our file as input:
        let input = await readText(item);
        input = parseInput(input);

        let seeds = input[0];
        let maps = input[1];

        let locations = [];
        for (let i = 0; i < seeds.length; i++) {
            let seed = seeds[i];
            let stops = [seed];
            for (let j = 0; j < maps.length; j++) {
                let map = maps[j];
                let next = traverse(map, stops[stops.length-1]);
                stops.push(next);
            }
            locations.push(stops[stops.length-1]);
        }
        console.log("Minimum location:", Math.min(...locations));
    }
}


function traverse(maps, input) {
    for (let i = 0; i < maps.length; i++) {
        let rangeMap = maps[i];
        if (rangeMap.contains(input)) {
            return rangeMap.place(input);
        }
    }
    return input;
}


function parseInput(text) {
    text = text.replace(/\r?\n/g, "\n")
    let maps = text.split("\n\n");
    let seeds = maps.shift();
    seeds = seeds.split("seeds: ")[1]
        .split(" ") // ["<s1>", "<s2>", ...]
        .map((num) => { return parseInt(num); }); // turns each seed into an int
    console.log(seeds);
    maps = maps.map((map) => {
        let temp = map.split("\n");
        temp.shift();
        return temp.map((line) => {
            line = line.split(" "); // split
            line = line.map((str) => parseInt(str)); // to ints
            return new RangeMap(line[0], line[1], line[2]); // make class
        });
    });
    return [seeds, maps];
}


function dragEnterHandler(ev) {
    console.log("File in drop zone");
    ev.preventDefault();
    document.getElementById("drop_zone").classList.add("dragover");
}

function dragOverHandler(ev) {
    ev.preventDefault();
}

function dragEndHandler(ev) {
    console.log("File no longer in grop zone");
    ev.preventDefault();
    document.getElementById("drop_zone").classList.remove("dragover");
}
