from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/receive-report', methods=['POST'])
def receive_report():
    try:
        # Get JSON data sent from GitHub Actions
        report_data = request.json
        
        if not report_data:
            return jsonify({"error": "No data received"}), 400
        
        # Save as test-report.json locally
        filename = "test-report.json"
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=4)
            
        print("\n[SUCCESS] Test report successfully received and saved as 'test-report.json'!")
        print(f"Overall Status: {report_data.get('overall_status')}")
        print(f"Passed: {report_data.get('passed_count')} | Failed: {report_data.get('failed_count')}\n")
        
        return jsonify({"status": "success", "message": "Report saved successfully"}), 200
        
    except Exception as e:
        print(f"[ERROR] Failed to save report: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Runs on port 5000 locally
    app.run(host='0.0.0.0', port=5000)