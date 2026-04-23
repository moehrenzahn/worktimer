// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "WorkTimerBar",
    platforms: [.macOS(.v14)],
    dependencies: [
        .package(url: "https://github.com/jpsim/Yams.git", from: "5.0.0"),
    ],
    targets: [
        .executableTarget(
            name: "WorkTimerBar",
            dependencies: [
                .product(name: "Yams", package: "Yams"),
            ],
            path: "Sources/WorkTimerBar",
        ),
    ]
)
