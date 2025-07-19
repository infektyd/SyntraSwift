// swift-tools-version:6.0
import PackageDescription

let package = Package(
    name: "SyntraSwift",
    platforms: [
        .macOS("26.0")
    ],
    products: [
        .library(name: "Valon", targets: ["Valon"]),
        .library(name: "Modi", targets: ["Modi"]),
        .library(name: "Drift", targets: ["Drift"]),
        .library(name: "MemoryEngine", targets: ["MemoryEngine"]),
        .library(name: "SyntraConfig", targets: ["SyntraConfig"]),
        .library(name: "BrainEngine", targets: ["BrainEngine"]),
        .library(name: "CognitiveDrift", targets: ["CognitiveDrift"]),
        .library(name: "MoralCore", targets: ["MoralCore"]),
        .library(name: "ConversationalInterface", targets: ["ConversationalInterface"]),
        .library(name: "ConsciousnessStructures", targets: ["ConsciousnessStructures"]),
        .library(name: "StructuredConsciousnessService", targets: ["StructuredConsciousnessService"]),
        .library(name: "MoralDriftMonitoring", targets: ["MoralDriftMonitoring"]),
        .library(name: "SyntraTools", targets: ["SyntraTools"]),
        .executable(name: "SyntraSwiftCLI", targets: ["SyntraSwiftCLI"]),
    ],
    targets: [
        .target(name: "Valon", path: "SyntraSwift/SyntraSwift/Sources/Valon"),
        .target(name: "Modi", path: "SyntraSwift/SyntraSwift/Sources/Modi"),
        .target(name: "Drift", path: "SyntraSwift/SyntraSwift/Sources/Drift"),
        .target(
            name: "MemoryEngine",
            dependencies: ["Valon", "Modi", "Drift"],
            path: "SyntraSwift/SyntraSwift/Sources/MemoryEngine"
        ),
        .target(name: "SyntraConfig", path: "SyntraSwift/SyntraSwift/Sources/SyntraConfig"),
        .target(
            name: "BrainEngine",
            dependencies: ["Valon", "Modi", "Drift", "SyntraConfig", "ConsciousnessStructures", "StructuredConsciousnessService"],
            path: "SyntraSwift/SyntraSwift/Sources/BrainEngine"
        ),
        .target(
            name: "CognitiveDrift",
            dependencies: ["Valon", "Modi", "Drift", "SyntraConfig", "BrainEngine"],
            path: "SyntraSwift/SyntraSwift/Sources/CognitiveDrift"
        ),
        .target(
            name: "MoralCore",
            dependencies: ["ConsciousnessStructures"],
            path: "SyntraSwift/SyntraSwift/Sources/MoralCore"
        ),
        .target(
            name: "ConversationalInterface",
            dependencies: ["MoralCore", "BrainEngine", "SyntraConfig", "ConsciousnessStructures", "StructuredConsciousnessService"],
            path: "SyntraSwift/SyntraSwift/Sources/ConversationalInterface"
        ),
        .target(
            name: "ConsciousnessStructures",
            dependencies: [],
            path: "SyntraSwift/SyntraSwift/Sources/ConsciousnessStructures"
        ),
        .target(
            name: "StructuredConsciousnessService",
            dependencies: ["ConsciousnessStructures", "MoralDriftMonitoring"],
            path: "SyntraSwift/SyntraSwift/Sources/StructuredConsciousnessService"
        ),
        .target(
            name: "MoralDriftMonitoring",
            dependencies: ["ConsciousnessStructures"],
            path: "SyntraSwift/SyntraSwift/Sources/MoralDriftMonitoring"
        ),
        .target(
            name: "SyntraTools",
            dependencies: ["Valon", "Modi", "Drift", "ConsciousnessStructures", "MoralDriftMonitoring", "StructuredConsciousnessService"],
            path: "SyntraSwift/SyntraSwift/Sources/SyntraTools"
        ),
        .executableTarget(
            name: "SyntraSwiftCLI",
            dependencies: [
                "Valon", "Modi", "Drift", "MemoryEngine",
                "SyntraConfig", "BrainEngine", "CognitiveDrift",
                "MoralCore", "ConversationalInterface", "ConsciousnessStructures",
                "MoralDriftMonitoring", "StructuredConsciousnessService", "SyntraTools"
            ],
            path: "SyntraSwift/SyntraSwift/swift"
        ),
        .testTarget(
            name: "SyntraSwiftTests",
            dependencies: [
                "SyntraSwiftCLI", "Valon", "Modi", "Drift", "MemoryEngine",
                "SyntraConfig", "BrainEngine", "CognitiveDrift", 
                "MoralCore", "ConversationalInterface", "ConsciousnessStructures",
                "MoralDriftMonitoring", "StructuredConsciousnessService", "SyntraTools"
            ],
            path: "SyntraSwift/SyntraSwift/Tests"
        ),
    ]
)