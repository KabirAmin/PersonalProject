import requests
import random
import json
from typing import Optional

class SteamGuessingGame:
    def __init__(self):
        self.steam_api_key = "STEAMWEBAPI"
        self.base_url = "https://api.steampowered.com"
        self.game_reviews = {}
        self.current_game = None
        self.current_review = None
        self.score = 0
        self.total_games = 0
        self.popular_game_ids = [
            570, 730, 1091500, 252490, 275850, 578080, 1172620, 1174180,
            289070, 892970, 1313860, 304930, 233250, 238960, 227300, 440,
            302930, 221100, 570940, 291550, 431960, 377160, 367520, 322330
        ]

    def get_game_name(self, app_id: int) -> Optional[str]:
        try:
            url = f"{self.base_url}/ISteamApps/GetAppDetails/v2"
            params = {"appids": app_id}
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            if str(app_id) in data and data[str(app_id)].get("success"):
                return data[str(app_id)]["data"].get("name")
        except:
            pass
        return None

    def get_game_reviews(self, app_id: int) -> list:
        try:
            url = f"{self.base_url}/appreviews/570"
            params = {
                "json": 1,
                "language": "english",
                "review_type": "positive",
                "num_per_page": 100
            }
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            if data.get("success"):
                reviews = [
                    r.get("review", "").strip()
                    for r in data.get("reviews", [])
                    if r.get("review") and len(r.get("review", "").strip()) > 20
                ]
                return reviews[:50]
        except:
            pass
        return []

    def load_sample_reviews(self):
        self.game_reviews = {
            570: ("Dota 2", [
                "Amazing strategy game with incredible depth. Addictive gameplay!",
                "Best competitive esports game out there. Highly recommend!",
                "Complex but rewarding. Best free-to-play game ever made.",
                "The graphics are stunning and the mechanics are perfectly balanced.",
                "Endless hours of fun with friends. Absolutely fantastic!",
                "Most rewarding game I've ever played. Community is amazing.",
                "Deep strategic gameplay that never gets old.",
            ]),
            730: ("Counter-Strike 2", [
                "Best FPS on the market. Fast-paced competitive action!",
                "Incredible gunplay mechanics. Most satisfying shooter ever!",
                "Perfect balance of skill and teamwork. Simply the best!",
                "24 years and still the king of competitive shooters.",
                "Timeless classic that defined the genre. Must play!",
                "The precision and skill ceiling is unmatched.",
            ]),
            271590: ("Grand Theft Auto V", [
                "Massive open world with endless possibilities. Masterpiece!",
                "Best game ever made. Story is incredible and immersive.",
                "One of the greatest achievements in gaming history!",
                "Sandbox perfection. Can play for thousands of hours.",
                "The attention to detail is absolutely mind-blowing.",
            ]),
            1672970: ("Baldur's Gate 3", [
                "RPG perfection. Hundreds of hours of content!",
                "Best turn-based RPG ever created. Absolute masterpiece!",
                "The freedom and choices are incredible. Simply amazing!",
                "Outstanding storytelling and character development.",
                "Pure magic. Every playthrough is completely different.",
            ]),
            109600: ("Dark Souls", [
                "Challenging and rewarding. Changed gaming forever!",
                "Masterclass in game design. Pure perfection.",
                "Extremely challenging but incredibly satisfying.",
                "The best action RPG ever made. Iconic and legendary.",
            ]),
            252490: ("Rust", [
                "Survival at its finest. Heart-pounding gameplay!",
                "Most intense multiplayer experience ever.",
                "Brutal, unforgiving, and absolutely addictive!",
                "Community-driven chaos that never gets boring.",
            ]),
            1091500: ("Cyberpunk 2077", [
                "Mind-blowing futuristic world. Incredible game!",
                "The atmosphere and story are absolutely phenomenal.",
                "Best cyberpunk themed game ever created.",
            ]),
            578080: ("PlayerUnknown's Battlegrounds", [
                "Revolutionary battle royale. So much fun!",
                "Heart-pounding moments every single game.",
                "The game that started it all. Highly addictive.",
            ]),
        }

    def get_random_game(self):
        if not self.game_reviews:
            self.load_sample_reviews()
        
        app_id = random.choice(list(self.game_reviews.keys()))
        game_name, reviews = self.game_reviews[app_id]
        review = random.choice(reviews)
        
        self.current_game = game_name
        self.current_review = review
        self.total_games += 1
        
        return review, app_id

    def check_guess(self, guess: str) -> bool:
        if guess.strip().lower() == self.current_game.lower():
            self.score += 1
            return True
        return False

    def play(self):
        self.load_sample_reviews()
        print("\n" + "="*60)
        print("STEAM GAME GUESSER")
        print("="*60)
        print("Read the review and guess the game name!")
        print("Type 'quit' to exit\n")
        
        while True:
            review, app_id = self.get_random_game()
            print(f"\nReview: \"{review}\"\n")
            
            guess = input("Your guess: ").strip()
            
            if guess.lower() == 'quit':
                print(f"\n{'='*60}")
                print(f"Final Score: {self.score}/{self.total_games - 1}")
                print(f"Accuracy: {(self.score / max(1, self.total_games - 1) * 100):.1f}%")
                print("="*60)
                break
            
            if self.check_guess(guess):
                print(f"✓ Correct! It's {self.current_game}!")
            else:
                print(f"✗ Wrong! The game was: {self.current_game}")
            
            print(f"Score: {self.score}/{self.total_games - 1}")

if __name__ == "__main__":
    game = SteamGuessingGame()
    game.play()
