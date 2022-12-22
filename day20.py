from helpers import read_intlines


class Number:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

    def move(self):
        # connect the previous number to the next number
        nxt = self.next
        prv = self.prev

        # move self.val to the next number
        cur = self
        for i in range(self.val):
            cur = cur.next

        # connect the previous to the next, removing self from between them
        prv.next = nxt
        nxt.prev = prv

        # put self between cur and cur.next

        # step 1. connect self to cur.next
        cur.next.prev = self
        self.next = cur.next
        # step 2. connect self to cur
        cur.next = self
        self.prev = cur


# this order should be kept
nums = list(read_intlines("day20_example.txt"))

prevnum = None
start = None
num_objects = {}
for i in nums:
    num = Number(i)
    if prevnum:
        num.prev = prevnum
        prevnum.next = num
    else:
        start = num
    num_objects[num.val] = num
    prevnum = num

# connect the last number to the first
num.next = start
start.prev = num

for num in nums:
    num_obj = num_objects[num]
    num_obj.move()
