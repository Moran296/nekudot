local wezterm = require 'wezterm'
local config = wezterm.config_builder()

config.default_prog = { '/usr/bin/zsh' }

wezterm.on('window-resized', function(window, pane)
	local overrides = window:get_config_overrides() or {}
	local window_width = window:get_dimensions().pixel_width
	local window_height = window:get_dimensions().pixel_height
	if window_width > window_height then
		-- landscape
		overrides.window_background_image = './nekudot/wallpapers/tuhua_wide.jpg'
	else
		-- portrait
		overrides.window_background_image = './nekudot/wallpapers/tuhua_long.jpg'
	end

  window:set_config_overrides(overrides)
  end)

 config.window_background_image_hsb = {
   brightness = 0.025,
   hue = 1.0,
   saturation = 0.6,
}



-- schemes: https://wezfurlong.org/wezterm/colorschemes/index.html
config.color_scheme = 'Catppuccin Frappe'
config.font_size = 12.5  -- Adjust font size for better readability



return config
