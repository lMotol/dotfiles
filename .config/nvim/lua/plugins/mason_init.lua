-- ~/.config/nvim/lua/plugins/init.lua
return {
    -- add pyright to lspconfig
    {
        "neovim/nvim-lspconfig",
        ---@class PluginLspOpts
        opts = {
            ---@type lspconfig.options
            servers = {
                -- pyright will be automatically installed with mason and loaded with lspconfig
                pyright = {},
                ast_grep = {},
                clangd = {},
            },
        },
    },

    -- Mason と関連ツールのインストール
    {
        "williamboman/mason.nvim",
        opts = {
            ensure_installed = {
                "stylua",
                "shellcheck",
                "shfmt",
                "flake8",
            },
        },
    },
    {
        "williamboman/mason-lspconfig.nvim",
        config = function()
            require("mason-lspconfig").setup({
                ensure_installed = { "sumneko_lua", "pyright", "tsserver", "ast_grep", "clangd" }, -- 使用するLSPを指定
                automatic_installation = true, -- 起動時に自動でインストール
            })
        end,
    },
}
