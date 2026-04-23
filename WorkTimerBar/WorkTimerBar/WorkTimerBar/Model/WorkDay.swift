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

    /// Time spent on breaks (gaps between consecutive work blocks), plus the current
    /// ongoing pause if `paused == true`. Mirrors Python's `Day.getPausetime()`.
    func pauseTime(now: Date = .now) -> TimeInterval {
        let sorted = work.sorted { a, b in
            a.start.hour < b.start.hour ||
            (a.start.hour == b.start.hour && a.start.minute < b.start.minute)
        }
        var total: TimeInterval = 0
        for i in 1..<sorted.count {
            if let ps = sorted[i - 1].stop {
                let curStart = sorted[i].start
                let gap = TimeInterval((curStart.hour - ps.hour) * 3600 + (curStart.minute - ps.minute) * 60)
                if gap > 0 { total += gap }
            }
        }
        // Include the current ongoing pause (from last work stop to now)
        if paused, let lastStop = sorted.last?.stop {
            let base = Calendar.current.startOfDay(for: now)
            let stopDate = base.addingTimeInterval(TimeInterval(lastStop.hour * 3600 + lastStop.minute * 60))
            let currentPause = now.timeIntervalSince(stopDate)
            if currentPause > 0 { total += currentPause }
        }
        return total
    }

    /// Remaining work to reach goal. Negative = overtime already accrued.
    func remainingWork(now: Date = .now) -> TimeInterval {
        goal - workedTime(now: now)
    }

    /// Overtime (positive = over goal, negative = under).
    func overtime(now: Date = .now) -> TimeInterval {
        workedTime(now: now) - goal
    }

    /// Projected end-of-day time. Only meaningful while running and not yet past goal.
    func projectedEndTime(now: Date = .now) -> Date? {
        guard isRunning, remainingWork(now: now) > 0 else { return nil }
        return now.addingTimeInterval(remainingWork(now: now))
    }
}
