return {
    {
        "ludovicchabant/vim-gutentags",
        event = { "BufReadPre", "BufNewFile" },
        config = function()
            local cache_dir = vim.fn.stdpath("cache") .. "/tags"
            if vim.fn.isdirectory(cache_dir) == 0 then
                vim.fn.mkdir(cache_dir, "p")
            end
            vim.g.gutentags_cache_dir = cache_dir
            vim.g.gutentags_project_root = { ".git", ".hg", ".bzr", ".svn", "Makefile", "package.json" }
            vim.g.gutentags_generate_on_write = 1
        end,
    },
}
