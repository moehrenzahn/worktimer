import Foundation

/// A single work day, mirroring the Python `Day`/`Today` class.
struct WorkDay {
    var date: Date          // calendar date, time-of-day is ignored
    var goal: TimeInterval  // seconds (default 8 * 3600)
    var comment: String?
    var work: [WorkBlock]
    /// Only meaningful for today — mirrors Python's `paused` flag.
    var paused: Bool = false

    var isToday: Bool {
        Calendar.current.isDateInToday(date)
    }

    var isRunning: Bool {
        work.contains { $0.isRunning }
    }

    /// The most recent work block (by start time).
    var lastWork: WorkBlock? {
        work.max { a, b in
            a.start.hour < b.start.hour ||
            (a.start.hour == b.start.hour && a.start.minute < b.start.minute)
        }
    }

    /// Total worked time today. Running blocks are measured against `now`.
    func workedTime(now: Date = .now) -> TimeInterval {
        work.reduce(0) { $0 + $1.duration(on: now) }
    }

    /// Time spent on breaks (gaps between consecutive work blocks).
    /// Mirrors Python's `Day.calculatePauses()`.
    func pauseTime(now: Date = .now) -> TimeInterval {
        guard work.count > 1 else { return 0 }
        let sorted = work.sorted { a, b in
            a.start.hour < b.start.hour ||
            (a.start.hour == b.start.hour && a.start.minute < b.start.minute)
        }
        var total: TimeInterval = 0
        let base = Calendar.current.startOfDay(for: now)
        for i in 1..<sorted.count {
            let prevStop = sorted[i - 1].stop
            let curStart = sorted[i].start
            if let ps = prevStop {
                let gap = TimeInterval((curStart.hour - ps.hour) * 3600 + (curStart.minute - ps.minute) * 60)
                if gap > 0 { total += gap }
            }
        }
        return total
    }

    /// Remaining work needed to reach goal. Estimates 30-min pause if none taken.
    func remainingWork(now: Date = .now) -> TimeInterval {
        let pauses = pauseTime(now: now)
        let worked = workedTime(now: now)
        return max(0, goal - worked)
    }

    /// Overtime (positive = over goal, negative = under).
    func overtime(now: Date = .now) -> TimeInterval {
        workedTime(now: now) - goal
    }

    /// Projected end-of-day time (when remaining work reaches 0), estimating
    /// a 30-minute break if none has been taken yet and the timer is running.
    func projectedEndTime(now: Date = .now) -> Date? {
        guard isRunning else { return nil }
        let pauses = pauseTime(now: now)
        let estimatedPause: TimeInterval = pauses == 0 ? 30 * 60 : pauses
        let remaining = max(0, goal - workedTime(now: now) + estimatedPause - pauses)
        return now.addingTimeInterval(remaining)
    }
}
