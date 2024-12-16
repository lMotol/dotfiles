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
