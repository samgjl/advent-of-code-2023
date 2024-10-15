open System.Text.RegularExpressions
open System.IO

let filename = "../input.txt"

let read f part = 
    let removeSpaces line = 
        if part = 1 then Regex.Replace(line, @"(\s)\s+", "$1")
        else Regex.Replace(line, @"(\s)\s+", "")
    let lines = (File.ReadAllLines(f) |> Array.toList)
    let timeLine = (
        lines[0].Replace("Time:","").Trim()
        |> removeSpaces)
    let distLine = (
        lines[1].Replace("Distance:","").Trim()
        |> removeSpaces)
    let times = (
        timeLine.Split([|' '|]) 
        |> Array.map float
        |> Array.toList)
    let dists = (
        distLine.Split([|' '|])
        |> Array.map float
        |> Array.toList)
    (times, dists)

let removeAllSpaces line = 
    Regex.Replace(line, @"(\s)\s+", "")

let solveEquation T D =
    let discriminant = sqrt((T*T) - (4.0 * D))
    let x1 = max ((-T + discriminant) / -2.0) 1.0
    let x2 = min ((-T - discriminant) / -2.0) (T - 1.0)
    abs ((floor (x2 - 0.0001)) - (ceil (x1 + 0.0001)) + 1.0)

let rec solveAll (times: float list) (dists: float list): float list = 
    if times.IsEmpty || dists.IsEmpty then []
    else 
        let sol = solveEquation times.Head dists.Head
        [sol] @ (solveAll times.Tail dists.Tail)

let part1 = 
    let (T, D) = read filename 1
    solveAll T D
    |> List.reduce (*)

let part2 = 
    let (T,D) = read filename 2
    solveAll T D
    |> List.reduce (*)


printfn "--- PART 1 ---"
printfn $"Total: {part1}"
printfn "--------------"
printfn "--- PART 2 ---"
printfn $"Total: {part2}"
printfn "--------------"