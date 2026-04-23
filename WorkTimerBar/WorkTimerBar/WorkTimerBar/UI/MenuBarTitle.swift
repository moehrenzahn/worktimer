import SwiftUI

/// The label shown in the macOS menu bar.
/// - "Free" — no timer, not paused
/// - SF pause symbol + pause time — paused
/// - "Remaining – Category [Summary] Duration" — timer running
struct MenuBarTitle: View {
    let viewModel: MenuBarViewModel

    var body: some View {
        // Access lastTick so SwiftUI re-evaluates every 30 seconds
        let _ = viewModel.store.lastTick
        titleView
    }

    @ViewBuilder
    private var titleView: some View {
        let store = viewModel.store
        let config = viewModel.config

        if store.isPaused, let today = store.today {
            HStack(spacing: 4) {
                Image(systemName: "pause.fill")
                Text(formatDuration(today.pauseTime()))
            }
        } else if store.isTimer, let today = store.today, let last = today.lastWork {
            let remaining = today.remainingWork()
            let remStr = (remaining < 0 ? "−" : "") + formatDuration(remaining)
            let catName = config.displayName(for: last.category)
            if let summary = last.summary, !summary.isEmpty {
                Text("\(remStr) – \(catName) \(summary.prefix(10))… \(formatDuration(last.duration()))")
            } else {
                Text("\(remStr) – \(catName) \(formatDuration(last.duration()))")
            }
        } else {
            Text("Free")
        }
    }

    private func formatDuration(_ seconds: TimeInterval) -> String {
        let total = Int(abs(seconds))
        let h = total / 3600
        let m = (total % 3600) / 60
        return "\(h):\(String(format: "%02d", m))"
    }
}
