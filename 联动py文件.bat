@echo off
echo 正在运行 get_wxapkg.py...
python get_wxapkg.py

echo.
echo get_wxapkg.py 运行完毕，正在运行 killwxapkg.py...
python killwxapkg.py

echo.
echo 全部运行完成！
pause