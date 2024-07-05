# Flask Weather Greeting App

This Flask application greets visitors based on their provided name (extracted from query parameters), retrieves their IP address, and fetches current weather information using the WeatherAPI.

## Features

- **Greeting Endpoint**: `/hello`
  - Greets visitors based on their provided name.
  - If no name is provided, a generic greeting is displayed.

- **Weather Information Endpoint**: `/hello`
  - Fetches the visitor's IP address.
  - Retrieves current weather information based on the visitor's IP using WeatherAPI.

## Setup

### Prerequisites

- Python 3.x
- Flask
- Requests library
- WeatherAPI API key

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Create a virtual environment and activate it:
    ```python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```


3. Install dependencies

    ```
    pip install -r requirements.txt
    ```

4. Set up your WeatherAPI key as an environment variable:

    ```
    export API_KEY='your_weather_api_key'
    ```
    On Windows, use:
    ```
    set API_KEY='your_weather_api_key'
    ```

## Running the Application
### Start the Flask development server:

```
flask run
```


Navigate to http://127.0.0.1:5000/ to see the welcome message.

To get a personalized greeting, navigate to http://127.0.0.1:5000/hello?visitor_name=YourName.


## Example Response
When you visit the /hello endpoint, you will get a JSON response like this:

```
{
    "client_ip": "127.0.0.1",
    "location": "Lagos",
    "greeting": "Hello, YourName!, the temperature is 27.7 degrees  Celsius in Lagos."
}
```


### Live URL: https://hng-stage-1-weld.vercel.app/api/


