-- ==========================================================
-- Firefox popup-only hotkeys (focus not required)
-- MOD+Enter toggles maximize <-> restore previous frame
-- ==========================================================

local MOD = { "ctrl", "cmd" }

local STEP = 80
local MIN_W, MIN_H = 240, 180
local MARGIN = 0

-- Used only for initial popup detection (before we "remember" it)
local MAX_POPUP_W = 1200
local MAX_POPUP_H = 900

-- Optional title filter to improve precision (set "" to disable)
local TITLE_MUST_CONTAIN = ""

-- Remember last chosen popup window id
local lastPopupId = nil

-- Store "restore frame" per window id
-- restoreFrames[winId] = hs.geometry.rect(x,y,w,h)
local restoreFrames = {}

-- ----------------------------------------------------------
-- Utilities
-- ----------------------------------------------------------
local function clamp(v, lo, hi)
	if v < lo then
		return lo
	end
	if v > hi then
		return hi
	end
	return v
end

local function windowStillValidAsFirefox(w)
	if not w then
		return false
	end
	if not w:isVisible() then
		return false
	end
	if not w:isStandard() then
		return false
	end
	local app = w:application()
	if not app or app:name() ~= "Firefox" then
		return false
	end
	return true
end

-- "Nearly equals" for frames (tolerance in pixels)
local function framesNearlyEqual(a, b, tol)
	tol = tol or 2
	return math.abs(a.x - b.x) <= tol
		and math.abs(a.y - b.y) <= tol
		and math.abs(a.w - b.w) <= tol
		and math.abs(a.h - b.h) <= tol
end

-- Pick Firefox popup window without requiring focus.
-- First: return remembered window (even if large).
-- Fallback: detect by size/title and remember it.
local function pickFirefoxPopupWindow()
	if lastPopupId then
		local w = hs.window.get(lastPopupId)
		if windowStillValidAsFirefox(w) then
			return w, nil
		end
		lastPopupId = nil
	end

	local app = hs.application.get("Firefox")
	if not app then
		return nil, "Firefox not running"
	end

	local wins = app:allWindows() or {}
	local candidates = {}

	for _, w in ipairs(wins) do
		if w:isVisible() and w:isStandard() then
			local f = w:frame()
			local title = w:title() or ""

			if TITLE_MUST_CONTAIN ~= "" and not string.find(title, TITLE_MUST_CONTAIN) then
			-- skip
			else
				if f.w <= MAX_POPUP_W and f.h <= MAX_POPUP_H then
					table.insert(candidates, w)
				end
			end
		end
	end

	if #candidates == 0 then
		return nil, "No popup candidates (tune MAX_POPUP_* or TITLE_MUST_CONTAIN)"
	end

	table.sort(candidates, function(a, b)
		local fa, fb = a:frame(), b:frame()
		return (fa.w * fa.h) < (fb.w * fb.h)
	end)

	local chosen = candidates[1]
	lastPopupId = chosen:id()
	return chosen, nil
end

local function popupWindowOrAlert()
	local w, err = pickFirefoxPopupWindow()
	if not w then
		hs.alert.show("Firefox popup not found: " .. err)
		return nil
	end
	return w
end

-- ----------------------------------------------------------
-- Actions (operate on Firefox popup only)
-- ----------------------------------------------------------

-- Toggle maximize: maximize <-> restore previous frame
local function toggleMaximizePopup()
	local win = popupWindowOrAlert()
	if not win then
		return
	end

	local id = win:id()
	lastPopupId = id

	local sf = win:screen():frame()
	local f = win:frame()

	local isMaximized = framesNearlyEqual(f, sf, 300)

	if isMaximized then
		-- Restore
		local rf = restoreFrames[id]
		if rf then
			win:setFrame(rf)
		else
			-- If we don't have a saved frame, do a reasonable fallback (centered, ~60%)
			win:moveToUnit(hs.geometry.rect(0.2, 0.2, 0.6, 0.6))
		end
	else
		-- Save current frame, then maximize
		restoreFrames[id] = f
		win:maximize()
	end
end

-- corner: "tl" | "tr" | "bl" | "br"
local function movePopupToCorner(corner)
	local win = popupWindowOrAlert()
	if not win then
		return
	end
	lastPopupId = win:id()

	local sf = win:screen():frame()
	local f = win:frame()

	local x, y = f.x, f.y
	if corner == "tl" then
		x = sf.x + MARGIN
		y = sf.y + MARGIN
	elseif corner == "tr" then
		x = sf.x + sf.w - f.w - MARGIN
		y = sf.y + MARGIN
	elseif corner == "bl" then
		x = sf.x + MARGIN
		y = sf.y + sf.h - f.h - MARGIN
	elseif corner == "br" then
		x = sf.x + sf.w - f.w - MARGIN
		y = sf.y + sf.h - f.h - MARGIN
	end

	x = clamp(x, sf.x + MARGIN, sf.x + sf.w - f.w - MARGIN)
	y = clamp(y, sf.y + MARGIN, sf.y + sf.h - f.h - MARGIN)

	win:setFrame({ x = x, y = y, w = f.w, h = f.h })
end

-- Resize around center while keeping within screen
local function resizePopupCentered(dw, dh)
	local win = popupWindowOrAlert()
	if not win then
		return
	end
	lastPopupId = win:id()

	local sf = win:screen():frame()
	local f = win:frame()

	local newW = clamp(f.w + dw, MIN_W, sf.w - 2 * MARGIN)
	local newH = clamp(f.h + dh, MIN_H, sf.h - 2 * MARGIN)

	local cx = f.x + f.w / 2
	local cy = f.y + f.h / 2

	local x = clamp(cx - newW / 2, sf.x + MARGIN, sf.x + sf.w - newW - MARGIN)
	local y = clamp(cy - newH / 2, sf.y + MARGIN, sf.y + sf.h - newH - MARGIN)

	win:setFrame({ x = x, y = y, w = newW, h = newH })
end

-- ----------------------------------------------------------
-- Key bindings (Firefox popup only)
-- ----------------------------------------------------------

-- Toggle maximize <-> restore
hs.hotkey.bind(MOD, "Return", toggleMaximizePopup)

-- Move to corners (keep size)
hs.hotkey.bind(MOD, "U", function()
	movePopupToCorner("tl")
end) -- Top Left
hs.hotkey.bind(MOD, "I", function()
	movePopupToCorner("tr")
end) -- Top Right
hs.hotkey.bind(MOD, "J", function()
	movePopupToCorner("bl")
end) -- Bottom Left
hs.hotkey.bind(MOD, "K", function()
	movePopupToCorner("br")
end) -- Bottom Right

-- Resize (grow/shrink)
hs.hotkey.bind(MOD, "=", function()
	resizePopupCentered(STEP, STEP)
end)
hs.hotkey.bind(MOD, "-", function()
	resizePopupCentered(-STEP, -STEP)
end)

-- Reload config
hs.hotkey.bind(MOD, "R", function()
	hs.reload()
end)

hs.alert.show("Firefox popup-only hotkeys loaded")
