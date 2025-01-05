-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.wrap = true

-- 言語によって indent を変更する
local filetype_tabstop = { typescriptreact = 2, typescript = 2 } -- filetype毎のインデント幅
local usrftcfg = vim.api.nvim_create_augroup("UserFileTypeConfig", { clear = true })
vim.api.nvim_create_autocmd("FileType", {
    group = usrftcfg,
    callback = function(args)
        local ftts = filetype_tabstop[args.match]
        if ftts then
            vim.bo.tabstop = ftts
            vim.bo.shiftwidth = ftts
        end
    end,
})

if os.getenv("TMUX") then
    vim.opt.termguicolors = true
end
