import requests

rs = requests.session()

url = "https://www.thebump.com/real-answers/v1/topics/926/questions"

params = {
    "include_user": "true",
    "page_num": 1,
    "page_size": 67
}

res = rs.get(url,params=params)


j = res.json()

list = j['questions']
for i in range(len(list)):

    print(list[i])



# print(len(j['questions']))







def get_topicid_from_html(html):

    id_index = html.find("gon.topic_id")
    id_html = html[id_index:]
    start_index = id_html.find("=")
    end_index = id_html.find(";")

    return int(id_html[start_index+1:end_index])


# res2 = rs.get("https://www.thebump.com/real-answers/topics/morning-sickness")
#
# id = get_topicid_from_html(res2.text)
# print(id)









