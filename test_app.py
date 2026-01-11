"""
Simple test Flask app for demonstrating hostify
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Test App - Hostify</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            h1 { margin-top: 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Test App is Live!</h1>
            <p>This Flask app is running on port 5000 and being hosted via Hostify.</p>
            <p><strong>Domain:</strong> app.yaspik.tech</p>
            <p><strong>Status:</strong> Working perfectly!</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("Starting Flask test app on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
