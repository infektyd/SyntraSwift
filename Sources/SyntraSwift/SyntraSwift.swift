import Valon
import Modi
import Drift
import MemoryEngine

public struct SyntraSwift {
    public var valon: Valon
    public var modi: Modi
    public var drift: Drift
    public var memoryEngine: MemoryEngine

    public init(valon: Valon = Valon(), modi: Modi = Modi(), drift: Drift = Drift(), memoryEngine: MemoryEngine = MemoryEngine()) {
        self.valon = valon
        self.modi = modi
        self.drift = drift
        self.memoryEngine = memoryEngine
    }
}
