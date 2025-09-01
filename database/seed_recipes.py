import sqlite3, os, pathlib, json

BASE = pathlib.Path(__file__).resolve().parent
DB = BASE / "emorecipe.sqlite3"

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def run_sql(path):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    con = connect()
    con.executescript(sql)
    con.commit()
    con.close()

def seed():
    con = connect()
    cur = con.cursor()
    count = cur.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
    if count > 0:
        print("Recipes already seeded.")
        con.close()
        return

    items = [
        # celebration (happy)
        ("Sunshine Fruit Tart", "Bright and zesty tart",
         ["Mixed fruits","Tart base","Custard","Honey"],
         ["Bake tart base","Fill with custard","Top with fruits","Drizzle honey"],
         320, "celebration", "fruit_tart", 4.8),

        ("Party Veggie Pizza", "Crispy thin-crust pizza",
         ["Pizza dough","Tomato sauce","Mozzarella","Veggies"],
         ["Preheat oven","Top and bake 10–12m"],
         540, "celebration", "pizza", 4.7),

        # chocolate (sad)
        ("Midnight Chocolate Mug Cake", "Single-serve quick fix",
         ["Flour","Cocoa","Sugar","Milk","Oil"],
         ["Mix in mug","Microwave 70–90s"],
         420, "chocolate", "mug_cake", 4.6),

        ("Fudgy Brownie Squares", "Dense, gooey brownies",
         ["Chocolate","Butter","Sugar","Eggs","Flour"],
         ["Melt & mix","Bake 20–25m"],
         480, "chocolate", "brownie", 4.7),

        # comfort (stressed)
        ("Comfort Masala Khichdi", "Warm, spiced rice & lentils",
         ["Rice","Moong dal","Ghee","Spices"],
         ["Pressure cook","Tempering & serve"],
         380, "comfort", "khichdi", 4.9),

        ("Ginger Tulsi Tea", "Calming herbal tea",
         ["Water","Ginger","Tulsi","Honey"],
         ["Simmer 5–7m","Strain & sip"],
         30, "comfort", "herbal_tea", 4.5),

        # high_protein (excited)
        ("Paneer Tikka Wrap", "Grilled paneer, crunchy salad",
         ["Paneer","Yogurt","Spices","Tortilla"],
         ["Marinate & grill","Wrap & serve"],
         560, "high_protein", "paneer_wrap", 4.6),

        ("Protein Power Bowl", "Quinoa, beans & veggies",
         ["Quinoa","Black beans","Corn","Avocado"],
         ["Cook quinoa","Assemble & dress"],
         520, "high_protein", "protein_bowl", 4.6),

        # fresh (energized)
        ("Minty Cucumber Cooler", "Ultra-refreshing drink",
         ["Cucumber","Mint","Lime","Soda"],
         ["Blend & top with soda"],
         90, "fresh", "cooler", 4.4),

        ("Rainbow Crunch Salad", "Crisp veggies + seeds",
         ["Lettuce","Carrots","Peppers","Seeds","Dressing"],
         ["Chop & toss"],
         260, "fresh", "salad", 4.5),
    ]

    for title, desc, ings, steps, cal, tag, img, rating in items:
        cur.execute("""
            INSERT INTO recipes(title, description, ingredients, steps, calories, mood_tag, image_url, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, desc, json.dumps(ings), json.dumps(steps), cal, tag, img, rating))

    con.commit()
    con.close()
    print("Seeded recipes to", DB)

if __name__ == "__main__":
    os.makedirs(BASE, exist_ok=True)
    run_sql(BASE / "schema.sql")
    seed()