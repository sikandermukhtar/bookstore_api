import csv

valid_books = [
    ["Deep Work","Cal Newport",25.50,"https://example.com/images/deep_work.jpg","2016-01-05"],
    ["Atomic Habits","James Clear",20.99,"https://example.com/images/atomic_habits.jpg","2018-10-16"],
    ["The Lean Startup","Eric Ries",22.00,"https://example.com/images/lean_startup.jpg","2011-09-13"],
    ["Thinking, Fast and Slow","Daniel Kahneman",18.50,"https://example.com/images/thinking_fast_slow.jpg","2011-10-25"],
    ["The 7 Habits of Highly Effective People","Stephen R. Covey",19.99,"https://example.com/images/7_habits.jpg","1989-08-15"],
    ["Start With Why","Simon Sinek",21.50,"https://example.com/images/start_with_why.jpg","2009-09-01"],
    ["Grit","Angela Duckworth",17.75,"https://example.com/images/grit.jpg","2016-05-03"],
    ["The Power of Habit","Charles Duhigg",16.99,"https://example.com/images/power_of_habit.jpg","2012-02-28"],
    ["Hooked","Nir Eyal",23.00,"https://example.com/images/hooked.jpg","2014-11-24"],
    ["Drive","Daniel H. Pink",18.25,"https://example.com/images/drive.jpg","2009-04-21"],
]

faulty_books = [
    ["Deep Work","Cal Newport",25.50,"https://example.com/images/deep_work.jpg","2016-01-05"],
    ["Atomic Habits","James Clear","abc","https://example.com/images/atomic_habits.jpg","2018-10-16"],  # price invalid
    ["","Eric Ries",22.00,"https://example.com/images/lean_startup.jpg","2011-09-13"],  # missing title
    ["Thinking, Fast and Slow","Daniel Kahneman",18.50,"https://example.com/images/thinking_fast_slow.jpg","2011-10-25"],
    ["The 7 Habits of Highly Effective People","Stephen R. Covey",19.99,"","1989-08-15"],  # missing cover image
    ["Start With Why","Simon Sinek",21.50,"https://example.com/images/start_with_why.jpg","2009-09-01"],
    ["Grit","Angela Duckworth",17.75,"https://example.com/images/grit.jpg","not_a_date"],  # invalid date
    ["The Power of Habit","Charles Duhigg",16.99,"https://example.com/images/power_of_habit.jpg","2012-02-28"],
    ["Hooked","Nir Eyal",23.00,"https://example.com/images/hooked.jpg","2014-11-24"],
    ["Drive","Daniel H. Pink",18.25,"https://example.com/images/drive.jpg","2009-04-21"],
]

header = ["title","author","price","book_cover_image","published_date"]

def write_csv(filename, data):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    print(f"{filename} created with {len(data)} rows.")

if __name__ == "__main__":
    write_csv("books_valid.csv", valid_books)
    write_csv("books_faulty.csv", faulty_books)
