-- every spec file under the "plugins" directory will be loaded automatically by lazy.nvim
--
-- In your plugin files, you can:
-- * add extra plugins
-- * disable/enabled LazyVim plugins
-- * override the configuration of LazyVim plugins
return {
    {
        "folke/tokyonight.nvim",
        opts = {
            on_colors = function(colors)
                colors.hint = colors.orange
                colors.comment = "#CD853F"
            end,
            style = "storm",
            transparent = true,
            styles = {
                sidebars = "transparent",
                floats = "transparent",
            },
        },
    },
}
