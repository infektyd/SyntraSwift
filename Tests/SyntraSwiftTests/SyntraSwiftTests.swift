import Testing
@testable import SyntraSwiftCore

@Test func testReflectValon() async throws {
    let result = reflectValon("This is a warning about procedure")
    #expect(result == "cautious/alert")
}

@Test func testReflectModi() async throws {
    let result = reflectModi("If torque is high then check diagram")
    #expect(result.contains("conditional_logic"))
    #expect(result.contains("mechanical_precision"))
    #expect(result.contains("visual_mapping"))
}

@Test func testDriftAverage() async throws {
    let drift = driftAverage(valon: "neutral", modi: ["a", "b"])
    #expect(drift["emotion"] == "neutral")
    #expect(drift["logic"] == "a,b")
}

@Test func testProcessThroughBrains() async throws {
    let cog = processThroughBrains("If torque then warning")
    #expect(cog.keys.contains("valon"))
    #expect(cog.keys.contains("modi"))
    #expect(cog.keys.contains("drift"))
}
