#if canImport(FoundationModels)
import Foundation
import FoundationModels

@available(macOS 15.0, *)
@Generable
struct FMResult {
    @Guide(description: "Raw response from the language model")
    var text: String
}

@available(macOS 15.0, *)
public struct EchoTool: Tool {
    public struct Arguments: Codable {
        @Guide(description: "Text to echo back")
        var text: String
    }
    public func callAsFunction(_ arguments: Arguments) async throws -> String {
        "Echo: \(arguments.text)"
    }
}

@available(macOS 15.0, *)
public func queryFoundationModel(_ prompt: String) async throws -> String {
    let session = try LanguageModelSession(for: SystemLanguageModel.default,
                                           tools: [EchoTool()])
    let result: FMResult = try await session.respond(
        to: prompt,
        as: FMResult.self,
        options: GenerationOptions(maxOutputTokens: 128)
    )
    return result.text
}
#else
public func queryFoundationModel(_ prompt: String) async throws -> String {
    "[foundation model unavailable]"
}
#endif
