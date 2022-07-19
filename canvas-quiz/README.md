# Canvas Quiz from CSV

Canvas supports the QTI XML format for quiz content imports. With this code, create a quiz in a CSV file and generate the XML to import.

## Usage

1. Name your CSV file the name of your Quiz (e.g. `My Quiz.csv`)
2. Update `CSV_FILENAME` in `main.py`. (e.g. `CSV_FILENAME = "My Quiz.csv"`)

### CSV File Format

Here's an example CSV file with a 5 point multiple choice question (row 1) and a 2 point multiple response question (row 2). The last column is an array of correct answer indicies (zero-indexed). For example, the first row's correct answer is "c" (index 2) and the second row's correct answers are "a" and "d" (index 0 and 3).

```python
5,"This is <strong>question 1</strong>","[""a"", ""b"", ""c"", ""d""]","[2]"
2,"This is <strong>question 2</strong>","[""a"", ""b"", ""c"", ""d""]","[0, 3]"
```

## Based On

[CSV for Canvas Quizzes](https://dl.sps.northwestern.edu/canvas/2021/06/add-quiz-questions-to-canvas-by-converting-csv-files-to-qti-zip-files/)

[CSV to QTI](https://canconvert.k-state.edu/qti/)
