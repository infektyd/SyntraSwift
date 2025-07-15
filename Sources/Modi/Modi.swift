import Foundation

public struct Modi {
    public init() {}
    public func reflect(_ content: String) -> [String] {
        var reasoning: [String] = []
        let lower = content.lowercased()
        if lower.contains("if") && lower.contains("then") { reasoning.append("conditional_logic") }
        if lower.contains("torque") || lower.contains("psi") { reasoning.append("mechanical_precision") }
        if lower.contains("diagram") { reasoning.append("visual_mapping") }
        if reasoning.isEmpty { reasoning.append("baseline_analysis") }
        return reasoning
    }
}

public func reflect_modi(_ content: String) -> [String] {
    Modi().reflect(content)
}
