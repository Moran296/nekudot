function Linemode:size_and_mtime()
	local time = math.floor(self._file.cha.modified or 0)
	if time == 0 then
		time = ""
	elseif os.date("%Y", time) == os.date("%Y") then
		time = os.date("%b %d %H:%M", time)
	else
		time = os.date("%b %d  %Y", time)
	end

	local size = self._file:size()
	if size then
		return ui.Line(string.format("%s %s", ya.readable_size(size), time))
	else
		local folder = cx.active:history(self._file.url)
		local file_count = folder and tostring(#folder.files) or "0"
		return ui.Line(string.format("%s %s", file_count, time))
	end
end
