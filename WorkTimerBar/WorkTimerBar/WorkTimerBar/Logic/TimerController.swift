import Foundation

/// Implements start/stop/pause/update operations on the WorkStore, then
/// persists to disk. Mirrors the Python `actions/timer.py` and `actions/pause.py`
/// and `actions/change.py` logic exactly — including edge cases.
@MainActor
class TimerController {
    let store: WorkStore
    let config: AppConfig
    let yamlURL: URL

    init(store: WorkStore, config: AppConfig, yamlURL: URL) {
        self.store = store
        self.config = config
        self.yamlURL = yamlURL
    }

    // MARK: – Timer

    /// Start or stop the timer. If already running the same category: stop.
    /// If running a different category: stop that one first, then start new.
    /// Mirrors Python `actions/timer.py:timer()`.
    func startTimer(category: String = "", summary: String? = nil) throws {
        guard !store.isPaused else {
            NotificationManager.shared.send(title: "Timer Paused", body: "End your break before starting a new timer.")
            return
        }
        let cat = category.isEmpty ? (config.defaultCategory ?? "") : category
        let now = HourMinute.now()
        let today = Calendar.current.startOfDay(for: Date())

        if let idx = store.todayIndex {
            // Stop any running block
            for i in store.days[idx].work.indices where store.days[idx].work[i].isRunning {
                store.days[idx].work[i].stop = now
            }
            store.days[idx].work.append(WorkBlock(start: now, stop: nil, category: cat, summary: summary))
        } else {
            let newDay = WorkDay(
                date: today,
                goal: config.goalSeconds,
                comment: nil,
                work: [WorkBlock(start: now, stop: nil, category: cat, summary: summary)],
                paused: false
            )
            store.days.append(newDay)
        }
        try save()

        let endMsg = endTimeString()
        let catName = config.displayName(for: cat)
        NotificationManager.shared.send(
            title: "Timer Started",
            body: "Working on \(catName). Done at approx. \(endMsg)."
        )
    }

    /// Stop all running work blocks for today.
    func stopTimer() throws {
        guard let idx = store.todayIndex else { return }
        let now = HourMinute.now()
        for i in store.days[idx].work.indices where store.days[idx].work[i].isRunning {
            store.days[idx].work[i].stop = now
        }
        try save()
        NotificationManager.shared.send(title: "Timer Stopped", body: workedTodayString())
    }

    // MARK: – Pause

    /// Start a break: stop all running work, set paused flag.
    /// Mirrors Python `actions/pause.py:pauseStart()`.
    func pauseStart() throws {
        guard !store.isPaused else { return }
        let now = HourMinute.now()

        if let idx = store.todayIndex {
            for i in store.days[idx].work.indices where store.days[idx].work[i].isRunning {
                store.days[idx].work[i].stop = now
            }
            store.days[idx].paused = true
        } else {
            // No work today yet — create a day entry in paused state
            let newDay = WorkDay(
                date: Calendar.current.startOfDay(for: Date()),
                goal: config.goalSeconds,
                comment: nil,
                work: [],
                paused: true
            )
            store.days.append(newDay)
        }
        try save()
        let hm = HourMinute.now()
        NotificationManager.shared.send(title: "Break Started", body: "Break started at \(hm.string).")
    }

    /// End a break: if break duration was 0 minutes, undo the stop (continue
    /// previous block). Otherwise start a new block resuming previous category.
    /// Mirrors Python `actions/pause.py:pauseStop()`.
    func pauseStop() throws {
        guard let idx = store.todayIndex, store.days[idx].paused else { return }
        let now = HourMinute.now()
        store.days[idx].paused = false

        if let lastIdx = store.days[idx].work.indices.last {
            let last = store.days[idx].work[lastIdx]
            if let lastStop = last.stop, lastStop == now {
                // 0-minute break — just undo the stop
                store.days[idx].work[lastIdx].stop = nil
            } else {
                // Resume with same category + summary
                store.days[idx].work.append(
                    WorkBlock(start: now, stop: nil, category: last.category, summary: last.summary)
                )
            }
        }
        try save()

        let pauseDuration = store.today?.pauseTime() ?? 0
        NotificationManager.shared.send(
            title: "Break Ended",
            body: "Total break time: \(formatDuration(pauseDuration))."
        )
    }

    // MARK: – Update Category / Summary

    /// Update category and/or summary of the most recent work block.
    /// If category changes and no new summary is given, summary is cleared.
    /// Mirrors Python `actions/change.py:change()`.
    func updateCategory(_ category: String, summary: String? = nil) throws {
        guard let idx = store.todayIndex,
              let workIdx = store.days[idx].work.indices.last else { return }

        let oldCategory = store.days[idx].work[workIdx].category
        var changed = false

        if !category.isEmpty && category != oldCategory {
            store.days[idx].work[workIdx].category = category
            if summary == nil {
                store.days[idx].work[workIdx].summary = nil
            }
            changed = true
        }
        if let s = summary, s != store.days[idx].work[workIdx].summary {
            store.days[idx].work[workIdx].summary = s.isEmpty ? nil : s
            changed = true
        }

        guard changed else { return }
        try save()

        let catName = config.displayName(for: store.days[idx].work[workIdx].category)
        let summaryPart = store.days[idx].work[workIdx].summary.map { " — \($0)" } ?? ""
    }

    // MARK: – Persistence

    func save() throws {
        try YAMLCoder.save(store, to: yamlURL)
    }

    // MARK: – Helpers

    private func endTimeString() -> String {
        guard let projected = store.today?.projectedEndTime() else { return "?" }
        let formatter = DateFormatter()
        formatter.dateFormat = "H:mm"
        return formatter.string(from: projected)
    }

    private func workedTodayString() -> String {
        guard let today = store.today else { return "" }
        return "Worked \(formatDuration(today.workedTime())) today."
    }

    private func formatDuration(_ seconds: TimeInterval) -> String {
        let h = Int(seconds) / 3600
        let m = (Int(seconds) % 3600) / 60
        return "\(h):\(String(format: "%02d", m))"
    }
}
