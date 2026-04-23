import SwiftUI

private struct DayRow: Identifiable {
    let id = UUID()
    let start: HourMinute
    let stop: HourMinute?   // nil = currently active
    let label: String
    let detail: String
    let isRunning: Bool
    let isPause: Bool

    var duration: TimeInterval {
        let s = stop ?? HourMinute.now()
        return TimeInterval(max(0, (s.hour - start.hour) * 3600 + (s.minute - start.minute) * 60))
    }
}

struct MenuBarView: View {
    let viewModel: MenuBarViewModel
    @Environment(\.dismiss) private var dismiss

    /// Runs an action then dismisses the popover.
    private func perform(_ action: () -> Void) {
        action()
        dismiss()
    }

    var body: some View {
        let _ = viewModel.store.lastTick
        VStack(spacing: 0) {
            if viewModel.projectDir == nil {
                setupSection
            } else {
                mainContent
            }
        }
        .frame(width: 370)
    }

    // MARK: – Setup

    private var setupSection: some View {
        VStack(spacing: 12) {
            Text("Select your worktimer folder to get started.")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)
            Button("Select Folder…") { viewModel.pickProjectDir {} }
                .buttonStyle(.borderedProminent)
        }
        .padding(20)
    }

    // MARK: – Main content

    @ViewBuilder
    private var mainContent: some View {
        let store = viewModel.store

        statusSection
        Divider()
        statsSection
        if let today = store.today, !today.work.isEmpty {
            Divider()
            blocksSection(today: today)
        }
        Divider()
        actionsSection
    }

    // MARK: – Status

    private var statusSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .center, spacing: 10) {
                statusContent
                Spacer()
                statusButtons
            }
            if viewModel.store.isTimer {
                updateControls
            }
        }
        .padding(.horizontal, 14)
        .padding(.vertical, 10)
    }

    @ViewBuilder
    private var statusContent: some View {
        let store = viewModel.store
        let config = viewModel.config

        if store.isPaused, let today = store.today {
            Image(systemName: "pause.fill").foregroundStyle(.orange)
            Text("Paused")
            Text(formatDuration(today.pauseTime()))
                .monospacedDigit()
                .foregroundStyle(.secondary)
        } else if store.isTimer, let today = store.today, let last = today.lastWork {
            VStack(alignment: .leading, spacing: 3) {
                HStack(spacing: 8) {
                    Text(config.displayName(for: last.category))
                        .fontWeight(.semibold)
                    if let s = last.summary, !s.isEmpty {
                        Text(s).foregroundStyle(.secondary)
                    }
                    Text(formatDuration(last.duration()))
                        .monospacedDigit()
                        .foregroundStyle(.secondary)
                }
                .lineLimit(1)
            }
        } else {
            Text("Free").foregroundStyle(.secondary)
        }
    }

    @ViewBuilder
    private var updateControls: some View {
        HStack(spacing: 8) {
            if !viewModel.categories.isEmpty {
                Menu {
                    ForEach(viewModel.categories, id: \.key) { key, name in
                        Button(name) { viewModel.updateCategory(key) }
                    }
                } label: {
                    Label("Update Category", systemImage: "tag")
                }
                .buttonStyle(.bordered)
                .fixedSize()
            }
            SummaryComboBox(
                suggestions: viewModel.recentSummaries,
                initialValue: viewModel.store.today?.lastWork?.summary ?? "",
                onCommit: viewModel.updateSummary
            )
            .frame(height: 24)
        }
    }

    @ViewBuilder
    private var statusButtons: some View {
        let store = viewModel.store

        if store.isPaused {
            Button { perform { viewModel.pauseStop() } } label: {
                Label("Continue", systemImage: "play.fill")
            }
            .buttonStyle(.borderedProminent)
        } else if store.isTimer {
            Button { perform { viewModel.pauseStart() } } label: {
                Label("Pause", systemImage: "pause.fill")
            }
            .buttonStyle(.bordered)
            Button { perform { viewModel.stopTimer() } } label: {
                Label("Stop", systemImage: "stop.fill")
            }
            .buttonStyle(.borderedProminent)
        } else {
            Button { perform { viewModel.startTimer() } } label: {
                Label("Start", systemImage: "play.fill")
            }
            .buttonStyle(.borderedProminent)
        }
    }

    // MARK: – Blocks table

    private func blocksSection(today: WorkDay) -> some View {
        let config = viewModel.config
        let sorted = today.work.sorted {
            $0.start.hour != $1.start.hour
                ? $0.start.hour < $1.start.hour
                : $0.start.minute < $1.start.minute
        }

        var rows: [DayRow] = []
        for (i, block) in sorted.enumerated() {
            // Insert pause row for the gap before this block
            if i > 0, let prevStop = sorted[i - 1].stop {
                let gap = (block.start.hour - prevStop.hour) * 3600 + (block.start.minute - prevStop.minute) * 60
                if gap > 0 {
                    rows.append(DayRow(start: prevStop, stop: block.start, label: "Pause", detail: "", isRunning: false, isPause: true))
                }
            }
            rows.append(DayRow(start: block.start, stop: block.stop, label: config.displayName(for: block.category), detail: block.summary ?? "", isRunning: block.isRunning, isPause: false))
        }
        // Current ongoing pause
        if today.paused, let lastStop = sorted.last?.stop {
            rows.append(DayRow(start: lastStop, stop: nil, label: "Pause", detail: "", isRunning: true, isPause: true))
        }

        return Grid(alignment: .leading, horizontalSpacing: 14, verticalSpacing: 0) {
            ForEach(rows) { row in
                GridRow {
                    Text("\(row.start.string)–\(row.stop?.string ?? "now")")
                        .monospacedDigit()
                        .foregroundStyle(row.isRunning ? .primary : .secondary)
                        .padding(.vertical, 3)
                        .gridColumnAlignment(.leading)
                    Text(row.label)
                        .foregroundStyle(row.isRunning ? .primary : .secondary)
                        .gridColumnAlignment(.leading)
                    Text(row.detail)
                        .lineLimit(1)
                        .truncationMode(.tail)
                        .foregroundStyle(row.isRunning ? .secondary : .tertiary)
                        .gridColumnAlignment(.leading)
                    Text(formatDuration(row.duration))
                        .monospacedDigit()
                        .foregroundStyle(row.isRunning ? .primary : .secondary)
                        .gridColumnAlignment(.trailing)
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(.horizontal, 14)
        .padding(.vertical, 8)
    }

    // MARK: – Stats

    private var statsSection: some View {
        let store = viewModel.store
        let config = viewModel.config

        return HStack(spacing: 0) {
            if let today = store.today {
                statTile(label: "Worked", value: formatDuration(today.workedTime()))
                if store.isTimer || store.isPaused {
                    let remaining = today.remainingWork()
                    Divider().frame(height: 32)
                    statTile(label: "Remaining", value: formatSigned(remaining))
                    if let endDate = today.projectedEndTime() {
                        let comps = Calendar.current.dateComponents([.hour, .minute], from: endDate)
                        let hm = HourMinute(hour: comps.hour ?? 0, minute: comps.minute ?? 0)
                        Divider().frame(height: 32)
                        statTile(label: "End", value: hm.string)
                    }
                }
                let ot = store.totalOvertime(offsetMinutes: config.overtimeOffsetInMinutes)
                Divider().frame(height: 32)
                statTile(label: "Overtime", value: (ot >= 0 ? "+" : "−") + formatDuration(abs(ot)))
            }
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 8)
    }

    private func statTile(label: String, value: String) -> some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(label).foregroundStyle(.secondary).lineLimit(1)
            Text(value).monospacedDigit().fontWeight(.medium).lineLimit(1)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(.horizontal, 14)
    }

    // MARK: – Actions

    private var actionsSection: some View {
        let store = viewModel.store

        return VStack(alignment: .leading, spacing: 0) {
            // Start Category — own line
            if !store.isPaused, !viewModel.categories.isEmpty {
                Menu {
                    ForEach(viewModel.categories, id: \.key) { key, name in
                        Button(name) { perform { viewModel.askAndStartTimer(category: key) } }
                    }
                } label: {
                    Label("Start New Category", systemImage: "tag.fill")
                }
                .buttonStyle(.borderedProminent)
                .fixedSize()
                .padding(14)
                Divider()
            }

            // Bottom bar: Open Log + overflow
            HStack(spacing: 8) {
                Button("Open Log") { perform { viewModel.openLog() } }
                    .buttonStyle(.bordered)
                    .fixedSize()

                Spacer()

                Menu {
                    Menu("Report") {
                        Button("Excel")        { perform { viewModel.runReport("excel") } }
                        Button("OpenDocument") { perform { viewModel.runReport("ods") } }
                        Button("Text")         { perform { viewModel.runReport("text") } }
                    }
                    if viewModel.hasSyncRepo {
                        Button("Sync") { perform { viewModel.syncRepo() } }
                    }
                    Divider()
                    Button("Change Folder…") { viewModel.pickProjectDir {} }
                    Divider()
                    Button("Quit") { NSApp.terminate(nil) }
                } label: {
                    Label("More", systemImage: "ellipsis.circle")
                }
                .labelStyle(.iconOnly)
                .buttonStyle(.borderless)
                .fixedSize()
            }
            .padding(14)
            .background(Color(NSColor.windowBackgroundColor))
            .environment(\.colorScheme, .dark)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    // MARK: – Helpers

    private func formatDuration(_ seconds: TimeInterval) -> String {
        let total = Int(abs(seconds))
        let h = total / 3600
        let m = (total % 3600) / 60
        return "\(h):\(String(format: "%02d", m))"
    }

    private func formatSigned(_ seconds: TimeInterval) -> String {
        return (seconds < 0 ? "−" : "") + formatDuration(seconds)
    }
}
