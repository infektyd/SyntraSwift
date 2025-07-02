// swift-tools-version: 6.1
import PackageDescription

let package = Package(
    name: "SyntraSwift",
    products: [
        .library(
            name: "SyntraSwiftCore",
            targets: ["SyntraSwiftCore"]),
        .executable(
            name: "SyntraREPL",
            targets: ["SyntraREPL"])
    ],
    targets: [
        .target(
            name: "SyntraSwiftCore"),
        .executableTarget(
            name: "SyntraREPL",
            dependencies: ["SyntraSwiftCore"]),
        .testTarget(
            name: "SyntraSwiftTests",
            dependencies: ["SyntraSwiftCore"]
        ),
    ]
)
