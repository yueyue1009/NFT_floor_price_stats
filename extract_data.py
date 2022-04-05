import sys, requests, json
import mysql.connector


if __name__ == '__main__':
    if len(sys.argv) < 2 :
        print("Please give the name of NFT collections you want to trace")
        exit()
    collection = sys.argv[1]
    res = requests.get('https://api.opensea.io/api/v1/collection/{}/stats'.format(collection), headers = {"Accept": "application/json"})
    if res:
        print('floor price: ', json.loads(res.text)['stats']['floor_price'])
    else :
        print('{} is not supported'.format(collection))

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database="dApp"
    )

    mycursor = mydb.cursor()
    mycursor.execute("DROP FUNCTION date_trunc")
    mycursor.execute("create function date_trunc(vInterval varchar(7), vDate timestamp) returns timestamp DETERMINISTIC begin declare toReturn timestamp; if vInterval = 'year' then set toReturn = date_add('1900-01-01', interval TIMESTAMPDIFF(YEAR, '1900-01-01', vDate) YEAR); elseif vInterval = 'quarter' then set toReturn = date_add('1900-01-01', interval TIMESTAMPDIFF(QUARTER, '1900-01-01', vDate) QUARTER); elseif vInterval = 'month' then set toReturn = date_add('1900-01-01', interval TIMESTAMPDIFF(MONTH, '1900-01-01', vDate) MONTH); elseif vInterval = 'week' then set toReturn = date_add('1900-01-01', interval TIMESTAMPDIFF(WEEK, '1900-01-01', vDate) WEEK); elseif vInterval = 'day' then set toReturn = date_add('1900-01-01', interval TIMESTAMPDIFF(DAY, '1900-01-01', vDate) DAY); elseif vInterval = 'hour' then set toReturn = date_add('1900-01-01', interval TIMESTAMPDIFF(HOUR, '1900-01-01', vDate) HOUR); elseif vInterval = 'minute' then set toReturn = date_add('1900-01-01', interval TIMESTAMPDIFF(MINUTE, '1900-01-01', vDate) MINUTE); END IF; return toReturn; end")
    mycursor.execute("CREATE TABLE IF NOT EXISTS {} (floor_price FLOAT, load_time TIMESTAMP);".format(collection))
    mycursor.execute("INSERT INTO {}(floor_price, load_time) VALUES({}, DATE_TRUNC('hour', NOW()));".format(collection, json.loads(res.text)['stats']['floor_price']))
    mydb.commit()



