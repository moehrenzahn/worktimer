import Foundation

/// Mirrors `config_default.json` + `config.json`.
/// `Decodable` only — AppConfig is never serialized back to JSON.
struct AppConfig: Decodable {
    var log: String = "database/work"
    var notifications: Bool = true
    var textbar: Bool = false
    var defaultCategory: String? = nil
    var hoursPerDay: Double = 8.0
    /// Ordered as they appear in the config file.
    var categories: [(key: String, value: String)] = []
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

    // Custom decoder so categories use `allKeys` order rather than dict hash order.
    init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        log                    = (try? c.decode(String.self,  forKey: .log))                    ?? "database/work"
        notifications          = (try? c.decode(Bool.self,    forKey: .notifications))          ?? true
        textbar                = (try? c.decode(Bool.self,    forKey: .textbar))                ?? false
        defaultCategory        =  try? c.decode(String.self,  forKey: .defaultCategory)
        hoursPerDay            = (try? c.decode(Double.self,  forKey: .hoursPerDay))            ?? 8.0
        overtimeOffsetInMinutes = (try? c.decode(Int.self,   forKey: .overtimeOffsetInMinutes)) ?? 0
        syncRepoUrl            = (try? c.decode(String.self,  forKey: .syncRepoUrl))            ?? ""
        syncAutomatically      = (try? c.decode(Bool.self,    forKey: .syncAutomatically))      ?? false

        // Order is patched by ConfigLoader after decoding; decode here just to populate values.
        if let dict = try? c.decode([String: String].self, forKey: .categories) {
            categories = dict.map { (key: $0.key, value: $0.value) }
        }
    }

    init() {}

    var goalSeconds: TimeInterval { hoursPerDay * 3600 }

    /// Returns the display name for a category key, falling back to title-cased key.
    func displayName(for category: String) -> String {
        if let pair = categories.first(where: { $0.key == category }) { return pair.value }
        return category
            .replacingOccurrences(of: "_", with: " ")
            .split(separator: " ")
            .map { $0.prefix(1).uppercased() + $0.dropFirst() }
            .joined(separator: " ")
    }
}
