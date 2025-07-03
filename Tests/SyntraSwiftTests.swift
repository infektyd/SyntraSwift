import XCTest
@testable import Valon
@testable import Modi
@testable import Drift
@testable import MemoryEngine

final class SyntraSwiftTests: XCTestCase {
    /// Helper to run the CLI and capture output
    func runCLI(_ command: String, _ args: [String] = []) throws -> String {
        let exe = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
            .appendingPathComponent(".build/debug/SyntraSwiftCLI")
        let process = Process()
        process.executableURL = exe
        process.arguments = [command] + args
        let pipe = Pipe()
        process.standardOutput = pipe
        try process.run()
        process.waitUntilExit()
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        return String(data: data, encoding: .utf8)?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
    }

    func testReflectValonMatchesCLI() throws {
        let input = "Warning: torque is high"
        let cliOut = try runCLI("reflect_valon", [input])
        XCTAssertEqual(cliOut, reflect_valon(input))
    }

    func testReflectModiMatchesCLI() throws {
        let input = "If pressure then torque"
        let cliOut = try runCLI("reflect_modi", [input])
        let cliResult = try JSONSerialization.jsonObject(with: Data(cliOut.utf8)) as? [String]
        XCTAssertEqual(cliResult, reflect_modi(input))
    }

    func testDriftAverageMatchesCLI() throws {
        let valon = "neutral/observing"
        let modi = ["baseline_analysis"]
        let modiJSON = try String(data: JSONSerialization.data(withJSONObject: modi), encoding: .utf8) ?? "[]"
        let cliOut = try runCLI("drift_average", [valon, modiJSON])
        let cliResult = try JSONSerialization.jsonObject(with: Data(cliOut.utf8)) as? [String: Any]
        let apiResult = drift_average(valon, modi)
        XCTAssertEqual(cliResult?["converged_state"] as? String, apiResult["converged_state"] as? String)
    }

    func testProcessThroughBrainsMatchesCLI() throws {
        let input = "Procedure diagram"
        let cliOut = try runCLI("processThroughBrains", [input])
        let cliResult = try JSONSerialization.jsonObject(with: Data(cliOut.utf8)) as? [String: Any]
        let apiResult = processThroughBrains(input)
        XCTAssertEqual(cliResult?["valon"] as? String, apiResult["valon"] as? String)
        let m1 = cliResult?["modi"] as? [String]
        let m2 = apiResult["modi"] as? [String]
        XCTAssertEqual(m1, m2)
    }

    func testLoadConfigAppleLLMFields() throws {
        let tmp = URL(fileURLWithPath: NSTemporaryDirectory()).appendingPathComponent("cfg.json")
        let json = """
        {"use_apple_llm": true, "apple_llm_model": "test-model"}
        """
        try json.write(to: tmp, atomically: true, encoding: .utf8)
        var cfg = try loadConfig(path: tmp.path)
        XCTAssertEqual(cfg.useAppleLlm, true)
        XCTAssertEqual(cfg.appleLlmModel, "test-model")

        setenv("USE_APPLE_LLM", "false", 1)
        setenv("APPLE_LLM_MODEL", "env-model", 1)
        cfg = try loadConfig(path: tmp.path)
        XCTAssertEqual(cfg.useAppleLlm, false)
        XCTAssertEqual(cfg.appleLlmModel, "env-model")
        unsetenv("USE_APPLE_LLM")
        unsetenv("APPLE_LLM_MODEL")
    }

    func testProcessThroughBrainsAppleLLM() throws {
        setenv("USE_APPLE_LLM", "true", 1)
        let result = processThroughBrains("hi")
        unsetenv("USE_APPLE_LLM")
        XCTAssertNil(result["appleLLM"])
    }
}
