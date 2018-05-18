#coding:utf-8
"""base_data与encrypt_key做按位异或运算，位置一一对应，encrypt_key到达索引末尾，再重头开始"""

import base64


base_data = "muid=800c414626a11b022b6a0f24b3c15b35&conv_time=1478746456&click_id=870a40cf-bdd6-4434-9431-388b4e83409c&client_ip=&sign=c3ed37ed07a75cf524541de82218cdc9"
encrypt_key = "BAAAAAAAAAAABIWS"

result_list = []
j = 0
for data in base_data:
    data_int = ord(data)
    try:
        key_int = ord(encrypt_key[j])
        j += 1
    except IndexError, e:
        j = 0
        key_int = ord(encrypt_key[j])
        j += 1
    xor = data_int^key_int
    result_list.append(str(xor))
result_xor = "".join(result_list)
print result_xor

print base64.urlsafe_b64encode(result_xor)







