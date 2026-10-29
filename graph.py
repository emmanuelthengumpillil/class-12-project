import matplotlib.pyplot as plt
import io
import base64
import database


def usercount_analysis():
    query = "Select name, date_modified from customers"
    data = database.connect_sql(query)

    user_count = {}

    for row in data:
        date = row['date_modified']
        if date not in user_count:
            user_count[date] = 0
        user_count[date] += 1


    sorted_dates = []
    count_values = []

    for date, count in user_count.items():
        sorted_dates.append(date)
        count_values.append(count)

    result = graph(sorted_dates, count_values)
    return result
    

def graph(sorted_dates, count_values):
    plt.figure(figsize=(4, 4))
    plt.subplot(2, 1, 1)
    plt.plot(sorted_dates, count_values, marker = "o")

    plt.xlabel("Date")
    plt.ylabel("No of customers")


    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", bbox_inches="tight")
    img_buffer.seek(0)

    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt.close()

    return img_base64
