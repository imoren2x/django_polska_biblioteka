
@echo off
for /l %%i in (2,1,255) do (
  ping -n 1 -w 50 192.168.43.%%i

  timeout 5
)

