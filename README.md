# MentL - Health Tracking Web Application

The app can be viewed [here](https://mikehawk-mentl.onrender.com/)

MentL is a Flask-based web application designed to help users track and manage their health metrics, such as sleep, physical activity, and calorie intake. The application includes features like user authentication, data logging, score calculation, and a dashboard to visualize health metrics.

---

## Authors

- Prayas Sinha (Backend Team)
- Aritro Shome (Backend Team, Team Lead)
- SK Asif Tanvir (Frontend Team)
- Vedanta Saha (Frontend Team)

---

## Features

- **User Authentication**: Signup, login, and logout functionalities.
- **Health Data Logging**: Record sleep, physical activity, and calorie intake.
- **Score Calculation**: Generate health scores for sleep, physical activity, and calorie intake.
- **Dashboard**: Visualize health scores.
- **Journaling**: Maintain a journal to track daily thoughts or activities.
---

## Project Structure

```
├── app.py
├── bin/
├── documentation.txt
├── include/
├── lib/
├── lib64/
├── LICENSE
├── mail.py
├── pyvenv.cfg
├── README.md
├── requirements.txt
├── serviceAccountKey.json
├── static/
│   ├── dash.css
│   ├── dash.js
│   ├── getjourn.js
│   ├── home.css
│   ├── home.js
│   ├── journal.css
│   ├── journal.js
│   ├── login.css
│   ├── login.js
├── templates/
│   ├── about.html
│   ├── articles.html
│   ├── community.html
│   ├── dashboard.html
│   ├── getjourn.html
│   ├── home.html
│   ├── journal.html
│   ├── login.html
└── .gitignore
```

---

## Installation

### Prerequisites

- Python 3.7+
- Firebase account with a service account key

### Steps

1. Clone the repository:
    ```bash
    git clone <https://github.com/sortira/MentL>
    cd <MentL>
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up Firebase:
    - Place your `serviceAccountKey.json` file in the root directory.

5. Run the Flask application:
    ```bash
    flask run
    ```

6. Open your web browser and navigate to `http://127.0.0.1:5000`.

---

## Functions

### User Authentication

- **`signup()`**: Handles user signup by creating a new user document in the Firestore database.
- **`login()`**: Verifies user credentials and logs in the user.
- **`logout_user()`**: Logs out the current user.

### Health Data Logging

- **`log_sleep()`**: Logs sleep data for the current user.
- **`log_physical_activity()`**: Logs physical activity data for the current user.
- **`log_food()`**: Logs food data (calories) for the current user.
- **`log_journalling()`**: Logs journaling content for the current user.

### Score Calculation

- **`calculate_sleep_score(email)`**: Calculates the sleep score based on logged sleep data.
- **`calculate_physical_activity_score(email)`**: Calculates the physical activity score based on logged exercise data.
- **`calculate_calories_score(email)`**: Calculates the calorie intake score based on logged food data.
- **`calculate_mentl_score(email)`**: Computes the overall health score by averaging sleep, physical activity, and calorie scores.

### Page Rendering

- **`home()`**: Renders the home page.
- **`send_dashboard_page()`**: Renders the dashboard page with health scores.
- **`send_articles_page()`**: Renders the articles page.
- **`send_aboutus_page()`**: Renders the about us page.
- **`send_community_page()`**: Placeholder for rendering the community page.
- **`getJourns()`**: Fetches and displays journaling data for the current user.
- **`send_journalling_page()`**: Renders the journaling page with the current day's journal content if available.

---

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

