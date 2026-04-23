import SwiftUI

@main
struct WorkTimerBarApp: App {
    @State private var viewModel = MenuBarViewModel()

    var body: some Scene {
        MenuBarExtra {
            MenuBarView(viewModel: viewModel)
        } label: {
            MenuBarTitle(viewModel: viewModel)
        }
        .menuBarExtraStyle(.menu)
    }
}
