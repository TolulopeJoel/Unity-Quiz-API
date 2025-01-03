# Unity-Quiz-API

Quiz API for Smart Nonsense — A Clipt Company

This documentation provides an overview of the API for managing and retrieving SAT quiz questions with rich text and JSON support.

---

## Features
- **CRUD Operations**: Create, retrieve, update, and delete questions.
- **Rich Text Support**: Questions and solutions can include formatting such as bold, italics, and embedded image URLs.
- **Structured JSON Output**: Retrieve questions in a structured format suitable for integration with platforms like Unity.
- **Categorisation**: Questions can be tagged with categories like math, reading, skills, and difficulty levels.

---

## Getting Started

### Prerequisites
- Python 3.8+
- Required dependencies are listed in `requirements.txt`.

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/TolulopeJoel/Unity-Quiz-API.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Unity-Quiz-API
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
Run Migrations:
```bash
python manage.py migrate
```

Start the development server:
```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`.

---

## Endpoints

### 1. CRUD Operations for Questions

#### Create a Question
- **URL**: `/questions/`
- **Method**: POST
- **Request Body** (example):
    ```json
    {
        "Question": "A rectangle has a length of 3x + 2 and a width of x - 4. What is the expression for its area?",
        "Solution": "<color=green>Choice C is correct.</color> The area of a rectangle is calculated by multiplying the length and the width. Expand (3x + 2)(x - 4) using distributive property: 3x^2 - 12x + 2x - 8 = 3x^2 - 10x + 8.",
        "ImageUrl": "https://example.com/image.jpg",
        "Options": [
            "3x^2 + 10x + 8",
            "3x^2 - 10x - 8",
            "3x^2 - 10x + 8",
            "3x^2 + 2x - 8",
            "3x^2 - 2x - 8"
        ],
        "CorrectAnswer": "3x^2 - 10x + 8",
        "Difficulty": "hard",
        "Tags": [
            "geometry",
            "algebra"
        ],
        "Steps": [
            {
                "Title": "Step 1: Set up the formula for area",
                "Result": "The area of a rectangle is length multiplied by width. Substitute the given expressions: (3x + 2)(x - 4)."
            },
            {
                "Title": "Step 2: Apply the distributive property",
                "Result": "Multiply each term in the first parentheses by each term in the second: (3x * x) + (3x * -4) + (2 * x) + (2 * -4)."
            }
        ]
    }
    ```

- **Field Details**:
    - **`Question`** (required): A string representing the text of the question.
    - **`Solution`** (requiree): A string containing the solution text with optional rich text formatting.
    - **`Options`** (required): An array of strings listing the possible answers.
    - **`CorrectAnswer`** (required): A string representing the correct answer, which must match one of the options.
    - **`Steps`** (required): An array of objects detailing the solution steps, each with:
        - **`Title`**: A string describing the step.
        - **`Result`**: A string with the outcome or explanation for the step.
        - **`ImageUrl`** (optional): A string URL pointing to an image for the step.
    - **`Difficulty`** (optional): A string indicating the question's difficulty level. Allowed values are:
        - `"easy"`
        - `"medium"`
        - `"hard"`
    - **`Tags`** (optional): An array of strings categorizing the question (e.g., `"geometry"`, `"algebra"`).
    - **`ImageUrl`** (optional): A string URL pointing to an image associated with the question.

**Response Structure**:
```json
{
    "id": 1,
    "Question": "string",
    "Solution": "string",
    "Steps": [
        {
            "Title": "string",
            "Result": "string",
            "ImageUrl": "string or null"
        }
    ],
    "Options": ["string"],
    "ImageUrl": "string or null",
    "Difficulty": "string",
    "Tags": ["string"],
    "CorrectAnswer": "string"
}
```

#### Retrieve Questions
- **URL**: `/questions/`
- **Method**: GET
- **Response Structure**:
    ```json
    [
        {
            "id": 1,
            "Question": "string",
            "Solution": "string",
            "Steps": [
                {
                    "Title": "string",
                    "Result": "string",
                    "ImageUrl": "string or null"
                }
            ],
            "Options": ["string"],
            "ImageUrl": "string or null",
            "Difficulty": "string",
            "Tags": ["string"],
            "CorrectAnswer": "string"
        },
        {
            "id": 2,
            "Question": "string",
            "Solution": "string",
            "Steps": [
                {
                    "Title": "string",
                    "Result": "string",
                    "ImageUrl": "string or null"
                }
            ],
            "Options": ["string"],
            "ImageUrl": "string or null",
            "Difficulty": "string",
            "Tags": ["string"],
            "CorrectAnswer": "string"
        },
        ...
    ]
    ```

#### Update a Question
- **URL**: `/questions/<id>/`
- **Method**: PUT
- **Request Body**: Same as the create question endpoint
- **Note**: All fields are required when updating, even if only changing some fields

#### Delete a Question
- **URL**: `/questions/<id>/`
- **Method**: DELETE
- **Response**: Returns empty response with 204 status code

### 2. Retrieve Questions as JSON
- **URL**: `/questions/json/`
- **Method**: GET
- **Query Parameters**: Same as the regular GET endpoint
- **Response**: Returns questions in structured JSON format with rich text and embedded image URLs

## Error Responses

The API returns appropriate HTTP status codes and error messages:

- 400 Bad Request: Invalid input data
- 404 Not Found: Question not found
- 500 Internal Server Error: Server-side error

Example error response:
```json
{
    "status": 400,
    "message": "Answer must be in the options",
    "field": "CorrectAnswer"
}
```



## Contact

For any questions or inquiries, please contact toluisjoel@gmail.com