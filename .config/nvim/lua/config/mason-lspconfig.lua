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

lspconfig.clangd.setup({
    cmd = {
        "clangd",
        "--background-index",
        "--clang-tidy",
        "--completion-style=detailed",
        "--header-insertion=never",
        "--fallback-style=LLVM", -- .clang-formatが存在しない場合のフォールバックスタイル
    },
    on_attach = function(client, bufnr)
        -- 必要に応じてキー設定や他の設定を追加

        -- 自動フォーマットを有効にする場合（例: 保存時にフォーマット）
        vim.api.nvim_create_autocmd("BufWritePre", {
            buffer = bufnr,
            callback = function()
                vim.lsp.buf.format({ async = false })
            end,
        })
    end,
    filetypes = { "c", "cpp", "objc", "objcpp", "h" },
    root_dir = lspconfig.util.root_pattern("compile_commands.json", "compile_flags.txt", ".git"),
    capabilities = require("cmp_nvim_lsp").default_capabilities(),
})
