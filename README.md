# Healthcare Chatbot Mobile App

This is a mobile app that utilizes a chatbot to assist users with their healthcare needs. The app is built with Django and Celery for the backend and React for the frontend.

## Installation
To install and run the app, follow these steps:

### Clone the repository
Install the necessary packages using pip and npm

1. Set up the Django database and run migrations
2. Start the Django and Celery servers
3. Start the React frontend
4. Usage

Once the app is installed and running, users can interact with the chatbot through the mobile app. The chatbot utilizes a Fine-tuned GODEL transformer model by Microsoft to answer healthcare-related questions.

The app also includes a pre-processing step to confirm if the user is talking about healthcare topics, a post-processing step to check the chatbot's sentiment, and a module to find reference links for any medicine recommended by the chatbot.

### Contributing
Contributions to the app are welcome. If you would like to contribute, please submit a pull request.

### License
This app is licensed under the MIT License.
