import Foundation

enum ConfigLoader {

    /// Loads config by merging `config_default.json` (base) with `config.json` (overrides).
    /// The merge happens at the JSON dictionary level so partial user configs don't
    /// wipe fields that exist only in the defaults.
    static func load(from projectDir: URL) -> AppConfig {
        let defaultURL = projectDir.appendingPathComponent("config_default.json")
        let userURL    = projectDir.appendingPathComponent("config.json")

        var baseDict: [String: Any] = loadDict(from: defaultURL) ?? [:]
        if let userDict = loadDict(from: userURL) {
            for (k, v) in userDict { baseDict[k] = v }
        }

        guard let merged = try? JSONSerialization.data(withJSONObject: baseDict),
              var config = try? JSONDecoder().decode(AppConfig.self, from: merged) else {
            return AppConfig()
        }

        // The [String: Any] merge loses JSON key order for `categories`.
        // Re-read categories by scanning the raw JSON text for key order.
        config.categories = orderedCategories(preferring: userURL, fallback: defaultURL)
        return config
    }

    private static func loadDict(from url: URL) -> [String: Any]? {
        guard let data = try? Data(contentsOf: url),
              let obj  = try? JSONSerialization.jsonObject(with: data),
              let dict = obj as? [String: Any] else { return nil }
        return dict
    }

    /// Returns (key, value) pairs for the `categories` object, in JSON source order.
    /// Prefers the user config; falls back to the default config.
    private static func orderedCategories(
        preferring primary: URL,
        fallback secondary: URL
    ) -> [(key: String, value: String)] {
        for url in [primary, secondary] {
            guard let data = try? Data(contentsOf: url),
                  let dict = (try? JSONSerialization.jsonObject(with: data)) as? [String: Any],
                  let rawCats = dict["categories"] as? [String: Any],
                  !rawCats.isEmpty,
                  let keys = categoryKeysInOrder(from: data),
                  !keys.isEmpty else { continue }

            let result = keys.compactMap { key -> (key: String, value: String)? in
                guard let value = rawCats[key] as? String else { return nil }
                return (key: key, value: value)
            }
            if !result.isEmpty { return result }
        }
        return []
    }

    /// Scans the raw JSON text to extract the keys of the `"categories"` object
    /// in the order they appear in the source file.
    private static func categoryKeysInOrder(from data: Data) -> [String]? {
        guard let text = String(data: data, encoding: .utf8),
              let catRange = text.range(of: "\"categories\"") else { return nil }

        var i = catRange.upperBound

        // Advance past whitespace and ':'
        while i < text.endIndex, " \t\n\r:".contains(text[i]) { i = text.index(after: i) }
        guard i < text.endIndex, text[i] == "{" else { return nil }
        i = text.index(after: i)

        var keys: [String] = []
        var depth = 0

        while i < text.endIndex {
            switch text[i] {
            case "{":
                depth += 1
                i = text.index(after: i)
            case "}":
                if depth == 0 { return keys.isEmpty ? nil : keys }
                depth -= 1
                i = text.index(after: i)
            case "\"" where depth == 0:
                // Parse the string content
                i = text.index(after: i)
                var str = ""
                while i < text.endIndex, text[i] != "\"" {
                    if text[i] == "\\" {
                        i = text.index(after: i)
                        if i < text.endIndex { str.append(text[i]); i = text.index(after: i) }
                    } else {
                        str.append(text[i]); i = text.index(after: i)
                    }
                }
                if i < text.endIndex { i = text.index(after: i) } // skip closing "

                // If the next non-whitespace char is ':', this string is a key
                var j = i
                while j < text.endIndex, " \t\n\r".contains(text[j]) { j = text.index(after: j) }
                if j < text.endIndex, text[j] == ":" { keys.append(str) }

            default:
                i = text.index(after: i)
            }
        }
        return keys.isEmpty ? nil : keys
    }
}
