import XCTest
@testable import Valon
@testable import Modi
@testable import Drift
@testable import MemoryEngine

final class SyntraSwiftTests: XCTestCase {
    func testExample() {
        _ = Valon()
        _ = Modi()
        _ = Drift()
        _ = MemoryEngine()
        XCTAssertTrue(true)
    }
}
