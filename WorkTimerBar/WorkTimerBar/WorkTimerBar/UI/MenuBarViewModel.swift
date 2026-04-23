import Foundation
import AppKit
import Observation

private class CaseInsensitiveComboDataSource: NSObject, NSComboBoxDataSource {
    let items: [String]
    init(items: [String]) { self.items = items }

    func numberOfItems(in comboBox: NSComboBox) -> Int { items.count }

    func comboBox(_ comboBox: NSComboBox, objectValueForItemAt index: Int) -> Any? { items[index] }

    func comboBox(_ comboBox: NSComboBox, completedString string: String) -> String? {
        items.first { item in
            item.components(separatedBy: .whitespaces).contains { word in
                word.range(of: string, options: [.caseInsensitive, .anchored]) != nil
            }
        }
    }

    func comboBox(_ comboBox: NSComboBox, indexOfItemWithStringValue string: String) -> Int {
        items.firstIndex { $0.localizedCaseInsensitiveCompare(string) == .orderedSame } ?? NSNotFound
    }
}

/// The central view model: owns the store, config, controller, file watcher, and tick timer.
/// All mutation goes through `TimerController`; the SwiftUI views are read-only.
@Observable
@MainActor
class MenuBarViewModel {
    let store = WorkStore()
    private(set) var config = AppConfig()
    private var controller: TimerController?
    private var fileWatcher: FileWatcher?
    private var tickTimer: Timer?
    private(set) var projectDir: URL?
    private(set) var yamlURL: URL?

    init() {
        if let dir = resolveProjectDir() {
            configure(with: dir)
        }
    }

    // MARK: – Setup

    /// Loads from a project directory and starts all watchers.
    func configure(with dir: URL) {
        projectDir = dir
        config = ConfigLoader.load(from: dir)
        let yaml = dir.appendingPathComponent(config.log + ".yaml")
        yamlURL = yaml
        controller = TimerController(store: store, config: config, yamlURL: yaml)
        reload()
        startTickTimer()
        startFileWatcher(yaml: yaml)
        NotificationManager.shared.requestAuthorization()
    }

    func reload() {
        guard let url = yamlURL else { return }
        do {
            let days = try YAMLCoder.load(from: url)
            store.days = days
        } catch {
            // Preserve previous state on parse error; don't crash
        }
    }

    // MARK: – Timer actions

    func startTimer(category: String = "", summary: String? = nil) {
        let cat = category.isEmpty ? (config.defaultCategory ?? "") : category
        try? controller?.startTimer(category: cat, summary: summary)
    }

    func stopTimer() {
        try? controller?.stopTimer()
    }

    func pauseStart() {
        try? controller?.pauseStart()
    }

    func pauseStop() {
        try? controller?.pauseStop()
    }

    func updateCategory(_ category: String, summary: String? = nil) {
        try? controller?.updateCategory(category, summary: summary)
    }

    func updateSummary(_ summary: String) {
        let cat = store.today?.lastWork?.category ?? ""
        try? controller?.updateCategory(cat, summary: summary)
    }

    /// Shows a combo-box dialog to pick/type a summary, then starts the timer.
    func askAndStartTimer(category: String) {
        let recent = store.recentSummaries(limit: 10, category: category)
        let catName = config.displayName(for: category)
        showComboDialog(
            title: "Start \(catName)",
            message: "Enter a summary (optional):",
            suggestions: recent
        ) { [weak self] result in
            guard let result else { return }
            let summary = result.isEmpty ? nil : result
            self?.startTimer(category: category, summary: summary)
        }
    }

    /// Shows an NSAlert dialog for entering a summary, then applies it.
    func askAndUpdateSummary() {
        let recentCat = store.today?.lastWork?.category ?? ""
        let recent = store.recentSummaries(limit: 10, category: recentCat)
        let catName = config.displayName(for: recentCat)
        showComboDialog(
            title: "Update Summary",
            message: "Enter a summary for \(catName):",
            suggestions: recent
        ) { [weak self] result in
            guard let s = result, !s.isEmpty else { return }
            self?.updateSummary(s)
        }
    }

    // MARK: – Other actions

    func openLog() {
        guard let url = yamlURL else { return }
        NSWorkspace.shared.open(url)
    }

    func runReport(_ format: String) {
        guard let dir = projectDir else { return }
        let pythonScript = dir.appendingPathComponent("WorkTimer.py").path
        let proc = Process()
        proc.executableURL = URL(fileURLWithPath: "/opt/homebrew/bin/python3")
        proc.arguments = [pythonScript, "report", format]
        proc.currentDirectoryURL = dir
        try? proc.run()
    }

    func syncRepo() {
        guard let dir = projectDir else { return }
        let pythonScript = dir.appendingPathComponent("WorkTimer.py").path
        let proc = Process()
        proc.executableURL = URL(fileURLWithPath: "/opt/homebrew/bin/python3")
        proc.arguments = [pythonScript, "sync"]
        proc.currentDirectoryURL = dir
        do {
            try proc.run()
        } catch {
            print(error)
        }
    }

    // MARK: – Computed helpers

    var categories: [(key: String, value: String)] {
        config.categories
    }

    var recentSummaries: [String] {
        let cat = store.today?.lastWork?.category ?? ""
        return store.recentSummaries(limit: 20, category: cat)
    }

    var currentCategoryName: String {
        let cat = store.today?.lastWork?.category ?? ""
        return config.displayName(for: cat)
    }

    var hasSyncRepo: Bool { !config.syncRepoUrl.isEmpty }

    // MARK: – Private

    private func startTickTimer() {
        tickTimer?.invalidate()
        tickTimer = Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in
            Task { @MainActor [weak self] in
                self?.store.lastTick = .now
            }
        }
    }

    private func startFileWatcher(yaml: URL) {
        fileWatcher = FileWatcher(url: yaml) { [weak self] in
            self?.reload()
        }
    }

    private func resolveProjectDir() -> URL? {
        // Check UserDefaults for a previously chosen directory
        if let bookmarkData = UserDefaults.standard.data(forKey: "projectDirBookmark") {
            var isStale = false
            if let url = try? URL(
                resolvingBookmarkData: bookmarkData,
                options: .withSecurityScope,
                relativeTo: nil,
                bookmarkDataIsStale: &isStale
            ) {
                _ = url.startAccessingSecurityScopedResource()
                if isStale { saveBookmark(for: url) }
                return url
            }
        }
        return nil
    }

    func pickProjectDir(completion: @escaping () -> Void) {
        let panel = NSOpenPanel()
        panel.message = "Select the worktimer project folder"
        panel.prompt = "Select"
        panel.canChooseFiles = false
        panel.canChooseDirectories = true
        panel.allowsMultipleSelection = false
        panel.begin { [weak self] response in
            guard response == .OK, let url = panel.url else { return }
            self?.saveBookmark(for: url)
            self?.configure(with: url)
            completion()
        }
    }

    private func saveBookmark(for url: URL) {
        let data = try? url.bookmarkData(
            options: .withSecurityScope,
            includingResourceValuesForKeys: nil,
            relativeTo: nil
        )
        UserDefaults.standard.set(data, forKey: "projectDirBookmark")
    }

    private func showComboDialog(
        title: String,
        message: String,
        suggestions: [String],
        completion: @escaping (String?) -> Void
    ) {
        let alert = NSAlert()
        alert.messageText = title
        alert.informativeText = message
        alert.addButton(withTitle: "OK")
        alert.addButton(withTitle: "Cancel")

        let combo = NSComboBox(frame: NSRect(x: 0, y: 0, width: 300, height: 24))
        combo.placeholderString = "Summary…"
        combo.completes = true
        combo.usesDataSource = true
        let dataSource = CaseInsensitiveComboDataSource(items: suggestions)
        combo.dataSource = dataSource
        alert.accessoryView = combo
        alert.window.initialFirstResponder = combo

        let response = alert.runModal()
        _ = dataSource  // keep alive for the duration of the modal
        if response == .alertFirstButtonReturn {
            completion(combo.stringValue.trimmingCharacters(in: .whitespaces))
        } else {
            completion(nil)
        }
    }
}
