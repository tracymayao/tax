'''
小砖科技    
给定一个非空数组，返回此数组中第三大的数。如果不存在，则返回数组中最大的数。要求算法时间复杂度必须是O(n)。

我们可以创建一个大小为K的数据容器来存储最小的K个数，然后遍历整个数组，将每个数字和容器中的最大数进行比较，
如果这个数大于容器中的最大值，则继续遍历，否则用这个数字替换掉容器中的最大值。这个方法的理解也十分简单，
至于容器的选择，很多人第一反应便是最大堆，但是python中最大堆如何实现呢？我们可以借助实现了最小堆的heapq库，
因为在一个数组中，每个数取反，则最大数变成了最小数，
整个数字的顺序发生了变化，所以可以给数组的每个数字取反，然后借助最小堆，最后返回结果的时候再取反就可以了
'''


import heapq
def get_least_numbers_big_data(alist, k):
    max_heap = []
    length = len(alist)
    if not alist or k <= 0 or k > length:
        return
    k = k - 1
    for ele in alist:
        # ele = -ele
        if len(max_heap) <= k:
            heapq.heappush(max_heap, ele)
        else:
            heapq.heappushpop(max_heap, ele)

    # return map(lambda -x:x, max_heap)
    return max_heap


if __name__ == "__main__":
    l = [1, 9, 2, 4, 7, 6, 3]
    min_k = get_least_numbers_big_data(l, k=3)
    print(str(list(min_k)))