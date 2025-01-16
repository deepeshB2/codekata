from flask import Flask, request, jsonify
from config import Config
from werkzeug.exceptions import BadRequest
from flask_cors import CORS
import re
from dotenv import load_dotenv


from services.bowling_score_service import BowlingScoreService
from utils.mongo_utility import get_mongo_client

import os
import uuid



score_service = BowlingScoreService()
users_collection = get_mongo_client("users")
games_collection = get_mongo_client("games")
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=os.getenv('CORS_URL'), supports_credentials=True)
    print(os.getenv('CORS_URL'))


    def parse_rolls(rolls_str):
        rolls = rolls_str.split()  # Split by spaces
        parsed_rolls = []

        for roll in rolls:
            if roll == "X":  # Strike case
                parsed_rolls.append("X")
            elif "/" in roll:  # Spare case
                parsed_rolls.append(roll[0])  # First roll
                parsed_rolls.append("/")  # Spare indicator
            else:  # Open frame case (e.g., "9-", "5-")
                parsed_rolls.extend(list(roll))  # Break frame into rolls

        return parsed_rolls

    # Example Usage:
    # rolls_input = "X X X X X X X X X X X X"
    # parsed_rolls = parse_rolls(rolls_input)
    # print(parsed_rolls)  # Expected: ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']


    @app.route("/add-game", methods=["POST"])
    def add_game():
        try:
            data = request.get_json()
            email = data.get("email")
            rolls = data.get("rolls")
            if not email or not rolls:
                raise BadRequest("'email' and 'rolls' are required.")

            user = users_collection.find_one({"email": email})
            if not user:
                return jsonify({"error": "User not found. Please register first."}), 404

            parsed_rolls = parse_rolls(rolls)

            score = score_service.calculate_bowling_score(parsed_rolls)
            game_data = {
                "user_id": user["user_id"],
                "rolls": rolls,
                "score": score
            }
            games_collection.insert_one(game_data)

            return jsonify({"message": "Game added successfully", "score": score, "user_id": user["user_id"]}), 200
        except BadRequest as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500


    @app.route('/register', methods=['POST'])
    def register_user():
        try:
            data = request.get_json()
            email = data.get("email")
            if not email:
                raise BadRequest("'email' is required.")

            user = users_collection.find_one({"email": email})
            if user:
                return jsonify({"message": "User already exists", "user_id": user["user_id"]}), 200

            user = {"email": email, "user_id": str(uuid.uuid4())}
            users_collection.insert_one(user)
            return jsonify({"message": "User registered successfully", "user_id": user["user_id"]}), 201
        except BadRequest as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", "3000")), debug=True)





