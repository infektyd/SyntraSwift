import Foundation

/// Launches the `run_SYNTRA_loop.py` script and streams its output.
final class SyntraBridge {
    private var process: Process?
    private var stdinPipe: Pipe?
    private var stdoutPipe: Pipe?
    private var stderrPipe: Pipe?

    /// Callback invoked when new stdout text is available.
    var onOutput: ((String) -> Void)?
    /// Callback invoked when new stderr text is available.
    var onError: ((String) -> Void)?

    private let python: String
    private let script: String

    init(python: String = "python3", script: String = "run_SYNTRA_loop.py") {
        self.python = python
        self.script = script
    }

    /// Start the Python process if it is not already running.
    func start() {
        guard process == nil else { return }
        let proc = Process()
        proc.executableURL = URL(fileURLWithPath: python)
        proc.arguments = [script]
        proc.environment = ProcessInfo.processInfo.environment

        let inPipe = Pipe()
        let outPipe = Pipe()
        let errPipe = Pipe()
        proc.standardInput = inPipe
        proc.standardOutput = outPipe
        proc.standardError = errPipe

        outPipe.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData
            if !data.isEmpty, let text = String(data: data, encoding: .utf8) {
                self?.onOutput?(text)
            }
        }

        errPipe.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData
            if !data.isEmpty, let text = String(data: data, encoding: .utf8) {
                self?.onError?(text)
            }
        }

        do {
            try proc.run()
            process = proc
            stdinPipe = inPipe
            stdoutPipe = outPipe
            stderrPipe = errPipe
        } catch {
            onError?("Failed to start Python: \(error)")
        }
    }

    /// Send a line of input to the running Python REPL.
    func send(_ text: String) {
        guard let handle = stdinPipe?.fileHandleForWriting else { return }
        if let data = (text + "\n").data(using: .utf8) {
            handle.write(data)
        }
    }

    /// Terminate the Python process and clean up handlers.
    func stop() {
        stdoutPipe?.fileHandleForReading.readabilityHandler = nil
        stderrPipe?.fileHandleForReading.readabilityHandler = nil
        process?.terminate()
        process = nil
        stdinPipe = nil
        stdoutPipe = nil
        stderrPipe = nil
    }
}
