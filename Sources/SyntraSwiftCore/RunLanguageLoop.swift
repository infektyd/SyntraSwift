import Foundation

// Directories for symbolic logs
let ENTROPY_DIR = "entropy_logs"
let DRIFT_DIR = "drift_logs"

private func ensureLogDirs() {
    let fm = FileManager.default
    try? fm.createDirectory(atPath: ENTROPY_DIR, withIntermediateDirectories: true)
    try? fm.createDirectory(atPath: DRIFT_DIR, withIntermediateDirectories: true)
}

// MARK: - Symbolic Reflection Functions

public func reflectValon(_ content: String) -> String {
    var result = "neutral/observing"
    let lower = content.lowercased()
    if lower.contains("warning") { result = "cautious/alert" }
    else if lower.contains("troubleshooting") { result = "curious/focused" }
    else if lower.contains("procedure") { result = "structured/learning" }

    logStage(name: "valon_stage", output: result, directory: ENTROPY_DIR)
    return result
}

public func reflectModi(_ content: String) -> [String] {
    var reasoning: [String] = []
    let lower = content.lowercased()
    if lower.contains("if") && lower.contains("then") { reasoning.append("conditional_logic") }
    if lower.contains("torque") || lower.contains("psi") { reasoning.append("mechanical_precision") }
    if lower.contains("diagram") { reasoning.append("visual_mapping") }
    if reasoning.isEmpty { reasoning = ["baseline_analysis"] }

    logStage(name: "modi_stage", output: reasoning, directory: ENTROPY_DIR)
    return reasoning
}

public func driftAverage(valon: String, modi: [String]) -> [String: String] {
    let drift = [
        "emotion": valon,
        "logic": modi.joined(separator: ","),
        "converged_state": "\(valon) + \(modi.joined(separator: ", "))"
    ]
    logStage(name: "drift_stage", output: drift, directory: DRIFT_DIR)
    return drift
}

public func processThroughBrains(_ input: String) -> [String: Any] {
    let valonOutput = reflectValon(input)
    let modiOutput = reflectModi(input)
    let driftOutput = driftAverage(valon: valonOutput, modi: modiOutput)
    return [
        "valon": valonOutput,
        "modi": modiOutput,
        "drift": driftOutput
    ]
}

private func logStage(name: String, output: Any, directory: String) {
    ensureLogDirs()
    let logPath = URL(fileURLWithPath: directory).appendingPathComponent("\(name).json")
    var dataArray: [[String: Any]] = []
    if let data = try? Data(contentsOf: logPath),
       let obj = try? JSONSerialization.jsonObject(with: data) as? [[String: Any]] {
        dataArray = obj
    }
    let entry: [String: Any] = ["timestamp": ISO8601DateFormatter().string(from: Date()), "output": output]
    dataArray.append(entry)
    if let outputData = try? JSONSerialization.data(withJSONObject: dataArray, options: [.prettyPrinted]) {
        try? outputData.write(to: logPath)
    }
}

// MARK: - Configuration Loading

struct Config: Codable {
    var enable_valon_output: Bool?
    var enable_modi_output: Bool?
    var enable_drift_output: Bool?
}

func loadConfig() -> Config {
    let searchPaths = ["config/config.local.json", "config.local.json", "config.json"]
    let fileManager = FileManager.default
    let decoder = JSONDecoder()
    for path in searchPaths {
        if fileManager.fileExists(atPath: path),
           let data = try? Data(contentsOf: URL(fileURLWithPath: path)),
           let cfg = try? decoder.decode(Config.self, from: data) {
            return cfg
        }
    }
    return Config()
}

// MARK: - Placeholder Bridges

func mistralSummarize(_ text: String) -> String {
    return "Summary: \(text)"
}

func queryPhi3(_ text: String) -> String {
    return "Phi3 response to: \(text)"
}

func getWordInfo(_ word: String) -> [String: Any] {
    return ["word": word]
}

func analyzeStructure(_ text: String) -> [String: Any] {
    return ["length": text.count]
}

// MARK: - Language Loop

public func runLanguageLoop(_ inputText: String,
                            showValon: Bool? = nil,
                            showModi: Bool? = nil,
                            showDrift: Bool? = nil,
                            debugOutputTrace: Bool = false) -> [String: Any] {
    print("\n🧠 SYNTRA Observing: \"\(inputText)\"")
    let config = loadConfig()
    let valonFlag = showValon ?? config.enable_valon_output ?? true
    let modiFlag = showModi ?? config.enable_modi_output ?? true
    let driftFlag = showDrift ?? config.enable_drift_output ?? true

    _ = mistralSummarize(inputText)
    _ = queryPhi3(inputText)
    _ = inputText.split(separator: " ").map { getWordInfo(String($0)) }
    _ = analyzeStructure(inputText)

    let cognition = processThroughBrains(inputText)

    if debugOutputTrace {
        if let data = try? JSONSerialization.data(withJSONObject: cognition, options: [.prettyPrinted]),
           let string = String(data: data, encoding: .utf8) {
            print("\n[DEBUG] COGNITION TRACE:")
            print(string)
        }
    }

    if valonFlag, let valonOutput = cognition["valon"] {
        print("\n🔮 VALON SAYS:\n", valonOutput)
    }
    if modiFlag, let modiOutput = cognition["modi"] {
        print("\n🧠 MODI SAYS:\n", modiOutput)
    }
    if driftFlag, let driftOutput = cognition["drift"] {
        print("\n⚖️ SYNTRA DRIFT OUTPUT:\n", driftOutput)
    }

    return cognition
}
