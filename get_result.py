import sys, mysql.connector
from tabulate import tabulate

if __name__ == '__main__':
    if len(sys.argv) < 3 :
        print("Please give the name of NFT collections you want to trace and date range")
        exit()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database="dApp"
    )
    collection = sys.argv[1]
    date_type  = sys.argv[2]
    cursor = mydb.cursor()
    cursor.execute("SELECT DATE_FORMAT(date_trunc('{}', load_time), '%Y-%m-%d') AS {}, AVG(floor_price) AS average_price, STDDEV(floor_price) AS standard_deviation FROM {} GROUP BY DATE_FORMAT(date_trunc('{}', load_time), '%Y-%m-%d') LIMIT 2;".format(date_type, date_type, collection, date_type))

    results = cursor.fetchall()

    print(tabulate(results, headers=[date_type, 'average_price', 'standard_deviation'], tablefmt='psql'))
