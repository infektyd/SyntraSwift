import Foundation
import FoundationNetworking

func queryAppleLLM(_ prompt: String) -> String {
    guard let apiKey = ProcessInfo.processInfo.environment["APPLE_LLM_API_KEY"] else {
        let msg = "[Missing APPLE_LLM_API_KEY]"
        logStage(stage: "apple_llm", output: ["prompt": prompt, "response": msg], directory: "entropy_logs")
        return msg
    }
    let base = ProcessInfo.processInfo.environment["APPLE_LLM_API_BASE"] ?? "https://api.apple.com/llm"
    guard let url = URL(string: "\(base)/v1/chat/completions") else {
        let msg = "[Invalid Apple LLM URL]"
        logStage(stage: "apple_llm", output: ["prompt": prompt, "response": msg], directory: "entropy_logs")
        return msg
    }
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.addValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
    request.addValue("application/json", forHTTPHeaderField: "Content-Type")
    let body: [String: Any] = ["prompt": prompt]
    request.httpBody = try? JSONSerialization.data(withJSONObject: body)

    let semaphore = DispatchSemaphore(value: 0)
    var result = ""
    let task = URLSession.shared.dataTask(with: request) { data, _, error in
        defer { semaphore.signal() }
        if let error = error {
            result = "[apple llm error: \(error.localizedDescription)]"
            return
        }
        guard let data = data else {
            result = "[apple llm empty]"
            return
        }
        if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
           let choices = json["choices"] as? [[String: Any]],
           let message = choices.first?["message"] as? [String: Any],
           let content = message["content"] as? String {
            result = content
        } else if let str = String(data: data, encoding: .utf8) {
            result = str
        } else {
            result = "[apple llm parse error]"
        }
    }
    task.resume()
    semaphore.wait()
    logStage(stage: "apple_llm", output: ["prompt": prompt, "response": result], directory: "entropy_logs")
    return result
}
