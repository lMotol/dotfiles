-- ~/.config/nvim/lua/config/mason-lspconfig.lua
local mason_lspconfig = require("mason-lspconfig")

mason_lspconfig.setup({
    ensure_installed = { "sumneko_lua", "pyright", "tsserver", "ast_grep", "clangd" }, -- 必要なLSPサーバーをリストで指定
    automatic_installation = true, -- 起動時にインストール
})

-- mason-lspconfig と nvim-lspconfig を組み合わせてLSPを設定する
local lspconfig = require("lspconfig")

mason_lspconfig.setup_handlers({
    function(server_name) -- 各LSPサーバーに対して共通の設定を行う
        lspconfig[server_name].setup({
            on_attach = function(client, bufnr)
                -- LSPに関連する設定やキーのバインディングなど
            end,
        })
    end,
})
