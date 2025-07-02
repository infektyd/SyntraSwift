import Valon
import Modi
import Drift
import MemoryEngine
import Foundation

let args = CommandLine.arguments
guard args.count >= 3 else { exit(0) }

let command = args[1]
let input = args[2]

switch command {
case "reflect_valon":
    print(reflect_valon(input))
case "reflect_modi":
    print(jsonString(reflect_modi(input)))
case "drift_average":
    if args.count >= 4,
       let modiData = args[3].data(using: .utf8),
       let modiArr = try? JSONSerialization.jsonObject(with: modiData) as? [String] {
        print(jsonString(drift_average(input, modiArr)))
    }
case "processThroughBrains":
    print(jsonString(processThroughBrains(input)))
default:
    break
}
