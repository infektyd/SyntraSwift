import Foundation
import SyntraSwiftCore

struct SyntraREPL {
    let showValon: Bool?
    let showModi: Bool?
    let showDrift: Bool?

    func run() {
        while true {
            print("\n[SYNTRA] > ", terminator: "")
            guard let line = readLine(), line.lowercased() != "exit", line.lowercased() != "quit" else { break }
            let cognition = runLanguageLoop(line,
                                            showValon: showValon,
                                            showModi: showModi,
                                            showDrift: showDrift)
            if let drift = cognition["drift"] {
                print("\n🌀 Final Drift Output:\n", drift)
            }
        }
    }
}

let repl = SyntraREPL(showValon: nil, showModi: nil, showDrift: nil)
repl.run()
