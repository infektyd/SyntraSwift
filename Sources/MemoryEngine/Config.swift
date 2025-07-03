import Foundation

public struct SyntraConfig: Codable {
    public var openaiApiKey: String?
    public var openaiApiBase: String?
    public var openaiModel: String?
    public var elevenlabsApiKey: String?
    public var useMistralForValon: Bool?
    public var preferredVoice: String?
    public var driftRatio: [String: Double]?
    public var enableValonOutput: Bool?
    public var enableModiOutput: Bool?
    public var enableDriftOutput: Bool?
    public var logSymbolicDrift: Bool?
    public var memoryMode: String?
    public var interpreterOutput: Bool?
    public var telemetryCsvPath: String?
    public var useAppleLlm: Bool?
    public var appleLlmModel: String?
    public var appleLLMApiKey: String?
    public var appleLLMApiBase: String?
}

public enum ConfigError: Error {
    case notFound
    case invalid
}

public func loadConfig(path: String = "config.json") throws -> SyntraConfig {
    let searchPaths = [
        "config/config.local.json",
        "config.local.json",
        path
    ]
    var configURL: URL?
    let fm = FileManager.default
    for p in searchPaths {
        if fm.fileExists(atPath: p) {
            configURL = URL(fileURLWithPath: p)
            break
        }
    }
    if configURL == nil {
        configURL = URL(fileURLWithPath: path)
    }
    guard let url = configURL, fm.fileExists(atPath: url.path) else {
        throw ConfigError.notFound
    }
    let data = try Data(contentsOf: url)
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    var cfg = try decoder.decode(SyntraConfig.self, from: data)
    let env = ProcessInfo.processInfo.environment
    if let val = env["OPENAI_API_KEY"] { cfg.openaiApiKey = val }
    if let val = env["ELEVENLABS_API_KEY"] { cfg.elevenlabsApiKey = val }
    if let val = env["USE_APPLE_LLM"] { cfg.useAppleLlm = val.lowercased() == "true" }
    if let val = env["APPLE_LLM_MODEL"] { cfg.appleLlmModel = val }
    if let val = env["APPLE_LLM_API_KEY"] { cfg.appleLLMApiKey = val }
    if let val = env["APPLE_LLM_API_BASE"] { cfg.appleLLMApiBase = val }
    return cfg
}
