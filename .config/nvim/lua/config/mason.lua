-- ~/.config/nvim/lua/config/mason.lua
local mason = require("mason")

mason.setup({
    ui = {
        border = "single", -- uiのボーダー設定（変更可）
        icons = {
            package_installed = "✓", -- インストールされたパッケージのアイコン
            package_pending = "➜", -- インストール待ちのパッケージのアイコン
            package_uninstalled = "✗", -- インストールされていないパッケージのアイコン
        },
    },
    -- 他の設定（例えば、LSP、Dapのセットアップ）を加えることもできる
})
