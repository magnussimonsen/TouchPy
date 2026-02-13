# TouchPy 🎯

A beautiful terminal-based touch typing trainer built with Python, Textual, and Rich.

## Features

- 🎨 **Beautiful Terminal UI** - Modern, colorful interface using Textual
- ⚡ **Real-time Feedback** - See your typing speed (WPM) and accuracy live
- 🎯 **Visual Highlighting** - Correct characters in green, mistakes in red
- 📚 **Multiple Exercises** - 7 built-in exercises covering home row, top row, bottom row, and more
- ⏱️ **Automatic Timer** - Timer starts when you begin typing
- 📊 **Performance Summary** - Get detailed stats after each exercise
- ✏️ **Backspace Support** - Fix mistakes as you type

## Installation

1. **Clone the repository** (if you haven't already):

   ```bash
   git clone https://github.com/magnussimonsen/TouchPy.git
   cd TouchPy
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the typing trainer:

```bash
python run.py
```

Or run directly from the typing_trainer directory:

```bash
cd typing_trainer
python app.py
```

## How to Use

1. **Select an Exercise** - Use arrow keys to navigate the menu, press Enter to select
2. **Start Typing** - The timer starts automatically when you type the first character
3. **Watch Your Progress** - See real-time WPM and accuracy as you type
4. **Complete the Exercise** - Type the entire text correctly to finish
5. **Review Your Results** - Get a summary with your speed, accuracy, and time

### Keyboard Shortcuts

- **Arrow Keys** - Navigate menu
- **Enter** - Select exercise or return to menu
- **Escape** - Return to menu from typing view
- **Q** - Quit from main menu
- **Backspace** - Correct mistakes while typing

## Project Structure

```
TouchPy/
├── typing_trainer/
│   ├── app.py                 # Main application
│   ├── models.py              # Exercise data model
│   ├── services/
│   │   ├── loader.py          # Exercise file loader
│   │   └── metrics.py         # WPM and accuracy calculations
│   ├── views/
│   │   ├── menu_view.py       # Exercise selection screen
│   │   ├── typing_view.py     # Main typing practice screen
│   │   └── summary_view.py    # Results screen
│   └── exercises/
│       ├── 001_home_row.txt
│       ├── 002_home_row_words.txt
│       ├── 003_top_row.txt
│       ├── 004_bottom_row.txt
│       ├── 005_pangrams.txt
│       ├── 006_numbers_symbols.txt
│       └── 007_code_practice.txt
├── requirements.txt
├── run.py
└── README.md
```

## Creating Custom Exercises

You can easily add your own exercises! Just create a `.txt` file in the `typing_trainer/exercises/` directory:

1. **First line**: Exercise title
2. **Remaining lines**: The text to type

Example (`exercises/008_my_exercise.txt`):

```
My Custom Exercise
This is the text that users will practice typing.
It can span multiple lines.
```

The exercises will automatically appear in the menu, sorted by filename.

## Built-in Exercises

1. **Home Row Basics** - Practice the home row keys (asdf jkl;)
2. **Home Row Words** - Simple words using only home row
3. **Top Row Practice** - Practice the top row keys (qwerty uiop)
4. **Bottom Row Practice** - Practice the bottom row keys (zxcvbnm)
5. **Common Words Practice** - Famous pangrams like "the quick brown fox"
6. **Numbers and Symbols** - Practice numbers and special characters
7. **Programming Practice** - Python code snippets

## Technology Stack

- **[Textual](https://github.com/Textualize/textual)** - Terminal UI framework
- **[Rich](https://github.com/Textualize/rich)** - Beautiful text formatting
- **Python 3.8+**

## Requirements

- Python 3.8 or higher
- textual >= 0.50.0
- rich >= 13.7.0

## Contributing

Feel free to contribute by:

- Adding new exercises
- Improving the UI
- Fixing bugs
- Adding new features

## License

MIT License - feel free to use this project for learning and teaching!

## Tips for Better Touch Typing

1. 🪑 **Proper Posture** - Sit up straight with feet flat on the floor
2. 👀 **Look at the Screen** - Not at your keyboard!
3. 🏠 **Home Row Position** - Keep fingers on asdf and jkl;
4. 🎯 **Accuracy First** - Speed will come naturally with practice
5. 📅 **Practice Daily** - Even 15 minutes a day makes a difference
6. 🔄 **Repeat Exercises** - Muscle memory improves with repetition

Happy typing! 🚀
