import AppKit
import SwiftUI

/// An inline NSComboBox with case-insensitive, word-boundary autocomplete.
/// Calls `onCommit` with the trimmed string value when the user presses Return.
struct SummaryComboBox: NSViewRepresentable {
    let suggestions: [String]
    let initialValue: String
    let onCommit: (String) -> Void

    func makeNSView(context: Context) -> NSComboBox {
        let combo = NSComboBox()
        combo.placeholderString = "Update Summary"
        combo.completes = true
        combo.usesDataSource = true
        combo.dataSource = context.coordinator
        combo.delegate = context.coordinator
        combo.stringValue = initialValue
        return combo
    }

    func updateNSView(_ nsView: NSComboBox, context: Context) {
        if context.coordinator.suggestions != suggestions {
            context.coordinator.suggestions = suggestions
            nsView.reloadData()
        }
        if context.coordinator.initialValue != initialValue {
            context.coordinator.initialValue = initialValue
            nsView.stringValue = initialValue
        }
    }

    func makeCoordinator() -> Coordinator { Coordinator(suggestions: suggestions, initialValue: initialValue, onCommit: onCommit) }

    // MARK: - Coordinator

    class Coordinator: NSObject, NSComboBoxDataSource, NSComboBoxDelegate {
        var suggestions: [String]
        var initialValue: String
        let onCommit: (String) -> Void

        init(suggestions: [String], initialValue: String, onCommit: @escaping (String) -> Void) {
            self.suggestions = suggestions
            self.initialValue = initialValue
            self.onCommit = onCommit
        }

        // MARK: NSComboBoxDataSource

        func numberOfItems(in comboBox: NSComboBox) -> Int { suggestions.count }

        func comboBox(_ comboBox: NSComboBox, objectValueForItemAt index: Int) -> Any? { suggestions[index] }

        func comboBox(_ comboBox: NSComboBox, completedString string: String) -> String? {
            suggestions.first { $0.range(of: string, options: [.caseInsensitive, .anchored]) != nil }
        }

        func comboBox(_ comboBox: NSComboBox, indexOfItemWithStringValue string: String) -> Int {
            suggestions.firstIndex { $0.localizedCaseInsensitiveCompare(string) == .orderedSame } ?? NSNotFound
        }

        // MARK: NSControlTextEditingDelegate (via NSComboBoxDelegate)

        func control(_ control: NSControl, textView: NSTextView, doCommandBy commandSelector: Selector) -> Bool {
            guard commandSelector == #selector(NSResponder.insertNewline(_:)) else { return false }
            onCommit(control.stringValue.trimmingCharacters(in: .whitespaces))
            return true
        }
    }
}
