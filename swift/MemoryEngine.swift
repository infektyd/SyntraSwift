import Foundation

public struct MemoryNode: Codable {
    var uid: String
    var timestamp: String?
    var path: String?
    var summary: String?
}

private let hybridDir = URL(fileURLWithPath: "memory_vault/hybrid_store")
private let nodesFile = hybridDir.appendingPathComponent("graph_nodes.json")
private let edgesFile = hybridDir.appendingPathComponent("edges_map.json")
private let indexFile = hybridDir.appendingPathComponent("hybrid_index.json")

private func loadJSON<T: Codable>(_ url: URL, defaultValue: T) -> T {
    let fm = FileManager.default
    guard fm.fileExists(atPath: url.path) else { return defaultValue }
    do {
        let data = try Data(contentsOf: url)
        return try JSONDecoder().decode(T.self, from: data)
    } catch {
        return defaultValue
    }
}

private func saveJSON<T: Codable>(_ url: URL, value: T) {
    let fm = FileManager.default
    try? fm.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
    if let data = try? JSONEncoder().encode(value) {
        try? data.write(to: url)
    }
}

public func initHybridStore() {
    let fm = FileManager.default
    try? fm.createDirectory(at: hybridDir, withIntermediateDirectories: true)
    for url in [nodesFile, edgesFile, indexFile] {
        if !fm.fileExists(atPath: url.path) {
            saveJSON(url, value: [String: AnyCodable]())
        }
    }
}

public func addMemoryNode(entry: [String: Any], references: [String]?) -> String? {
    let config: SyntraConfig
    do {
        config = try loadConfig()
    } catch {
        return nil
    }
    guard config.memoryMode == "hybrid" else { return nil }
    initHybridStore()

    let uid = UUID().uuidString
    var nodes: [String: MemoryNode] = loadJSON(nodesFile, defaultValue: [:])
    let node = MemoryNode(
        uid: uid,
        timestamp: entry["timestamp"] as? String,
        path: entry["source"] as? String,
        summary: (entry["summary"] as? String)?.prefix(200).description
    )
    nodes[uid] = node
    saveJSON(nodesFile, value: nodes)

    var edges: [String: [String]] = loadJSON(edgesFile, defaultValue: [:])
    edges[uid] = references ?? []
    saveJSON(edgesFile, value: edges)

    var index: [String: [String]] = loadJSON(indexFile, defaultValue: [:])
    let src = entry["source"] as? String ?? "unknown"
    index[src, default: []].append(uid)
    saveJSON(indexFile, value: index)

    return uid
}

public func traverseMemory() -> [MemoryNode] {
    let config: SyntraConfig
    do {
        config = try loadConfig()
    } catch {
        return []
    }
    var results: [MemoryNode] = []
    if config.memoryMode == "hybrid" {
        initHybridStore()
        let nodes: [String: MemoryNode] = loadJSON(nodesFile, defaultValue: [:])
        results = Array(nodes.values)
    } else {
        let vaults = ["memory_vault/modi", "memory_vault/valon"]
        for v in vaults {
            if let files = try? FileManager.default.contentsOfDirectory(atPath: v) {
                for f in files where f.hasSuffix(".json") {
                    let path = URL(fileURLWithPath: v).appendingPathComponent(f)
                    if let data = try? Data(contentsOf: path),
                       let node = try? JSONDecoder().decode(MemoryNode.self, from: data) {
                        results.append(node)
                    }
                }
            }
        }
    }
    return results
}

struct AnyCodable: Codable {}
