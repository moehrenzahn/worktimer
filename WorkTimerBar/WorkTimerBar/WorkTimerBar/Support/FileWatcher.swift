import Foundation
import CoreServices

/// Watches a directory for file changes using FSEventStream.
/// The callback is delivered on the main queue with ~500ms latency.
final class FileWatcher {
    private var stream: FSEventStreamRef?
    private let callback: () -> Void
    private let watchedURL: URL

    init(url: URL, callback: @escaping () -> Void) {
        self.watchedURL = url.deletingLastPathComponent()
        self.callback = callback
        start()
    }

    deinit {
        stop()
    }

    private func start() {
        let paths = [watchedURL.path] as CFArray
        var ctx = FSEventStreamContext(
            version: 0,
            info: Unmanaged.passRetained(self).toOpaque(),
            retain: nil,
            release: { ptr in Unmanaged<FileWatcher>.fromOpaque(ptr!).release() },
            copyDescription: nil
        )
        stream = FSEventStreamCreate(
            nil,
            { _, info, _, _, _, _ in
                let watcher = Unmanaged<FileWatcher>.fromOpaque(info!).takeUnretainedValue()
                DispatchQueue.main.async { watcher.callback() }
            },
            &ctx,
            paths,
            FSEventStreamEventId(kFSEventStreamEventIdSinceNow),
            0.5,
            FSEventStreamCreateFlags(kFSEventStreamCreateFlagFileEvents | kFSEventStreamCreateFlagUseCFTypes)
        )
        guard let s = stream else { return }
        FSEventStreamSetDispatchQueue(s, DispatchQueue.main)
        FSEventStreamStart(s)
    }

    private func stop() {
        guard let s = stream else { return }
        FSEventStreamStop(s)
        FSEventStreamInvalidate(s)
        FSEventStreamRelease(s)
        stream = nil
    }
}
