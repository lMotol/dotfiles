-- ~/.config/nvim/lua/plugins/overrides/fzf-lua.lua
return {
    "ibhagwan/fzf-lua",
    opts = {
        winopts = {
            height = 0.6,
            width = 0.8,
        },
        files = {
            -- デフォルトで隠しファイルを含めないなら true に
            hidden = true,
            -- カレントファイルのあるディレクトリを初期 cwd にする
            cwd_only = false,
            fd_opts = "--type f --hidden --exclude .git",
        },
        grep = {
            -- 検索時に隠しファイルを含める
            rg_opts = "--column --line-number --no-heading --hidden --smart-case",
            -- 必要なら改めて search_paths も指定可
            -- search_paths = { "~/my/project" },
        },
    },
}
