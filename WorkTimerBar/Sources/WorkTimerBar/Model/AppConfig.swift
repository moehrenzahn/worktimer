import Foundation

/// Mirrors `config_default.json` + `config.json`.
struct AppConfig: Codable {
    var log: String = "database/work"
    var notifications: Bool = true
    var textbar: Bool = false
    var defaultCategory: String? = nil
    var hoursPerDay: Double = 8.0
    var categories: [String: String] = [:]
    var overtimeOffsetInMinutes: Int = 0
    var syncRepoUrl: String = ""
    var syncAutomatically: Bool = false

    enum CodingKeys: String, CodingKey {
        case log
        case notifications
        case textbar
        case defaultCategory = "default_category"
        case hoursPerDay = "hours_per_day"
        case categories
        case overtimeOffsetInMinutes = "overtime_offset_in_minutes"
        case syncRepoUrl = "sync_repo_url"
        case syncAutomatically = "sync_automatically"
    }

    var goalSeconds: TimeInterval { hoursPerDay * 3600 }

    /// Returns the display name for a category code, falling back to title-cased key.
    func displayName(for category: String) -> String {
        if let name = categories[category] { return name }
        return category
            .replacingOccurrences(of: "_", with: " ")
            .split(separator: " ")
            .map { $0.prefix(1).uppercased() + $0.dropFirst() }
            .joined(separator: " ")
    }
}
