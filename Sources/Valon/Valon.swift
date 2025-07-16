import Foundation

public struct Valon {
    public init() {}
    public func reflect(_ content: String) -> String {
        let lower = content.lowercased()
        if lower.contains("warning") { return "cautious/alert" }
        else if lower.contains("troubleshooting") { return "curious/focused" }
        else if lower.contains("procedure") { return "structured/learning" }
        return "neutral/observing"
    }
}

public func reflect_valon(_ content: String) -> String {
    return Valon().reflect(content)
}
