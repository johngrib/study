# 파이썬 문법 요약 (3 기준)

# 샵 기호를 앞에 쓰면 주석이 된다.

'''
여러 줄 주석은 이렇게 쓴다.
여러 줄 string 과 똑같은 것 같지만, 변수에 입력하지 않으면 bytecode 를 생성하지 않는다.
아래의 링크는 여러 줄 주석에 대한 귀도 반 로썸 아저씨의 대답.
https://twitter.com/gvanrossum/status/112670605505077248
'''

# 기본 데이터 타입은 세 가지
string_value = '문자열'
raw_string = r'문자열\''   # 따옴표 앞에 r 이 있으면 raw string 으로 평가되어 \ 를 이스케이프로 평가하지 않는다.
float_number = 3.14
integer_number = 100
null_object = None  # python 에서는 null 이 아니라 None 이다.

# 기본 연산자는 다음과 같다. (연산자 우선순위 순)
2 ** 10  # 1024 : 거듭제곱
7 % 2  # 1    : 나머지
7 // 2  # 3    : 정수 나눗셈 (나머지를 버린다)
7 / 2  # 3.5
7 * 2  # 14
7 - 2  # 5
7 + 2  # 9
# 물론 +=, -=, *=-, /=, %= 등도 사용할 수 있다.

# 문자열 연결은 + 를 쓴다.
'abc' + 'def'  # 'abcdef'

# 문자열에 * 연산자를 사용하는 것도 가능하다.
'abc' * 3  # 이렇게 하면 'abcabcabc' 가 된다. 단, 정수만 가능하다.

# 숫자는 바로 연결하면 TypeError 가 발생하므로 str 함수를 사용해야 한다.
'abc' + str(4)  # 'abc4'

# 한 줄 코드를 여러 줄로 쓰려면 \ 를 쓴다.
a = 2 + \
    3       # a = 2 + 3

# 타입 캐스팅은 아래와 같이 한다.
int('900') + 100  # 1000
float('3.14') + 100  # 103.14
float(10)  # 10.0

# 문자열이나 리스트 등의 길이를 재려면 len 함수를 쓴다.
len('test')  # 4 : 문자열의 길이
len([1, 2, 3])  # 3 : 리스트의 길이
len((1, 2))  # 2 : 튜플의 길이

# 키보드에서 문자열 입력을 받을 땐 input 함수를 쓰면 된다.
print('아무거나 입력하고 엔터키를 누르세요.')
# test = input()
# print(test)

# 출력 요령
print('hello')      # hello
print('world!')     # world!

print('hello', end=',')
print('world!')     # hello,world!

print('hello', 'world!', 'hello', 'python!')           # hello world! hello python!
print('hello', 'world!', 'hello', 'python!', sep=',')  # hello,world!,hello,python!

# 부울 값. 첫 글자가 대문자다.
True
False

# 비교 연산자는 ==, !=, <, >, <=, >=, and, or, not 를 쓴다.
10 == 10.0  # True
10 != '10'  # True
not True  # False

# if 문
value = 10
if value == 10 and True:
    print('if 문은 이렇게 쓴다.')
elif value == 20:
    print('else if 가 아니라 elif 다.')
else:
    print('python 은 인덴트로 code block 을 구분하므로 인덴트에 주의해야 한다.')

# while 문
while value < 10:
    print('while 문은 이렇게 쓴다.')
    if value == 5:
        break
    else:
        continue

# for 문과 range 함수
for i in range(3):  # 3 번 루프한다.
    print(i)  # 0,1,2 를 출력한다.

for i in range(30, 33):  # 30 부터 33 이전까지 루프한다.
    print(i)  # 30, 31, 32 를 출력한다.

for i in range(70, 80, 2):  # 70 부터 80 이전까지 +2 step 으로 루프한다.
    print(i)  # 70, 72, 74, 76, 78 을 출력한다.

for i in range(2, -3, -1):  # 2 부터 -3 이전까지 -1 step 으로 루프한다.
    print(i)  # 2, 1, 0, -1, -2 를 출력한다.

# 모듈 임포트
import random

random.randint(1, 3)  # 1,2,3 중 하나를 랜덤으로 뽑는다.

import sys, os, math  # 여러 임포트를 한꺼번에 하는 것도 가능하다.


# sys.exit()  # 프로그램 종료

# 함수
def test_hello(name):
    return 'hello, ' + name

test_hello('john')  # 'hello, john'

def return_None():
    print('return None')
    # 아무것도 리턴하지 않는 함수라면 리턴값은 None 이 된다.

global_num = 42
def using_global():
    global global_num
    global_num = 17

using_global()
print(global_num)   # 17

# 예외 처리
try:
    42 / 0
except ZeroDivisionError:
    print('숫자를 0 으로 나눈 오류 발생')

# 리스트
sample_list = [11, 22, 33]
sample_list[0]     # 11
sample_list[-1]    # 33

# 리스트 slice
sample_list = ['a', 'b', 'c', 'd', 'e']
sample_list[1:2]   # ['b']
sample_list[2:4]   # ['c', 'd']
sample_list[:]     # ['a', 'b', 'c', 'd', 'e']

# 리스트 원소 검사
'a' in sample_list  # True
'f' not in sample_list  # True

# 리스트 원소 삭제
del sample_list[0]  # ['b', 'c', 'd', 'e']
del sample_list[1]  # ['b', 'd', 'e']

# 리스트 concat
[1,2] + [3]  # [1, 2, 3]
[1,2,3] * 2     # [1, 2, 3, 1, 2, 3]

# 리스트 iteration
for s in ['a', 'b', 'c']:
    print(s)

# 리스트를 통한 변수 할당 (변수의 갯수와 리스트의 길이가 일치해야 한다.)
aa, bb, cc = ['aa', 'bb', 'cc']

# 리스트 원소 검색하여 인덱스 리턴
['aa', 'bb', 'cc'].index('bb')  # 1

# 리스트에 원소 추가
sample_list = ['aa', 'bb', 'cc']
sample_list.append('dd')       # ['aa', 'bb', 'cc', 'dd']
sample_list.insert(2, '22')    # ['aa', 'bb', '22', 'cc', 'dd']
sample_list.remove('cc')       # ['aa', 'bb', '22', 'dd']
sample_list.sort()             # ['22', 'aa', 'bb', 'dd']
sample_list.sort(reverse=True)  # ['dd', 'bb', 'aa', '22']
print(sample_list)

# 문자열도 리스트로 취급된다.
string_value = 'abc'
string_value[1]     # 'b'
'bc' in string_value    # True
for s in string_value:  # 루프도 가능하다.
    print(s)

# 튜플
sample_tuple = (1, 'bb')
sample_tuple[0]         # 1
#sample_tuple[0] = 2    # 튜플에 값을 대입하면 에러가 발생
list(sample_tuple)      # [1, 'bb'] # tuple 을 list 로 변환
tuple([1, 2, 3])        # (1, 2, 3) # list 를 tuple 로 변환

# 리스트 복사
import copy
list1 = [1, 2, 3]
list2 = copy.copy(list1)    # deepcopy 도 있다.
list1.append(4)
print(list1)    # [1, 2, 3, 4]
print(list2)    # [1, 2, 3]

# 사전
sample_dict1 = {'name': 'test', 'text': 'sample'}
sample_dict1['name']     # 'test
sample_dict2 = {'text': 'sample', 'name': 'test'}
sample_dict1 == sample_dict2    # True
sample_dict1.keys()     # dict_keys(['name', 'text'])
sample_dict1.values()   # dict_values(['sample', 'test'])

for v in sample_dict1.values():
    print(v)

for v in sample_dict1.keys():
    print(v)

for v in sample_dict1.items():
    print(v)    # (key, value) 의 튜플

'name' in sample_dict1.keys()       # True
'42' not in sample_dict1.values()   # True

sample_dict1.get('name', 'John')    # 'test'
sample_dict1.get('age', 30)         # 30
sample_dict1.setdefault('name', 'Tom')  # {'text': 'sample', 'name': 'test'}
sample_dict1.setdefault('age', 35)      # {'age': 35, 'text': 'sample', 'name': 'test'}
