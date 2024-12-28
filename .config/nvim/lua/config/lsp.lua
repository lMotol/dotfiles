-- ~/.config/nvim/lua/config/lsp.lua
local lspconfig = require("lspconfig")
local mason_lspconfig = require("mason-lspconfig")

-- mason-lspconfig と lspconfig を使って、LSP をセットアップ
mason_lspconfig.setup_handlers({
    function(server_name)
        lspconfig[server_name].setup({
            on_attach = function(client, bufnr)
                -- LSP サーバーがアタッチされた時の処理
                print("LSP server attached")
            end,
            capabilities = require("cmp_nvim_lsp").update_capabilities(vim.lsp.protocol.make_client_capabilities()),
        })
    end,
})

-- ast-grep LSP サーバーを設定
lspconfig.ast_grep.setup({
    cmd = { "ast-grep", "lsp" },
    filetypes = { -- 対応するファイルタイプ
        "c",
        "cpp",
        "rust",
        "go",
        "java",
        "python",
        "javascript",
        "typescript",
        "html",
        "css",
        "kotlin",
        "dart",
        "lua",
    },
    root_dir = lspconfig.util.root_pattern("sgconfig.yaml", "sgconfig.yml"), -- プロジェクトのルートディレクトリを自動判別
    on_attach = function(client, bufnr)
        -- ファイル保存時に自動でフォーマットを実行
        vim.api.nvim_buf_set_option(bufnr, "formatexpr", "v:lua.vim.lsp.formatexpr()")
    end,
})
