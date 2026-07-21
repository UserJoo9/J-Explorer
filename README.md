# JExplorer

A modern file explorer for Windows built with Python and CustomTkinter, featuring a clean GUI with disk navigation, file/folder operations, and responsive design.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.x-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

## Features

- **Disk Navigation** - Browse all connected drives (C:, D:, etc.)
- **File/Folder Operations** - Create, copy, paste, rename, and delete files and folders
- **Responsive Design** - Automatically adapts to window resizing
- **Modern GUI** - Clean interface using CustomTkinter with custom icons
- **Keyboard Shortcuts** - Quick access to common operations
- **Path Bar** - Direct navigation by typing paths

## Screenshots

> Add screenshots here

## Installation

### Prerequisites

- Python 3.x
- Windows OS

### Dependencies

```bash
pip install customtkinter Pillow CTkToolTip CTkMessagebox pywin32
```

Or install all at once:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python JExplorer.py
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Alt + Left` | Navigate back |
| `Alt + Right` | Navigate forward |
| `Delete` | Delete selected item |
| `F2` | Rename selected item |
| `Ctrl + C` | Copy selected item |
| `Ctrl + V` | Paste copied item |

## Project Structure

```
JExplorer/
├── JExplorer.py      # Main application file
├── icons/            # UI icons
│   ├── new.png
│   ├── delete.png
│   ├── rename.png
│   ├── copy.png
│   ├── paste.png
│   ├── open-folder.png
│   ├── file.png
│   ├── harddisk.png
│   ├── left.png
│   ├── right.png
│   └── home.png
└── README.md
```

## How It Works

JExplorer is a single-class application that provides:

1. **Home Screen** - Displays all connected drives with disk icons
2. **Folder Navigation** - Double-click folders to open, use back/forward buttons for navigation
3. **File Operations** - Right-click or use toolbar buttons for copy, paste, rename, delete
4. **Path Bar** - Type a path directly and press Enter to navigate

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern looking Tkinter widgets
- [CTkToolTip](https://github.com/Clue-J/CTkToolTip) - Tooltips for CustomTkinter
- [CTkMessagebox](https://github.com/ajitkanekar/CTkMessagebox) - Message boxes for CustomTkinter
