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
        
        part1(input);
        // part2(input);
    }
}

function part1(input) {
    let seeds = input[0];
    let maps = input[1];

    // let locations = [];
    let minLoc = Infinity;
    for (let i = 0; i < seeds.length; i++) {
        let seed = seeds[i];
        let stops = [seed];
        for (let j = 0; j < maps.length; j++) {
            let map = maps[j];
            let next = traverse(map, stops[stops.length-1]);
            stops.push(next);
        }
        // locations.push(stops[stops.length-1]);
        minLoc = Math.min(minLoc, stops[stops.length-1]);
    }
    console.log("Minimum location:", minLoc);
    document.querySelector("#part1").innerHTML = `Part 1: ${minLoc}`;
    // console.log("Minimum location:", Math.min(...locations));
    return minLoc;
}

function part2(input){
    // 1. Updating the seeds array
    let p1Seeds = input[0];
    let seeds = [];
    let maps = input[1];

    for (let i = 0; i < p1Seeds.length; i+=2) {
        seeds.push([p1Seeds[i], p1Seeds[i+1]]); // list of (<base seed>, <range>)
    }

    let minLoc = Infinity;
    for (let i = 0; i < seeds.length; i++) {
        let seed = seeds[i][0];
        let range = seeds[i][1];
        for (let j = seed; j < seed + range; j++) {
            let temp = traverseAll(maps, j);
            if (temp < minLoc) minLoc = temp;
        }
        
    }

    console.log("Part 2:", minLoc);
    document.querySelector("#part2").innerHTML = `Part 2: ${minLoc}`;
    
}

function traverseAll(maps, input) {
    let out = input;
    for (let i = 0; i < maps.length; i++) {
        out = traverse(maps[i], out);
    }
    return out;
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
    ev.target.classList.add("dragover");
    ev.preventDefault();
}

function dragOverHandler(ev) {
    ev.preventDefault();
}

function dragLeaveHandler(ev) {
    ev.target.classList.remove("dragover");
    ev.preventDefault();
}
