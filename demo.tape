# VHS Script for py2mcp
# To record the GIF, run: vhs < demo.tape

Output demo.gif

Set FontSize 20
Set Width 1200
Set Height 700
Set FontFamily "JetBrains Mono"
Set Theme "Catppuccin Mocha"
Set WindowBar Colorful

Type "cat test_tools.py"
Enter
Sleep 3s

Type "py2mcp test_tools.py"
Enter
Sleep 4s

Ctrl+C
Sleep 1s

Type "# Now your tools are available in Claude Desktop! 🚀"
Enter
Sleep 3s
