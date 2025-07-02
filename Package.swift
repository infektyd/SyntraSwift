// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "SyntraSwift",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .library(name: "Valon", targets: ["Valon"]),
        .library(name: "Modi", targets: ["Modi"]),
        .library(name: "Drift", targets: ["Drift"]),
        .library(name: "MemoryEngine", targets: ["MemoryEngine"]),
        .executable(name: "SyntraSwiftCLI", targets: ["SyntraSwiftCLI"]),
    ],
    targets: [
        .target(name: "Valon", path: "Sources/Valon"),
        .target(name: "Modi", path: "Sources/Modi"),
        .target(name: "Drift", path: "Sources/Drift"),
        .target(name: "MemoryEngine", path: "Sources/MemoryEngine"),
        .executableTarget(name: "SyntraSwiftCLI", dependencies: ["Valon", "Modi", "Drift", "MemoryEngine"], path: "swift"),
        .testTarget(name: "SyntraSwiftTests", dependencies: ["SyntraSwiftCLI"], path: "Tests"),
    ]
)
