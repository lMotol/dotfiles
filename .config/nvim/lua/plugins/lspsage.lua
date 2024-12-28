-- every spec file under the "plugins" directory will be loaded automatically by lazy.nvim
--
-- In your plugin files, you can:
-- * add extra plugins
-- * disable/enabled LazyVim plugins
-- * override the configuration of LazyVim plugins
return {
    "nvimdev/lspsaga.nvim",
    dependencies = { "nvim-treesitter/nvim-treesitter", "nvim-tree/nvim-web-devicons" }, -- 必要な依存関係
    event = "LspAttach", -- LSP がアタッチされたときにロード
    config = function()
        require("lspsaga").setup({
            -- 以下に lspsaga の設定を記述
            ui = {
                theme = "round", -- UIテーマを設定
                border = "single",
            },
            code_action = {
                show_server_name = true,
                extend_gitsigns = true,
            },
            lightbulb = {
                enable = true,
                enable_in_insert = false,
                sign = true,
                sign_priority = 20,
                virtual_text = true,
            },
        })
    end,
}
