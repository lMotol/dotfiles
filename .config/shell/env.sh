export EDITOR="${EDITOR:-nvim}"
export VISUAL="${VISUAL:-$EDITOR}"
export GIT_EDITOR="${GIT_EDITOR:-$EDITOR}"
export FCEDIT="${FCEDIT:-$EDITOR}"
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"

if command -v brew >/dev/null 2>&1; then
    ctags_prefix="$(brew --prefix universal-ctags 2>/dev/null || true)"
    ctags_bin="$ctags_prefix/bin"
    if [ -n "$ctags_prefix" ] && [ -d "$ctags_bin" ]; then
        case ":$PATH:" in
            *":$ctags_bin:"*)
                ;;
            *)
                export PATH="$ctags_bin:$PATH"
                ;;
        esac
    fi
fi
