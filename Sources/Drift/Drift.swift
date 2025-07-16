import Foundation

public struct Drift {
    public init() {}
    public func average(valon: String, modi: [String]) -> [String: Any] {
        return ["emotion": valon,
                "logic": modi,
                "converged_state": "\(valon) + \(modi.joined(separator: ", "))"]
    }
}

public func drift_average(_ valon: String, _ modi: [String]) -> [String: Any] {
    return Drift().average(valon: valon, modi: modi)
}
