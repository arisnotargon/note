"""約数的ソート
2から1000000までの整数を以下の規則に従ってソート（整列）をします。

「1以外の最小の約数」が大きい順に並べる。例えば、143（約数は11）は147（約数は3）よりも前になる。
「1以外の最小の約数」が同じ場合は、その数自身が大きい順に並べる。例えば、119（約数は7）は91（約数は7）よりも前になる。
この規則でソートした場合、先頭から250001番目にある整数（先頭は“1番目”と数えます）は何かを求めてください。"""

import math

def get_primes(n):
    if n < 2:
        return 0
    isPrime = [1] * n
    isPrime[0] = isPrime[1] = 0  # 0和1不是质数，先排除掉

    # 埃式筛，把不大于根号n的所有质数的倍数剔除
    for i in range(2, int(n ** 0.5) + 1):
        if isPrime[i]:
            isPrime[i * i:n:i] = [0] * ((n - 1 - i * i) // i + 1)

    return isPrime


if __name__ == "__main__":
    mil = 1000000
    l = get_primes(mil)
    cnt = 0
    mil_arr = [True] * mil
    for i in range(mil - 1, 0, -1):
        if l[i]:
            maxtimes = math.floor(mil / i)
            for times in range(maxtimes,0,-1):
                prod = i * times
                if mil_arr[prod]:
                    mil_arr[prod] = False
                    cnt += 1
                    print(cnt)
                    if cnt == 250001:
                        print('i===>',i,'times=>',times,'res=>',prod)
                        exit()
