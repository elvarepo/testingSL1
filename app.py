from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory mock database
records = []

@app.route("/")
def home():
    return jsonify({
        "message": "Pet Record Service is running on EC2 via Jenkins CI/CD"
    })

@app.route("/pets", methods=["GET"])
def get_pets():
    return jsonify(records), 200

@app.route("/pets", methods=["POST"])
def add_pet():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ["pet_name", "owner_name", "visit_date", "details"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    record = {
        "id": len(records) + 1,
        "pet_name": data["pet_name"],
        "owner_name": data["owner_name"],
        "visit_date": data["visit_date"],
        "details": data["details"]
    }

    records.append(record)
    return jsonify({
        "message": "Pet visit recorded successfully",
        "record": record
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
