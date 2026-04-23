import Foundation
import Yams

/// Reads and writes `work.yaml` in a format compatible with the Python app.
///
/// Python format notes:
/// - Date keys are single-quoted strings: `'2024-01-15':`
/// - Time values use no leading zero on hour: `8:05`, `14:30`
/// - Fields are alphabetically sorted (`sort_keys=True`)
/// - `paused` is integer `1` (only written on today's entry when true)
/// - `stop` and `summary` are omitted when nil/empty
enum YAMLCoder {

    // MARK: - Load

    static func load(from url: URL) throws -> [WorkDay] {
        let text = try String(contentsOf: url, encoding: .utf8)
        guard !text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { return [] }
        guard let root = try Yams.load(yaml: text) as? [String: Any] else { return [] }

        return try root.keys.sorted().compactMap { key -> WorkDay? in
            guard let dict = root[key] as? [String: Any] else { return nil }
            return try parseDay(dict)
        }
    }

    private static func parseDay(_ d: [String: Any]) throws -> WorkDay {
        guard let dateStr = d["date"] as? String,
              let date = dateFromString(dateStr) else {
            throw CoderError.invalidDate
        }
        let goalStr = d["goal"] as? String ?? "8:00"
        let goal = parseInterval(goalStr) ?? (8 * 3600)
        let comment = d["comment"] as? String
        let paused = (d["paused"] as? Int ?? 0) != 0
        let rawWork = d["work"] as? [[String: Any]] ?? []
        let blocks = try rawWork.map { try parseBlock($0) }
        return WorkDay(date: date, goal: goal, comment: comment, work: blocks, paused: paused)
    }

    private static func parseBlock(_ b: [String: Any]) throws -> WorkBlock {
        guard let startStr = b["start"] as? String,
              let start = HourMinute(string: startStr) else {
            throw CoderError.invalidTime
        }
        let stop = (b["stop"] as? String).flatMap { HourMinute(string: $0) }
        let category = b["category"] as? String ?? ""
        let summary = b["summary"] as? String
        return WorkBlock(start: start, stop: stop, category: category, summary: summary)
    }

    // MARK: - Save

    /// Writes the store to disk as YAML, matching the Python app's output format.
    /// Uses manual string building to avoid dependency on Yams' Node API.
    static func save(_ store: WorkStore, to url: URL) throws {
        var lines: [String] = []

        for day in store.days.sorted(by: { $0.date < $1.date }) {
            let dateStr = formatDate(day.date)
            lines.append("'\(dateStr)':")

            // Alphabetical field order: comment, date, goal, paused, work
            if let c = day.comment, !c.isEmpty {
                lines.append("  comment: \(yamlString(c))")
            }
            lines.append("  date: '\(dateStr)'")
            lines.append("  goal: '\(formatInterval(day.goal))'")
            if day.paused {
                lines.append("  paused: 1")
            }
            if day.work.isEmpty {
                lines.append("  work: []")
            } else {
                lines.append("  work:")
            }
            for block in day.work {
                // Alphabetical: category, start, stop, summary
                lines.append("  - category: \(block.category)")
                lines.append("    start: '\(block.start.string)'")
                if let stop = block.stop {
                    lines.append("    stop: '\(stop.string)'")
                }
                if let summary = block.summary, !summary.isEmpty {
                    lines.append("    summary: \(yamlString(summary))")
                }
            }
        }

        let yaml = lines.joined(separator: "\n") + "\n"

        // Atomic write: temp file in the same directory, then rename
        let tempURL = url.deletingLastPathComponent()
            .appendingPathComponent(".\(url.lastPathComponent).tmp_\(UUID().uuidString)")
        try yaml.write(to: tempURL, atomically: false, encoding: .utf8)
        _ = try FileManager.default.replaceItemAt(url, withItemAt: tempURL)
    }

    // MARK: - Helpers

    /// Wraps a string in single quotes, escaping any single quotes inside.
    /// Falls back to double quotes if the value needs quoting.
    private static func yamlString(_ s: String) -> String {
        if s.contains("'") {
            // Use double-quoted YAML scalar with escaped characters
            let escaped = s
                .replacingOccurrences(of: "\\", with: "\\\\")
                .replacingOccurrences(of: "\"", with: "\\\"")
            return "\"\(escaped)\""
        }
        // Plain scalar if safe, otherwise single-quoted
        let needsQuoting = s.isEmpty || s.contains(":") || s.contains("#") ||
                           s.hasPrefix("-") || s.hasPrefix("?") || s.hasPrefix("|") ||
                           s.hasPrefix(">") || s.hasPrefix("!") || s.hasPrefix("&") ||
                           s.hasPrefix("*") || s.hasPrefix("{") || s.hasPrefix("[")
        if needsQuoting {
            return "'\(s)'"
        }
        return s
    }

    private static func dateFromString(_ s: String) -> Date? {
        let df = DateFormatter()
        df.dateFormat = "yyyy-MM-dd"
        df.timeZone = .current
        return df.date(from: s)
    }

    static func formatDate(_ date: Date) -> String {
        let df = DateFormatter()
        df.dateFormat = "yyyy-MM-dd"
        df.timeZone = .current
        return df.string(from: date)
    }

    private static func parseInterval(_ s: String) -> TimeInterval? {
        guard let hm = HourMinute(string: s) else { return nil }
        return TimeInterval(hm.hour * 3600 + hm.minute * 60)
    }

    /// Formats seconds as `H:MM` — matches Python's `format_delta`.
    static func formatInterval(_ seconds: TimeInterval) -> String {
        let total = Int(seconds)
        let h = total / 3600
        let m = (total % 3600) / 60
        return "\(h):\(String(format: "%02d", m))"
    }

    // MARK: - Errors

    enum CoderError: Error, LocalizedError {
        case invalidDate
        case invalidTime

        var errorDescription: String? {
            switch self {
            case .invalidDate: return "Invalid date in YAML"
            case .invalidTime: return "Invalid time in YAML"
            }
        }
    }
}
