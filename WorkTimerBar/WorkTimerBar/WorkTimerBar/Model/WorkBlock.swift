import Foundation

/// A single work interval, mirroring the Python `Block`/`Work` class.
/// Times are stored as hour+minute components to avoid timezone issues when
/// round-tripping through YAML (Python stores `H:MM` strings, not datetimes).
struct WorkBlock: Identifiable {
    let id = UUID()
    var start: HourMinute
    var stop: HourMinute?   // nil = timer currently running
    var category: String
    var summary: String?

    var isRunning: Bool { stop == nil }

    /// Elapsed duration. If running, measures from start until `now`.
    func duration(on date: Date = .now) -> TimeInterval {
        let base = Calendar.current.startOfDay(for: date)
        let startDate = base.addingTimeInterval(TimeInterval(start.hour * 3600 + start.minute * 60))
        let stopDate: Date
        if let s = stop {
            stopDate = base.addingTimeInterval(TimeInterval(s.hour * 3600 + s.minute * 60))
        } else {
            stopDate = date
        }
        return max(0, stopDate.timeIntervalSince(startDate))
    }
}

/// A plain hour+minute pair — avoids calendar/timezone ambiguity for stored times.
struct HourMinute: Equatable {
    var hour: Int
    var minute: Int

    /// Parses a `H:MM` or `HH:MM` string (Python uses no leading zero on hour).
    init?(string: String) {
        let parts = string.split(separator: ":", maxSplits: 1).map(String.init)
        guard parts.count == 2,
              let h = Int(parts[0]),
              let m = Int(parts[1]) else { return nil }
        self.hour = h
        self.minute = m
    }

    init(hour: Int, minute: Int) {
        self.hour = hour
        self.minute = minute
    }

    /// Formats as Python's `'{d.hour}:{d.minute:02}'` — no leading zero on hour.
    var string: String { "\(hour):\(String(format: "%02d", minute))" }
}

extension HourMinute {
    /// Returns an `HourMinute` for the current time.
    static func now() -> HourMinute {
        let comps = Calendar.current.dateComponents([.hour, .minute], from: Date())
        return HourMinute(hour: comps.hour ?? 0, minute: comps.minute ?? 0)
    }
}
