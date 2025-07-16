import Foundation
#if canImport(FoundationNetworking)
import FoundationNetworking
#endif

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
    final class Holder { var value: String = "" }
    let resultHolder = Holder()
    let task = URLSession.shared.dataTask(with: request) { data, _, error in
        let res: String
        if let error = error {
            res = "[apple llm error: \(error.localizedDescription)]"
        } else if let data = data {
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let choices = json["choices"] as? [[String: Any]],
               let message = choices.first?["message"] as? [String: Any],
               let content = message["content"] as? String {
                res = content
            } else if let str = String(data: data, encoding: .utf8) {
                res = str
            } else {
                res = "[apple llm parse error]"
            }
        } else {
            res = "[apple llm empty]"
        }
        DispatchQueue.main.sync { resultHolder.value = res }
        semaphore.signal()
    }
    task.resume()
    semaphore.wait()
    logStage(stage: "apple_llm", output: ["prompt": prompt, "response": resultHolder.value], directory: "entropy_logs")
    return resultHolder.value
}
