start "" /b cmd /c "hack.exe <input.in.txt >output.out.txt"
timeout /t 2 2>nul
tasklist | find "hack.exe" 2>nul && taskkill /f /im hack.exe