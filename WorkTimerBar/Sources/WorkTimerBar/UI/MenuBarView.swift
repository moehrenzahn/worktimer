import SwiftUI

/// The pulldown menu shown when clicking the menu bar item.
/// Uses only SwiftUI primitives valid inside `MenuBarExtra(.menu)`:
/// Button, Menu, Divider, Text.
struct MenuBarView: View {
    let viewModel: MenuBarViewModel

    var body: some View {
        // Access lastTick so the worked-time label stays live
        let _ = viewModel.store.lastTick

        if viewModel.projectDir == nil {
            // ── No project configured ────────────────────────────────────────
            Button("Select worktimer folder…") {
                viewModel.pickProjectDir {}
            }
            Divider()
            Button("Quit") { NSApp.terminate(nil) }
        } else {
            mainMenu
        }
    }

    @ViewBuilder
    private var mainMenu: some View {
        let store = viewModel.store
        let config = viewModel.config

        // ── "Worked X:XX" submenu ─────────────────────────────────────────
        if let today = store.today, !today.work.isEmpty {
            Menu("Worked \(formatDuration(today.workedTime()))") {
                ForEach(today.work) { block in
                    Text(blockLabel(block, config: config))
                }
            }
            Divider()
        }

        // ── Timer controls ────────────────────────────────────────────────
        if store.isPaused {
            Button("▶ Continue") { viewModel.pauseStop() }
        } else if store.isTimer {
            Button("⏹ Stop \(viewModel.currentCategoryName)") { viewModel.stopTimer() }
            Button("⏸ Pause") { viewModel.pauseStart() }
        } else {
            Button("▶ Start") { viewModel.startTimer() }
        }

        // ── Category / summary controls (not shown when paused) ───────────
        if !store.isPaused {
            if !viewModel.categories.isEmpty {
                Menu("Start Category") {
                    ForEach(viewModel.categories, id: \.key) { key, name in
                        Button(name) { viewModel.startTimer(category: key) }
                    }
                }
                if store.isTimer {
                    Menu("Update Category") {
                        ForEach(viewModel.categories, id: \.key) { key, name in
                            Button(name) { viewModel.updateCategory(key) }
                        }
                    }
                }
            }
            if store.isTimer {
                Menu("Update Summary") {
                    ForEach(viewModel.recentSummaries, id: \.self) { s in
                        Button("\"\(s)\"") { viewModel.updateSummary(s) }
                    }
                    Button("New…") { viewModel.askAndUpdateSummary() }
                }
            }
        }

        // ── Overtime info ─────────────────────────────────────────────────
        if let today = store.today {
            Divider()
            let overtime = today.overtime()
            let sign = overtime >= 0 ? "+" : ""
            Text("Overtime: \(sign)\(formatDuration(abs(overtime)))")
        }

        // ── Actions ───────────────────────────────────────────────────────
        Divider()
        Button("Open Log") { viewModel.openLog() }
        Menu("Create Report") {
            Button("Excel")        { viewModel.runReport("excel") }
            Button("OpenDocument") { viewModel.runReport("ods") }
            Button("Text")         { viewModel.runReport("text") }
        }
        if viewModel.hasSyncRepo {
            Button("Sync") { viewModel.syncRepo() }
        }
        Divider()
        Button("Change worktimer folder…") { viewModel.pickProjectDir {} }
        Button("Quit") { NSApp.terminate(nil) }
    }

    // MARK: – Helpers

    private func blockLabel(_ block: WorkBlock, config: AppConfig) -> String {
        let start = block.start.string
        let stop = block.stop?.string ?? "now"
        let cat = config.displayName(for: block.category)
        if let s = block.summary, !s.isEmpty {
            return "\(start)–\(stop)  \(cat)  \(s)"
        }
        return "\(start)–\(stop)  \(cat)"
    }

    private func formatDuration(_ seconds: TimeInterval) -> String {
        let total = Int(abs(seconds))
        let h = total / 3600
        let m = (total % 3600) / 60
        return "\(h):\(String(format: "%02d", m))"
    }
}
