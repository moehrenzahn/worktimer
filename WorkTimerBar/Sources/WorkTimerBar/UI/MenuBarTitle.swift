import SwiftUI

/// The label shown in the macOS menu bar.
/// - "Free" — no timer, not paused
/// - "⏸ H:MM" — paused (time since last stop)
/// - "<Category> H:MM" — timer running (elapsed)
struct MenuBarTitle: View {
    let viewModel: MenuBarViewModel

    var body: some View {
        // Access lastTick so SwiftUI re-evaluates every 30 seconds
        let _ = viewModel.store.lastTick
        Text(titleString)
    }

    private var titleString: String {
        let store = viewModel.store
        let config = viewModel.config

        if store.isPaused, let today = store.today {
            let pause = today.pauseTime()
            return "⏸ \(formatDuration(pause))"
        }

        if store.isTimer, let today = store.today, let last = today.lastWork {
            let elapsed = last.duration()
            let catName = config.displayName(for: last.category)
            return "\(catName) \(formatDuration(elapsed))"
        }

        return "Free"
    }

    private func formatDuration(_ seconds: TimeInterval) -> String {
        let h = Int(seconds) / 3600
        let m = (Int(seconds) % 3600) / 60
        return "\(h):\(String(format: "%02d", m))"
    }
}
