// swift-tools-version: 6.1
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "SyntraSwift",
    products: [
        // Products define the executables and libraries a package produces, making them visible to other packages.
        .library(
            name: "SyntraSwift",
            targets: ["SyntraSwift"]),
    ],
    targets: [
        // Core symbolic modules
        .target(name: "Valon"),
        .target(name: "Modi"),
        .target(name: "Drift"),
        .target(name: "MemoryEngine"),

        // Aggregator target
        .target(
            name: "SyntraSwift",
            dependencies: ["Valon", "Modi", "Drift", "MemoryEngine"]),

        // Empty test target
        .testTarget(
            name: "SyntraSwiftTests",
            dependencies: ["SyntraSwift"]
        ),
    ]
)
