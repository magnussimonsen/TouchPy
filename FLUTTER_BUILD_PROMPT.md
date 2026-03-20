# AI Prompt: Build a Touch Typing Trainer in Flutter

## Project Overview
Build a cross-platform touch typing trainer application in Flutter with a desktop-focused UI featuring a traditional menu bar, practice modes with real-time feedback, keyboard visualization, and comprehensive exercise management.

## Core Technology Stack
- **Framework**: Flutter (Desktop - Windows/macOS/Linux)
- **State Management**: Provider or Riverpod
- **Local Storage**: sqflite or Hive for exercise data and statistics
- **File Handling**: path_provider for file system access
- **UI**: Material Design with custom desktop widgets

---

## Data Models

### Exercise Model
```dart
class Exercise {
  final String id;              // Unique identifier (UUID or filename-based)
  final String title;           // Display title
  final String text;            // Content to type
  final String language;        // "English" or "Norwegian"
  final bool isBuiltIn;         // True for default exercises, false for custom
  final DateTime createdAt;
  final DateTime? modifiedAt;
  
  int get wordCount => text.split(RegExp(r'\s+')).length;
}
```

### TypingSession Model
```dart
class TypingSession {
  final String exerciseId;
  final DateTime startTime;
  DateTime? endTime;
  
  int totalCharactersTyped;
  int correctCharacters;
  int mistakes;
  Map<String, int> characterMistakes;  // Track errors per character
  List<String> completedWords;
  String currentWord;
  
  double get wpm => _calculateWPM();
  double get accuracy => (correctCharacters / totalCharactersTyped) * 100;
  double get elapsedSeconds => 
    (endTime ?? DateTime.now()).difference(startTime).inSeconds.toDouble();
}
```

### CharacterStatus Model
```dart
enum CharacterStatus {
  pending,   // Not yet typed
  correct,   // Typed correctly
  incorrect, // Typed incorrectly
  nextChar   // The next character to type (highlighted)
}
```

---

## UI Structure

### Main Window Layout

```
┌────────────────────────────────────────────────────┐
│ File    Edit    Language    Practice Mode    Help  │  ← Menu Bar
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │                                              │ │
│  │  TARGET TEXT DISPLAY                         │ │  ← Top Window
│  │  (Exercise words with color highlighting)    │ │     (Target Text)
│  │                                              │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │                                              │ │
│  │  INPUT FIELD                                 │ │  ← Middle Window
│  │  (User's typed text)                         │ │     (Input Field)
│  │                                              │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │                                              │ │
│  │  KEYBOARD FINGER MAP                         │ │  ← Bottom Window
│  │  (Visual keyboard with finger positions)     │ │     (Finger Map)
│  │  - Next key highlighted in blue              │ │
│  │  - Error keys highlighted in red             │ │
│  │                                              │ │
│  └──────────────────────────────────────────────┘ │
│                                                    │
├────────────────────────────────────────────────────┤
│ Status: [WPM: 0] [Accuracy: 100%] [Mistakes: 0]   │  ← Status Bar
└────────────────────────────────────────────────────┘
```

---

## Menu Bar Implementation

### File Menu
- **Open Exercise** → Shows dialog to select from available exercises
- **New Exercise** → Opens dialog to create new custom exercise
  - Fields: Title, Language (dropdown), Text (multiline)
- **Help** → Opens help documentation window
- **About** → Shows app information and credits
- **Quit** → Exits the application

### Edit Menu
- **Edit Exercise** → Opens edit dialog for selected exercise
- **Delete Exercise** → Confirms and deletes selected exercise (including built-in)
- **Restore Example Exercises** → Restores all default exercises that ship with app

### Language Menu
- **English** → Sets keyboard layout to English and shows English finger map
- **Norwegian** → Sets keyboard layout to Norwegian (æ, ø, å) and shows Norwegian finger map

### Practice Mode Menu
- **Review Mode** → Linear progression through exercise words
- **Weighted Repetition Mode** → Random selection with higher probability for mistake-prone words

---

## Core Features Implementation

### 1. **Target Text Display (Top Window)**

**Requirements:**
- Display words from current exercise
- Real-time color coding:
  - **Green**: Correctly typed characters
  - **Red**: Incorrectly typed characters
  - **Blue background**: Next character to type
  - **Gray/Dim**: Pending characters not yet reached
- Scroll or paginate for long exercises
- Font: Monospace, large and readable (16-18pt)

**Implementation Notes:**
- Use `RichText` with `TextSpan` for character-by-character styling
- Update highlighting on every keystroke
- Compare typed input against target text character-by-character

### 2. **Input Field (Middle Window)**

**Requirements:**
- Single-line or multi-line text input
- Shows what user has typed
- Cursor always visible
- Supports backspace to correct mistakes
- Focus management - auto-focus on exercise start

**Implementation Notes:**
- Use `TextField` with `TextEditingController`
- Listen to `onChanged` events
- Track cursor position
- Clear field between words if in word-by-word mode

### 3. **Finger Map Display (Bottom Window)**

**Requirements:**
- Visual ASCII/Unicode keyboard layout
- Color-coded by finger assignment:
  - **Magenta**: Pinky fingers
  - **Yellow**: Ring fingers  
  - **Cyan**: Middle fingers
  - **Green**: Index fingers
- Real-time highlighting:
  - **Blue background**: Next character to press
  - **Red background**: Top 3 most-mistaken characters
- Switch between English and Norwegian layouts
- Show hand position guide below keyboard

**English Keyboard Layout:**
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────────┐
│  `  │  1  │  2  │  3  │  4  │  5  │  6  │  7  │  8  │  9  │  0  │  -  │  =  │  BKSP   │
├─────┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──────┤
│  TAB   │  Q  │  W  │  E  │  R  │  T  │  Y  │  U  │  I  │  O  │  P  │  [  │  ]  │   \  │
├────────┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴──────┤
│   CAPS   │  A  │  S  │  D  │  F  │  G  │  H  │  J  │  K  │  L  │  ;  │  '  │  ENTER   │
├──────────┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──────────┤
│    SHIFT    │  Z  │  X  │  C  │  V  │  B  │  N  │  M  │  ,  │  .  │  /  │    SHIFT    │
└─────────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────────────┘
                                    SPACE BAR
```

**Norwegian Keyboard Layout:**
```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────────┐
│  |  │  1  │  2  │  3  │  4  │  5  │  6  │  7  │  8  │  9  │  0  │  +  │  \  │  BKSP   │
├─────┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──────┤
│  TAB   │  Q  │  W  │  E  │  R  │  T  │  Y  │  U  │  I  │  O  │  P  │  Å  │  ¨  │   '  │
├────────┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴─┬───┴──────┤
│   CAPS   │  A  │  S  │  D  │  F  │  G  │  H  │  J  │  K  │  L  │  Ø  │  Æ  │  ENTER   │
├──────────┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──────────┤
│    SHIFT    │  Z  │  X  │  C  │  V  │  B  │  N  │  M  │  ,  │  .  │  -  │    SHIFT    │
└─────────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────────────┘
                              MELLOMROMSTAST (SPACE BAR)
```

**Finger Color Assignment:**
- **Left Pinky**: `, 1, Q, A, Z, Shift (left)
- **Left Ring**: 2, W, S, X
- **Left Middle**: 3, E, D, C  
- **Left Index**: 4, 5, R, T, F, G, V, B
- **Right Index**: 6, 7, Y, U, H, J, N, M
- **Right Middle**: 8, I, K, comma
- **Right Ring**: 9, O, L, period
- **Right Pinky**: 0, -, =, P, [, ], ;, ', /, Shift (right), Backspace

### 4. **Metrics Calculator**

**WPM Calculation:**
```dart
double calculateWPM(int charactersTyped, double elapsedSeconds) {
  if (elapsedSeconds <= 0) return 0.0;
  
  // Standard: 1 word = 5 characters
  double words = charactersTyped / 5.0;
  double minutes = elapsedSeconds / 60.0;
  
  return words / minutes;
}
```

**Accuracy Calculation:**
```dart
double calculateAccuracy(String target, String typed) {
  if (target.isEmpty) return 100.0;
  if (typed.isEmpty) return 0.0;
  
  int correctChars = 0;
  int comparisonLength = min(target.length, typed.length);
  
  for (int i = 0; i < comparisonLength; i++) {
    if (target[i] == typed[i]) correctChars++;
  }
  
  // Penalize for length differences
  int totalLength = max(target.length, typed.length);
  double accuracy = (correctChars / totalLength) * 100.0;
  
  return accuracy;
}
```

**Character Status Check:**
```dart
CharacterStatus getCharacterStatus(String target, String typed, int position) {
  if (position >= typed.length) {
    return position == typed.length 
      ? CharacterStatus.nextChar 
      : CharacterStatus.pending;
  }
  
  if (position >= target.length) {
    return CharacterStatus.incorrect; // Extra characters
  }
  
  return target[position] == typed[position]
    ? CharacterStatus.correct
    : CharacterStatus.incorrect;
}
```

### 5. **Practice Modes**

#### Review Mode
- Present words/text linearly from start to finish
- User types each word or section in order
- Move to next word after correct completion or user presses space/enter

#### Weighted Repetition Mode  
- Randomly select words from exercise
- Maintain error count per word during session
- Weight selection probability:
  ```dart
  // Higher mistake count = higher probability
  double getWordWeight(String word, Map<String, int> wordMistakes) {
    int mistakes = wordMistakes[word] ?? 0;
    return 1.0 + (mistakes * 0.5); // Base weight 1.0, +0.5 per mistake
  }
  ```
- Use weighted random selection algorithm
- Words with more mistakes appear more frequently

### 6. **Error Tracking (Per Session)**

**Track per-character mistakes:**
```dart
Map<String, int> characterMistakes = {};

void recordMistake(String expectedChar, String typedChar) {
  // Increment mistake count for the expected character
  characterMistakes[expectedChar] = 
    (characterMistakes[expectedChar] ?? 0) + 1;
}

List<MapEntry<String, int>> getTopMistakes({int count = 3}) {
  var entries = characterMistakes.entries.toList()
    ..sort((a, b) => b.value.compareTo(a.value));
  return entries.take(count).toList();
}
```

**Display in finger map:**
- Highlight top 3 most-mistaken characters in red
- Update in real-time as user types

---

## Exercise Management

### File Format
Store exercises as JSON files or SQLite database entries:

```json
{
  "id": "uuid-or-filename",
  "title": "Home Row Practice",
  "language": "English",
  "text": "asdf jkl; asdf jkl; sad lad fad...",
  "isBuiltIn": true,
  "createdAt": "2026-03-20T10:00:00Z",
  "modifiedAt": null
}
```

### Built-in Exercises
Ship with the app (embedded as assets):
1. Home Row Basics - `asdf jkl;` repetition
2. Home Row Words - Common words using home row
3. Top Row Practice - `qwert yuiop`
4. Bottom Row Practice - `zxcvb nm,./`
5. Pangrams - "The quick brown fox..."
6. Code Practice - Programming symbols and syntax
7. 1000 Common English Words - High-frequency vocabulary
8. Norwegian Letters - Practice æ, ø, å
9. Norwegian Cities - Oslo, Bergen, Trondheim, etc.
10. Literary excerpts (if desired)

### CRUD Operations

**Create Exercise:**
- Dialog with: Title (text field), Language (dropdown), Text (multiline)
- Validate: Non-empty title and text
- Generate UUID for ID
- Save to local storage
- Refresh exercise list

**Read/Load Exercises:**
- On app start, load all exercises from storage
- Merge built-in exercises with custom exercises
- Display in exercise selection dialog

**Update Exercise:**
- Fetch exercise by ID
- Pre-populate dialog with existing values
- Allow editing all fields except ID and isBuiltIn
- Save changes and refresh

**Delete Exercise:**
- Confirmation dialog
- Allow deletion of both custom and built-in exercises
- Remove from local storage

**Restore Built-in Exercises:**
- Re-copy all built-in exercises from assets
- Overwrite any deleted built-in exercises
- Keep custom exercises intact

---

## User Interface Flow

### 1. Application Launch
- Show main window with menu bar and empty content area
- Status bar shows: "No exercise selected"
- All practice areas are blank/hidden

### 2. Select Exercise (File → Open Exercise)
- Show dialog listing all available exercises
- Sort by: Built-in first, then custom (alphabetically)
- Display: Title, Language, Word Count
- User selects and clicks "Open"

### 3. Start Practice Session
- Timer starts on first keystroke
- Target text appears in top window
- First character highlighted in blue
- Input field focused and ready
- Finger map shows next key highlighted

### 4. During Typing
- Real-time character comparison
- Color updates on every keystroke:
  - Green for correct
  - Red for incorrect
  - Blue for next char
- WPM and accuracy update every 100ms
- Mistake tracking updates character map
- Finger map highlights:
  - Next character in blue
  - Top 3 mistake chars in red

### 5. Complete Exercise
- Show summary dialog:
  - Exercise title
  - Final WPM
  - Accuracy percentage
  - Total mistakes
  - Elapsed time
  - Top 5 most-mistaken characters
- Options: "Retry", "New Exercise", "Main Menu"

### 6. Empty State (No Exercise)
- Top, middle, bottom windows are visible but empty/grayed out
- Status bar: "Select an exercise from File → Open Exercise to begin"
- Menu bar remains functional

---

## Technical Implementation Details

### State Management Structure

**AppState (Global):**
```dart
class AppState extends ChangeNotifier {
  List<Exercise> exercises = [];
  Exercise? currentExercise;
  String currentLanguage = "English";
  PracticeMode practiceMode = PracticeMode.review;
  
  Future<void> loadExercises();
  Future<void> createExercise(Exercise exercise);
  Future<void> updateExercise(Exercise exercise);
  Future<void> deleteExercise(String id);
  Future<void> restoreBuiltInExercises();
  void setCurrentExercise(Exercise? exercise);
  void setLanguage(String language);
  void setPracticeMode(PracticeMode mode);
}
```

**TypingState (Session):**
```dart
class TypingState extends ChangeNotifier {
  TypingSession? session;
  String targetText = "";
  String typedText = "";
  bool isTimerRunning = false;
  
  void startSession(Exercise exercise);
  void onKeyPress(String key);
  void onBackspace();
  void completeSession();
  void resetSession();
  
  // Computed properties
  double get wpm;
  double get accuracy;
  int get mistakes;
  Map<String, int> get characterMistakes;
  String? get nextCharacter;
  List<String> get top3MistakeChars;
}
```

### File Storage Structure

**Using sqflite (recommended for desktop):**
```sql
CREATE TABLE exercises (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  language TEXT NOT NULL,
  text TEXT NOT NULL,
  is_built_in INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  modified_at TEXT
);
```

**Or using Hive (NoSQL):**
```dart
@HiveType(typeId: 0)
class ExerciseEntity extends HiveObject {
  @HiveField(0)
  String id;
  
  @HiveField(1)  
  String title;
  
  @HiveField(2)
  String language;
  
  @HiveField(3)
  String text;
  
  @HiveField(4)
  bool isBuiltIn;
  
  @HiveField(5)
  DateTime createdAt;
  
  @HiveField(6)
  DateTime? modifiedAt;
}
```

### Key Widget Structure

```dart
// Main Application Window
class TouchTypingApp extends StatelessWidget {
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Column(
          children: [
            CustomMenuBar(),           // Top menu
            Expanded(
              child: MainContent(),    // Three-panel layout
            ),
            StatusBar(),               // Bottom status
          ],
        ),
      ),
    );
  }
}

// Main Content Area
class MainContent extends StatelessWidget {
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(
          flex: 3,
          child: TargetTextDisplay(),  // Top window
        ),
        Expanded(
          flex: 2,
          child: InputField(),          // Middle window
        ),
        Expanded(
          flex: 4,
          child: FingerMapDisplay(),    // Bottom window
        ),
      ],
    );
  }
}
```

---

## Priority Features Checklist

**Phase 1 - Core Functionality:**
- ✅ Desktop window with menu bar
- ✅ Three-panel layout (target, input, finger map)
- ✅ Exercise loading and display
- ✅ Real-time character comparison and coloring
- ✅ WPM and accuracy calculation
- ✅ Basic input handling with backspace support

**Phase 2 - Exercise Management:**
- ✅ Create custom exercises
- ✅ Edit exercises
- ✅ Delete exercises
- ✅ Restore built-in exercises
- ✅ Language selection (English/Norwegian)
- ✅ Local storage persistence

**Phase 3 - Advanced Features:**
- ✅ Finger map visualization with color coding
- ✅ Next character highlighting (blue)
- ✅ Error tracking per character
- ✅ Top 3 mistakes highlighting (red)
- ✅ Practice modes (Review / Weighted Repetition)
- ✅ Summary screen after completion

**Phase 4 - Polish:**
- ✅ Responsive layout for different screen sizes
- ✅ Keyboard shortcuts for menu items
- ✅ Help documentation
- ✅ About dialog
- ✅ Smooth animations and transitions
- ✅ Error handling and user feedback

---

## Design Insights from TouchPy (Python/Textual Version)

### Architecture Patterns Used:
1. **MVC-like separation**: Models (`Exercise`), Views (UI screens), Services (metrics, loader)
2. **Reactive state management**: Textual's reactive properties for auto-updates
3. **Character-by-character comparison**: Real-time feedback without buffering
4. **Timer-based updates**: 100ms interval for WPM recalculation
5. **Exercise loader**: Scans directories and loads .txt files with metadata
6. **Keyboard layout system**: Separate layouts for English/Norwegian with finger color coding

### Key Implementation Details:
- **WPM Standard**: 1 word = 5 characters (industry standard)
- **Accuracy Penalty**: Penalizes both wrong characters AND length differences
- **Backspace Support**: Allows error correction without penalty after fixing
- **Line-based or word-based**: Can practice word-by-word or continuous text
- **Visual Feedback Prioritization**: 
  1. Next char highlight (blue) takes precedence
  2. Then error highlights (red)
  3. Finally correct/pending states (green/dim)

### UI/UX Learnings:
- Monospace fonts are essential for alignment
- Large font sizes (16-18pt) reduce eye strain
- Clear color differentiation: Green (correct), Red (error), Blue (next), Gray (pending)
- Keyboard visualization helps beginners learn finger placement
- Real-time mistake tracking helps identify problem keys
- Summary stats motivate improvement

---

## Additional Recommendations

### Performance Optimization:
- Use `const` constructors where possible
- Debounce frequent UI updates (e.g., 100ms for WPM)
- Lazy load exercises list for large collections
- Cache finger map widget to avoid rebuild

### Accessibility:
- Support keyboard-only navigation
- Consider colorblind-friendly palette option
- Adjustable font sizes
- Optional audio feedback for mistakes

### Future Enhancements:
- User profiles and progress tracking over time
- Graphical charts showing WPM improvement
- Difficulty levels (beginner, intermediate, advanced)
- Timed challenges and leaderboards
- Import/Export exercises
- Custom keyboard layout support
- Dark mode theme

---

## Testing Strategy

### Unit Tests:
- WPM calculation with various inputs
- Accuracy calculation edge cases
- Character status determination
- Weighted word selection algorithm
- Exercise CRUD operations

### Widget Tests:
- Target text rendering and highlighting
- Input field behavior
- Finger map key highlighting
- Menu interactions

### Integration Tests:
- Full typing session flow
- Exercise management workflow
- Mode switching (Review ↔ Weighted)
- Language switching (English ↔ Norwegian)

---

## Summary

This prompt provides comprehensive specifications for building a professional touch typing trainer in Flutter based on the proven architecture of TouchPy. The application focuses on:

1. **Desktop-first experience** with traditional menu bar
2. **Real-time visual feedback** using color-coded text
3. **Comprehensive exercise management** (CRUD operations)
4. **Two practice modes** (Review and Weighted Repetition)
5. **Bilingual support** (English and Norwegian keyboards)
6. **Performance tracking** with WPM, accuracy, and error analysis
7. **Interactive finger map** showing proper hand positioning

Follow this specification step-by-step to build a complete, production-ready typing trainer that combines educational value with modern UI/UX design.
