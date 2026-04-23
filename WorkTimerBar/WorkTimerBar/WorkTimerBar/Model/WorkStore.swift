import Foundation
import Observation

/// Root container for all work days, mirroring Python's `Days` class.
@Observable
class WorkStore {
    var days: [WorkDay] = []
    /// Updated by the tick timer so the UI recomputes elapsed durations.
    var lastTick: Date = .now

    var today: WorkDay? {
        days.first { $0.isToday }
    }

    var todayIndex: Int? {
        days.firstIndex { $0.isToday }
    }

    var isTimer: Bool { today?.isRunning ?? false }
    var isPaused: Bool { today?.paused ?? false }

    /// Total overtime across all days plus the configured offset.
    /// Mirrors Python's `Today.getOvertime()`: today's overtime is 0 while running or paused.
    func totalOvertime(offsetMinutes: Int) -> TimeInterval {
        let offset = TimeInterval(offsetMinutes * 60)
        return days.reduce(offset) { acc, day in
            if day.isToday && (day.isRunning || day.paused) {
                return acc
            }
            return acc + day.overtime()
        }
    }

    /// Most recently used non-empty summaries, optionally filtered by category.
    func recentSummaries(limit: Int = 5, category: String = "") -> [String] {
        var seen = Set<String>()
        var result: [String] = []
        for day in days.sorted(by: { $0.date > $1.date }) {
            for block in day.work.reversed() {
                guard let s = block.summary, !s.isEmpty else { continue }
                if !category.isEmpty && block.category != category { continue }
                if seen.insert(s).inserted {
                    result.append(s)
                    if result.count >= limit { return result }
                }
            }
        }
        return result
    }
}
