import Foundation
import Valon
import Modi
import Drift

// Allow overriding the Apple LLM query for testing
public var queryAppleLLM: (String) -> String = { _ in "[apple_llm_placeholder]" }

public struct MemoryEngine {
    public init() {}
}

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

public func processThroughBrains(_ input: String) -> [String: Any] {
    let config: SyntraConfig
    do {
        config = try loadConfig()
    } catch {
        config = SyntraConfig()
    }
    let valon = reflect_valon(input)
    logStage(stage: "valon_stage", output: valon, directory: "entropy_logs")
    let modi = reflect_modi(input)
    logStage(stage: "modi_stage", output: modi, directory: "entropy_logs")
    let drift = drift_average(valon, modi)
    logStage(stage: "drift_stage", output: drift, directory: "drift_logs")
    var result: [String: Any] = ["valon": valon, "modi": modi, "drift": drift]
    if config.useAppleLlm == true {
        let apple = queryAppleLLM(input)
        logStage(stage: "apple_stage", output: apple, directory: "entropy_logs")
        result["appleLLM"] = apple
    }
    return result
}

public func jsonString(_ obj: Any) -> String {
    if let data = try? JSONSerialization.data(withJSONObject: obj, options: []),
       let str = String(data: data, encoding: .utf8) {
        return str
    }
    return "{}"
}
