import Foundation

struct SyntraConfig: Codable {
    var openaiApiKey: String?
    var openaiApiBase: String?
    var openaiModel: String?
    var elevenlabsApiKey: String?
    var appleLLMApiKey: String?
    var appleLLMApiBase: String?
    var useAppleLLM: Bool?
    var useMistralForValon: Bool?
    var preferredVoice: String?
    var driftRatio: [String: Double]?
    var enableValonOutput: Bool?
    var enableModiOutput: Bool?
    var enableDriftOutput: Bool?
    var logSymbolicDrift: Bool?
    var memoryMode: String?
    var interpreterOutput: Bool?
    var telemetryCsvPath: String?
    var appleLLMApiKey: String?
    var appleLLMApiBase: String?
    var appleLLMModel: String?
    var useAppleLLM: Bool?

    enum CodingKeys: String, CodingKey {
        case openaiApiKey
        case openaiApiBase
        case openaiModel
        case elevenlabsApiKey
        case useMistralForValon
        case preferredVoice
        case driftRatio
        case enableValonOutput
        case enableModiOutput
        case enableDriftOutput
        case logSymbolicDrift
        case memoryMode
        case interpreterOutput
        case telemetryCsvPath
        case appleLLMApiKey = "apple_llm_api_key"
        case appleLLMApiBase = "apple_llm_api_base"
        case appleLLMModel = "apple_llm_model"
        case useAppleLLM = "use_apple_llm"
    }
}

enum ConfigError: Error {
    case notFound
    case invalid
}

func loadConfig(path: String = "config.json") throws -> SyntraConfig {
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
    var cfg = try decoder.decode(SyntraConfig.self, from: data)
    let env = ProcessInfo.processInfo.environment
    if let val = env["OPENAI_API_KEY"] { cfg.openaiApiKey = val }
    if let val = env["ELEVENLABS_API_KEY"] { cfg.elevenlabsApiKey = val }
    if let val = env["APPLE_LLM_MODEL"] { cfg.appleLLMModel = val }
    if let val = env["APPLE_LLM_API_KEY"] { cfg.appleLLMApiKey = val }
    if let val = env["APPLE_LLM_API_BASE"] { cfg.appleLLMApiBase = val }
    if let val = env["USE_APPLE_LLM"] { cfg.useAppleLLM = (val as NSString).boolValue }
    return cfg
}

