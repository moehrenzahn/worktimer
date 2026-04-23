import Foundation

enum ConfigLoader {

    /// Loads config by merging `config_default.json` (base) with `config.json` (overrides).
    /// The merge happens at the JSON dictionary level so partial user configs don't
    /// wipe fields that exist only in the defaults.
    static func load(from projectDir: URL) -> AppConfig {
        let defaultURL = projectDir.appendingPathComponent("config_default.json")
        let userURL = projectDir.appendingPathComponent("config.json")

        // Start from defaults
        var baseDict: [String: Any] = loadDict(from: defaultURL) ?? [:]

        // Overlay user config keys
        if let userDict = loadDict(from: userURL) {
            for (k, v) in userDict { baseDict[k] = v }
        }

        // Re-encode merged dict → decode into AppConfig
        guard let merged = try? JSONSerialization.data(withJSONObject: baseDict),
              let config = try? JSONDecoder().decode(AppConfig.self, from: merged) else {
            return AppConfig()
        }
        return config
    }

    private static func loadDict(from url: URL) -> [String: Any]? {
        guard let data = try? Data(contentsOf: url),
              let obj = try? JSONSerialization.jsonObject(with: data),
              let dict = obj as? [String: Any] else { return nil }
        return dict
    }
}
