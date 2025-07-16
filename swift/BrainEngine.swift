import Foundation

func logStage(stage: String, output: Any, directory: String) {
    let fm = FileManager.default
    if !fm.fileExists(atPath: directory) {
        try? fm.createDirectory(atPath: directory, withIntermediateDirectories: true)
    }
    let path = URL(fileURLWithPath: directory).appendingPathComponent("\(stage).json")
    var data: [[String: Any]] = []
    if let d = try? Data(contentsOf: path),
       let j = try? JSONSerialization.jsonObject(with: d) as? [[String: Any]] {
        data = j
    }
    let entry: [String: Any] = ["timestamp": ISO8601DateFormatter().string(from: Date()),
                                "output": output]
    data.append(entry)
    if let out = try? JSONSerialization.data(withJSONObject: data, options: [.prettyPrinted]) {
        try? out.write(to: path)
    }
}

func reflect_valon(_ content: String) -> String {
    let lower = content.lowercased()
    if lower.contains("warning") { return "cautious/alert" }
    else if lower.contains("troubleshooting") { return "curious/focused" }
    else if lower.contains("procedure") { return "structured/learning" }
    return "neutral/observing"
}

func reflect_modi(_ content: String) -> [String] {
    var reasoning: [String] = []
    let lower = content.lowercased()
    if lower.contains("if") && lower.contains("then") { reasoning.append("conditional_logic") }
    if lower.contains("torque") || lower.contains("psi") { reasoning.append("mechanical_precision") }
    if lower.contains("diagram") { reasoning.append("visual_mapping") }
    if reasoning.isEmpty { reasoning.append("baseline_analysis") }
    return reasoning
}

func drift_average(_ valon: String, _ modi: [String]) -> [String: Any] {
    return ["emotion": valon,
            "logic": modi,
            "converged_state": "\(valon) + \(modi.joined(separator: ", "))"]
}

func processThroughBrains(_ input: String) -> [String: Any] {
    let valon = reflect_valon(input)
    logStage(stage: "valon_stage", output: valon, directory: "entropy_logs")
    let modi = reflect_modi(input)
    logStage(stage: "modi_stage", output: modi, directory: "entropy_logs")
    let drift = drift_average(valon, modi)
    logStage(stage: "drift_stage", output: drift, directory: "drift_logs")

    var result: [String: Any] = ["valon": valon, "modi": modi, "drift": drift]
    if let cfg = try? loadConfig(), cfg.useAppleLLM == true {
        let apple = queryAppleLLM(input)
        result["appleLLM"] = apple
    }
    return result
}

func jsonString(_ obj: Any) -> String {
    if let data = try? JSONSerialization.data(withJSONObject: obj, options: []),
       let str = String(data: data, encoding: .utf8) {
        return str
    }
    return "{}"
}
