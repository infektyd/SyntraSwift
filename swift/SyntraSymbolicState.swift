import Foundation

struct SyntraSymbolicMemory: Codable {
    var driftLogs: [String]
    var symbolicEvents: [SyntraSymbolicEvent]
    var reasoningBlends: [String]
    var dreamLogs: [String]
}

struct SyntraSymbolicEvent: Codable {
    var source: String
    var reflected: SyntraSymbolicReflection
    var timestamp: String
}

struct SyntraSymbolicReflection: Codable {
    var symbolicTerms: [String]
    var emotions: [String]
    var structure: String
    var meaning: String
}

struct SyntraSymbolicState: Codable {
    var valon: String
    var modi: [String]
    var drift: DriftOutput
}

struct DriftOutput: Codable {
    var emotion: String
    var logic: [String]
    var convergedState: String

    enum CodingKeys: String, CodingKey {
        case emotion
        case logic
        case convergedState = "converged_state"
    }
}
