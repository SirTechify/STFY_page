print("Python is working!")
print("This is a test script to verify Python is installed correctly.")

# Try importing Flask
try:
    from flask import Flask
    print("Flask is installed!")
    
    # Create a simple Flask app for testing
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "Flask is working!"
    
    print("Starting test server on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    if __name__ == '__main__':
        app.run(debug=True)
        
except ImportError:
    print("Flask is not installed. Please install it with: pip install flask")
except Exception as e:
    print(f"An error occurred: {str(e)}")
